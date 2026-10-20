"""Public API of content_tools: Markdown rendering, embeds and the .md importer."""

from html import escape

from modules.content_tools.embeds import embed_html, parse_video, video_html
from modules.content_tools.importer import (
    BlockDraft,
    LessonDraft,
    parse_lesson_markdown,
    read_markdown_uploads,
)
from modules.content_tools.markdown_render import render_markdown
from modules.content_tools.sanitizer import sanitize
from shared.exceptions import ServiceError

CALLOUT_KINDS = ("note", "tip", "warning", "example")

__all__ = [
    "BlockDraft",
    "LessonDraft",
    "callout_html",
    "embed_block_html",
    "image_html",
    "normalize_video",
    "import_markdown_files",
    "parse_lesson_markdown",
    "parse_video",
    "render_markdown",
    "video_block_html",
]


def callout_html(kind: str, text: str) -> str:
    kind = kind if kind in CALLOUT_KINDS else "note"
    return f'<div class="callout callout-{kind}">{render_markdown(text)}</div>'


def normalize_video(data: dict) -> dict:
    """Accept {url} or {provider, ref}; return {provider, ref, start, caption}."""
    video = parse_video(data.get("url") or data.get("ref", ""), data.get("provider", ""))
    if video is None:
        raise ServiceError("Use a YouTube, Vimeo, Loom, Google Drive or .mp4 link.", "bad_video")
    return {
        "provider": video[0],
        "ref": video[1],
        "start": int(data.get("start") or 0),
        "caption": data.get("caption", ""),
    }


def video_block_html(data: dict) -> str:
    """``data`` as returned by normalize_video."""
    return video_html(data["provider"], data["ref"], data["start"], data["caption"])


def embed_block_html(data: dict) -> str:
    try:
        return embed_html(data.get("url", ""), data.get("title", ""))
    except ValueError as exc:
        raise ServiceError(str(exc), "embed_not_allowed") from exc


def image_html(url: str, alt: str, caption: str = "") -> str:
    figcaption = f"<figcaption>{escape(caption)}</figcaption>" if caption else ""
    return sanitize(
        f'<figure><img src="{escape(url)}" alt="{escape(alt)}" loading="lazy">{figcaption}</figure>'
    )


def import_markdown_files(files) -> list[LessonDraft]:
    """Read uploaded .md / .zip files into lesson drafts, ordered by file name."""
    try:
        return [parse_lesson_markdown(text, name) for name, text in read_markdown_uploads(files)]
    except (ValueError, UnicodeDecodeError) as exc:
        raise ServiceError(f"Import failed: {exc}", "bad_import") from exc
