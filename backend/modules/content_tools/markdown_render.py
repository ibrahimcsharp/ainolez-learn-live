"""Markdown -> safe HTML, with ainolez shortcodes such as {{youtube:ID}}."""

import re

import markdown

from modules.content_tools.embeds import parse_video, video_html
from modules.content_tools.sanitizer import sanitize

EXTENSIONS = ["fenced_code", "tables", "toc", "admonition", "sane_lists"]
FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
VIDEO_SHORTCODE = re.compile(r"^\{\{(youtube|vimeo|video):\s*(\S+?)\s*\}\}$")


def parse_video_shortcode(line: str) -> tuple[str, str] | None:
    """'{{youtube:abc123XYZ}}' -> ('youtube', 'abc123XYZ'). None if not a valid shortcode."""
    match = VIDEO_SHORTCODE.match(line.strip())
    if not match:
        return None
    kind, value = match.groups()
    return parse_video(value, provider="" if kind == "video" else kind)


def render_markdown(text: str) -> str:
    html = markdown.markdown(_expand_shortcodes(text or ""), extensions=EXTENSIONS)
    return sanitize(html)


def _expand_shortcodes(text: str) -> str:
    """Replace shortcode lines with embed HTML, but never inside fenced code."""
    lines, in_fence = [], False
    for line in text.splitlines():
        if FENCE.match(line):
            in_fence = not in_fence
        video = None if in_fence else parse_video_shortcode(line)
        lines.append(f"\n{video_html(*video)}\n" if video else line)
    return "\n".join(lines)
