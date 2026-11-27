"""Build the site-local UCSD exchange reading page from its canonical README."""

from __future__ import annotations

import json
import os
import re
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
CHAPTERS_DIR = Path(os.environ.get("EXCHANGE_CHAPTERS_DIR", "exchange-pages"))
DISPLAY_TIME_ZONE = ZoneInfo("Asia/Shanghai")
CHAPTER_HEADING = re.compile(
    r"^##[ \t]+(第[一二三四五六七八九十百零\d]+章[：:].+)$", re.MULTILINE
)
GENERATED_MARKER = "generated_by: sync_exchange_notes.py"


def build_front_matter(
    last_updated: datetime, chapter_number: int, chapters: list[dict[str, str | int]]
) -> str:
    last_updated_iso = last_updated.isoformat(timespec="seconds")
    last_updated_display = (
        f"{last_updated.year} 年 {last_updated.month} 月 {last_updated.day} 日 "
        f"{last_updated:%H:%M}"
    )
    permalink = "/exchange/" if chapter_number == 1 else f"/exchange/{chapter_number}/"
    page_title = (
        "我的 UCSD 交换经历 | Junjie Nian"
        if chapter_number == 1
        else f"{chapters[chapter_number - 1]['title']} | 我的 UCSD 交换经历"
    )
    chapter_list = "\n".join(
        "  - number: {number}\n    title: {title}\n    url: {url}".format(
            number=chapter["number"],
            title=json.dumps(chapter["title"], ensure_ascii=False),
            url=json.dumps(chapter["url"]),
        )
        for chapter in chapters
    )
    return f"""---
{GENERATED_MARKER}
layout: exchange
title: {json.dumps(page_title, ensure_ascii=False)}
description: "Junjie Nian 持续更新的 UCSD 交换经历：从申请、行前准备到校园生活，为后来的交换生提供个人经验参考。"
permalink: "{permalink}"
last_updated: "{last_updated_iso}"
last_updated_display: "{last_updated_display}"
chapter_number: {chapter_number}
chapters:
{chapter_list}
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
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "JunjieNian.github.io exchange sync",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(
        SOURCE_COMMIT_API_URL,
        headers=headers,
    )
    with urlopen(request, timeout=30) as response:
        commits = json.load(response)

    if not commits:
        raise RuntimeError("GitHub returned no commits for the canonical exchange record.")

    committed_at = commits[0]["commit"]["committer"]["date"]
    return datetime.fromisoformat(committed_at.replace("Z", "+00:00")).astimezone(
        DISPLAY_TIME_ZONE
    )


def split_chapters(source: str) -> tuple[list[dict[str, str | int]], list[str]]:
    matches = list(CHAPTER_HEADING.finditer(source))
    if not matches:
        raise RuntimeError("The exchange record has no numbered chapter headings.")

    introduction = source[: matches[0].start()].strip()
    title = source.splitlines()[0]
    if not title.startswith("# ") or not introduction:
        raise RuntimeError("The exchange record is missing its title or introduction.")

    chapters = []
    pages = []
    for number, match in enumerate(matches, start=1):
        next_start = matches[number].start() if number < len(matches) else len(source)
        body = source[match.start() : next_start].strip()
        url = "/exchange/" if number == 1 else f"/exchange/{number}/"
        chapters.append({"number": number, "title": match.group(1), "url": url})
        pages.append((introduction if number == 1 else title) + "\n\n" + body + "\n")
    return chapters, pages


def main() -> None:
    source = fetch_source()
    last_updated = fetch_last_updated()
    chapters, pages = split_chapters(source)
    OUTPUT_PATH.write_text(
        build_front_matter(last_updated, 1, chapters) + pages[0],
        encoding="utf-8",
        newline="\n",
    )

    CHAPTERS_DIR.mkdir(parents=True, exist_ok=True)
    generated_paths = set()
    for number, body in enumerate(pages[1:], start=2):
        path = CHAPTERS_DIR / f"{number}.md"
        path.write_text(
            build_front_matter(last_updated, number, chapters) + body,
            encoding="utf-8",
            newline="\n",
        )
        generated_paths.add(path)

    for path in CHAPTERS_DIR.glob("[0-9]*.md"):
        if path not in generated_paths and path.read_text(encoding="utf-8").startswith(
            f"---\n{GENERATED_MARKER}\n"
        ):
            path.unlink()

    print(
        f"Synchronized {len(source)} characters in {len(chapters)} chapters from {SOURCE_URL}; "
        f"last updated {last_updated.isoformat(timespec='seconds')}"
    )


if __name__ == "__main__":
    main()
