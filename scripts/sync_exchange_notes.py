"""Build the site-local UCSD exchange reading page from its canonical README."""

from __future__ import annotations

import os
from pathlib import Path
from urllib.request import Request, urlopen


SOURCE_URL = os.environ.get(
    "EXCHANGE_SOURCE_URL",
    "https://raw.githubusercontent.com/JunjieNian/myUCSDexchange/main/README.md",
)
OUTPUT_PATH = Path(os.environ.get("EXCHANGE_OUTPUT_PATH", "exchange.md"))

FRONT_MATTER = """---
layout: exchange
title: "我的 UCSD 交换经历 | Junjie Nian"
description: "Junjie Nian 持续更新的 UCSD 交换经历：从申请、行前准备到校园生活，为后来的交换生提供个人经验参考。"
permalink: /exchange/
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


def main() -> None:
    source = fetch_source()
    OUTPUT_PATH.write_text(FRONT_MATTER + source + "\n", encoding="utf-8", newline="\n")
    print(f"Synchronized {len(source)} characters from {SOURCE_URL} to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
