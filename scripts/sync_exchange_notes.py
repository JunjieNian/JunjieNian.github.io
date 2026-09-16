"""Build the site-local UCSD exchange reading page from its canonical README."""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo


SOURCE_URL = os.environ.get(
    "EXCHANGE_SOURCE_URL",
    "https://raw.githubusercontent.com/JunjieNian/myUCSDexchange/main/README.md",
)
SOURCE_COMMIT_API_URL = os.environ.get(
    "EXCHANGE_SOURCE_COMMIT_API_URL",
    "https://api.github.com/repos/JunjieNian/myUCSDexchange/commits?path=README.md&per_page=1",
)
OUTPUT_PATH = Path(os.environ.get("EXCHANGE_OUTPUT_PATH", "exchange.md"))
DISPLAY_TIME_ZONE = ZoneInfo("Asia/Shanghai")


def build_front_matter(last_updated: datetime) -> str:
    last_updated_iso = last_updated.isoformat(timespec="seconds")
    last_updated_display = (
        f"{last_updated.year} 年 {last_updated.month} 月 {last_updated.day} 日 "
        f"{last_updated:%H:%M}"
    )
    return f"""---
layout: exchange
title: "我的 UCSD 交换经历 | Junjie Nian"
description: "Junjie Nian 持续更新的 UCSD 交换经历：从申请、行前准备到校园生活，为后来的交换生提供个人经验参考。"
permalink: /exchange/
last_updated: "{last_updated_iso}"
last_updated_display: "{last_updated_display}"
---

"""


def fetch_source() -> str:
    request = Request(SOURCE_URL, headers={"User-Agent": "JunjieNian.github.io exchange sync"})
    with urlopen(request, timeout=30) as response:
        body = response.read().decode("utf-8")

    normalized = body.replace("\r\n", "\n").replace("\r", "\n").strip()
    if len(normalized) < 500 or "# 我的 UCSD 交换经历" not in normalized:
        raise RuntimeError("The fetched README did not match the expected exchange record.")
    return normalized


def fetch_last_updated() -> datetime:
    request = Request(
        SOURCE_COMMIT_API_URL,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "JunjieNian.github.io exchange sync",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urlopen(request, timeout=30) as response:
        commits = json.load(response)

    if not commits:
        raise RuntimeError("GitHub returned no commits for the canonical exchange record.")

    committed_at = commits[0]["commit"]["committer"]["date"]
    return datetime.fromisoformat(committed_at.replace("Z", "+00:00")).astimezone(
        DISPLAY_TIME_ZONE
    )


def main() -> None:
    source = fetch_source()
    last_updated = fetch_last_updated()
    OUTPUT_PATH.write_text(
        build_front_matter(last_updated) + source + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        f"Synchronized {len(source)} characters from {SOURCE_URL} to {OUTPUT_PATH}; "
        f"last updated {last_updated.isoformat(timespec='seconds')}"
    )


if __name__ == "__main__":
    main()
