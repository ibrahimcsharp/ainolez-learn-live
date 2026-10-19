"""
Turns a .md file into a lesson draft made of blocks (PLANNING.md §6.2).

    ---                      optional front-matter
    title: Python Lists
    minutes: 8
    ---
    # Python Lists           first heading = title (if no front-matter title)
    Some text...             -> markdown block
    ```python tryit          -> example block (Try it Yourself)
    print([1, 2])
    ```
    {{youtube:VIDEO_ID}}     -> video block (on its own line)
    ```exercise              -> exercise block, JSON: {"prompt_md", "check_type",
    {...}                       "expected_value", "starter_code", "solution_code", "hint"}
    ```
    ```quiz                  -> quiz block, JSON: [{"question", "options": [...],
    [...]                       "answer": <index of the right option>, "explanation"}]
    ```                         or {"title", "final": true, "questions": [...]}
"""

import io
import json
import re
import zipfile
from dataclasses import dataclass, field
from pathlib import PurePosixPath

from modules.content_tools.markdown_render import FENCE, parse_video_shortcode

MAX_FILES = 200
MAX_FILE_BYTES = 1_000_000
TRYIT_LANGUAGES = {"html", "css", "javascript", "js", "python", "py", "sql"}
_LANGUAGE_ALIASES = {"js": "javascript", "py": "python"}
_FENCE_INFO = re.compile(r"^\s*(`{3,}|~{3,})\s*([\w+-]*)\s*(.*)$")
_TITLE = re.compile(r"^#\s+(.+?)\s*#*\s*$")


@dataclass
class BlockDraft:
    type: str
    content_md: str = ""
    data: dict = field(default_factory=dict)


@dataclass
class LessonDraft:
    title: str
    slug: str
    summary: str
    minutes: int
    source_md: str
    blocks: list[BlockDraft]


def read_markdown_uploads(files) -> list[tuple[str, str]]:
    """(filename, text) for each uploaded .md file or .md file inside a .zip, sorted by name."""
    found = []
    for upload in files:
        name = upload.name.lower()
        if name.endswith(".zip"):
            with zipfile.ZipFile(io.BytesIO(upload.read())) as archive:
                for info in archive.infolist():
                    if info.filename.lower().endswith(".md") and not info.is_dir():
                        _check_size(info.filename, info.file_size)
                        found.append((PurePosixPath(info.filename).name, archive.read(info)))
        elif name.endswith(".md"):
            _check_size(upload.name, upload.size)
            found.append((upload.name, upload.read()))
        else:
            raise ValueError(f"{upload.name}: only .md and .zip files can be imported.")
    if not found:
        raise ValueError("No .md files found.")
    if len(found) > MAX_FILES:
        raise ValueError(f"Import at most {MAX_FILES} files at once.")
    return sorted((name, raw.decode("utf-8-sig")) for name, raw in found)


def parse_lesson_markdown(text: str, filename: str = "") -> LessonDraft:
    meta, body = _split_front_matter(text)
    title = meta.get("title", "")
    lines = body.splitlines()
    if not title:
        title, lines = _take_title(lines)
    title = title or PurePosixPath(filename).stem.replace("-", " ").replace("_", " ").title()
    return LessonDraft(
        title=title,
        slug=meta.get("slug", ""),
        summary=meta.get("summary", ""),
        minutes=int(meta["minutes"]) if meta.get("minutes", "").isdigit() else 5,
        source_md=text,
        blocks=_split_blocks(lines),
    )


def _split_front_matter(text: str) -> tuple[dict, str]:
    text = text.lstrip("﻿")
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    meta = {}
    for line in text[4:end].splitlines():
        key, sep, value = line.partition(":")
        if sep:
            meta[key.strip().lower()] = value.strip().strip("\"'")
    return meta, text[end + 4 :].lstrip("\n")


def _take_title(lines: list[str]) -> tuple[str, list[str]]:
    in_fence = False
    for i, line in enumerate(lines):
        if FENCE.match(line):
            in_fence = not in_fence
        match = None if in_fence else _TITLE.match(line)
        if match:
            return match.group(1), lines[:i] + lines[i + 1 :]
    return "", lines


def _split_blocks(lines: list[str]) -> list[BlockDraft]:
    blocks: list[BlockDraft] = []
    text: list[str] = []
    example: dict | None = None  # the try-it, exercise or quiz fence being collected
    in_fence = False

    def flush_text():
        content = "\n".join(text).strip()
        if content:
            blocks.append(BlockDraft("markdown", content))
        text.clear()

    for line in lines:
        if example is not None:
            if FENCE.match(line) and line.strip().startswith(example["fence"]):
                blocks.append(_fenced_block(example["language"], "\n".join(example["code"])))
                example = None
            else:
                example["code"].append(line)
            continue

        fence = _FENCE_INFO.match(line)
        if fence and not in_fence:
            marker, language, rest = fence.groups()
            is_tryit = "tryit" in rest.split() and language.lower() in TRYIT_LANGUAGES
            if is_tryit or language.lower() in ("exercise", "quiz"):
                flush_text()
                language = _LANGUAGE_ALIASES.get(language.lower(), language.lower())
                example = {"fence": marker, "language": language, "code": []}
                continue
        if FENCE.match(line):
            in_fence = not in_fence

        video = None if in_fence else parse_video_shortcode(line)
        if video:
            flush_text()
            blocks.append(BlockDraft("video", data={"provider": video[0], "ref": video[1]}))
        else:
            text.append(line)

    flush_text()
    return blocks


def _fenced_block(language: str, body: str) -> BlockDraft:
    if language not in ("exercise", "quiz"):
        return BlockDraft("example", data={"language": language, "code": body})
    try:
        data = json.loads(body)
    except json.JSONDecodeError as exc:
        problem = f"{exc.msg}, line {exc.lineno}"
        raise ValueError(f"The {language} block is not valid JSON ({problem}).") from exc
    if language == "quiz":
        return BlockDraft("quiz", data=data if isinstance(data, dict) else {"questions": data})
    return BlockDraft("exercise", data=data if isinstance(data, dict) else {})


def _check_size(name: str, size: int) -> None:
    if size > MAX_FILE_BYTES:
        raise ValueError(f"{name} is larger than 1 MB.")
