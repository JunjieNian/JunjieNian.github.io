"""Build the site-local UCSD exchange journal from its canonical repository."""

from __future__ import annotations

import json
import os
import re
from datetime import datetime
from io import BytesIO
from pathlib import Path, PurePosixPath
from urllib.request import Request, urlopen
from zipfile import ZipFile
from zoneinfo import ZoneInfo


SOURCE_URL = os.environ.get("EXCHANGE_SOURCE_URL")
SOURCE_REPO = "JunjieNian/myUCSDexchange"
SOURCE_COMMIT_API_URL = os.environ.get(
    "EXCHANGE_SOURCE_COMMIT_API_URL",
    f"https://api.github.com/repos/{SOURCE_REPO}/commits?sha=main&per_page=1",
)
OUTPUT_PATH = Path(os.environ.get("EXCHANGE_OUTPUT_PATH", "exchange.md"))
CHAPTERS_DIR = Path(os.environ.get("EXCHANGE_CHAPTERS_DIR", "exchange-pages"))
DISPLAY_TIME_ZONE = ZoneInfo("Asia/Shanghai")
CHAPTER_HEADING = re.compile(
    r"^##[ \t]+(第[一二三四五六七八九十百零\d]+章[：:].+)$", re.MULTILINE
)
GENERATED_MARKER = "generated_by: sync_exchange_notes.py"
MAP_LINK = re.compile(r"^.*<!-- sd-travel-map -->[ \t]*$", re.MULTILINE)
MAP_ASSET_URL = "/exchange-pages/sd-map/"
MAP_FILES = {"embed.html", "map.css", "map.js", "places.json", "transit.json"}
PHOTO_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".avif"}
USER_AGENT = "JunjieNian.github.io exchange sync"


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


def fetch_source(revision: str) -> str:
    url = SOURCE_URL or f"https://raw.githubusercontent.com/{SOURCE_REPO}/{revision}/README.md"
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=30) as response:
        body = response.read().decode("utf-8")

    normalized = body.replace("\r\n", "\n").replace("\r", "\n").strip()
    if len(normalized) < 500 or "# 我的 UCSD 交换经历" not in normalized:
        raise RuntimeError("The fetched README did not match the expected exchange record.")
    return normalized


def fetch_source_commit() -> tuple[str, datetime]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": USER_AGENT,
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
        raise RuntimeError("GitHub returned no commits for the canonical exchange repository.")

    commit = commits[0]
    committed_at = commit["commit"]["committer"]["date"]
    updated = datetime.fromisoformat(committed_at.replace("Z", "+00:00"))
    return commit["sha"], updated.astimezone(DISPLAY_TIME_ZONE)


def is_map_photo(path: PurePosixPath) -> bool:
    return (
        len(path.parts) == 2
        and path.parts[0] == "photos"
        and path.suffix.lower() in PHOTO_EXTENSIONS
    )


def fetch_map_files(revision: str) -> dict[str, bytes]:
    url = f"https://codeload.github.com/{SOURCE_REPO}/zip/{revision}"
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=60) as response:
        archive_bytes = response.read()

    files = {}
    with ZipFile(BytesIO(archive_bytes)) as archive:
        for entry in archive.infolist():
            parts = PurePosixPath(entry.filename).parts
            if entry.is_dir() or len(parts) < 3 or parts[1] != "sd-map":
                continue
            relative = PurePosixPath(*parts[2:])
            if relative.as_posix() in MAP_FILES or is_map_photo(relative):
                files[relative.as_posix()] = archive.read(entry)

    missing = MAP_FILES - files.keys()
    if missing:
        raise RuntimeError(f"The canonical SD map is missing {', '.join(sorted(missing))}.")
    return files


def sync_map_assets(files: dict[str, bytes]) -> None:
    output = CHAPTERS_DIR / "sd-map"
    for name, contents in files.items():
        destination = output / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(contents)

    for path in [*output.glob("*"), *output.glob("photos/*")]:
        relative = PurePosixPath(path.relative_to(output).as_posix())
        if path.is_file() and (relative.as_posix() in MAP_FILES or is_map_photo(relative)):
            if relative.as_posix() not in files:
                path.unlink()


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
    revision, last_updated = fetch_source_commit()
    source = fetch_source(revision)
    map_files = {}
    if MAP_LINK.search(source):
        map_files = fetch_map_files(revision)
        embed = map_files.pop("embed.html").decode("utf-8").strip()
        embed = embed.replace("__SD_MAP_ASSETS__", MAP_ASSET_URL)
        embed = embed.replace("__SD_MAP_VERSION__", revision[:12])
        source = MAP_LINK.sub(lambda _: embed, source, count=1)

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

    sync_map_assets(map_files)
    print(
        f"Synchronized {len(source)} characters in {len(chapters)} chapters from "
        f"{SOURCE_REPO}@{revision[:12]}; "
        f"last updated {last_updated.isoformat(timespec='seconds')}"
    )


if __name__ == "__main__":
    main()
