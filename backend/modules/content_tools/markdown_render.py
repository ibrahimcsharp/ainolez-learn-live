"""Markdown -> safe HTML, with ainolez shortcodes such as {{youtube:ID}} and video timestamps."""

import re
from html import escape

import markdown

from modules.content_tools.embeds import parse_video, video_html
from modules.content_tools.sanitizer import sanitize

EXTENSIONS = ["fenced_code", "tables", "toc", "admonition", "sane_lists"]
FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
VIDEO_SHORTCODE = re.compile(r"^\{\{(youtube|vimeo|video):\s*(\S+?)\s*\}\}$")
# "00:40 | IDE Choice", "1:02:03 - Wrap up", "- 05:10 Testing" (as written under YouTube videos)
TIMESTAMP = re.compile(
    r"^\s*(?:[-*]\s+)?((?:\d{1,2}:)?\d{1,2}:[0-5]\d)\s*(?:[|\-–—:.)]\s*)?(\S.*)$"
)
# A line above the timestamps becomes their title unless it is Markdown of its own.
NOT_A_TITLE = re.compile(r"^\s*(#|\||[-*+>]\s|\d+\.\s|\{\{|!!!|<)")


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
    """Replace shortcode lines with embed HTML and runs of timestamp lines with a chapter
    list, but never inside fenced code."""
    source = text.splitlines()
    lines, in_fence, video, i = [], False, None, 0
    while i < len(source):
        line = source[i]
        if FENCE.match(line):
            in_fence = not in_fence
        if in_fence:
            lines.append(line)
            i += 1
            continue
        shortcode = parse_video_shortcode(line)
        if shortcode:
            video = shortcode
            lines.append(f"\n{video_html(*shortcode)}\n")
            i += 1
            continue
        run = []
        while i + len(run) < len(source) and (match := TIMESTAMP.match(source[i + len(run)])):
            run.append(match.groups())
        if len(run) >= 2:  # a single time on its own stays ordinary text
            title = ""
            if lines and lines[-1].strip() and not NOT_A_TITLE.match(lines[-1]):
                title = lines.pop().strip()
            lines.append(f"\n{timestamps_html(run, video, title)}\n")
            i += len(run)
            continue
        lines.append(line)
        i += 1
    return "\n".join(lines)


def seconds(stamp: str) -> int:
    """'1:02:03' -> 3723, '00:40' -> 40."""
    total = 0
    for part in stamp.split(":"):
        total = total * 60 + int(part)
    return total


def timestamps_html(items, video: tuple[str, str] | None, title: str = "") -> str:
    """Video chapters. Each time links to that moment of the video above it; on the site a
    click moves the embedded player instead (frontend shared/ui/timestamps.js)."""
    rows = "".join(
        f'<li><a class="timestamp" href="{escape(_moment_url(video, seconds(stamp)))}">'
        f"{escape(stamp)}</a> <span>{escape(label.strip())}</span></li>"
        for stamp, label in items
    )
    heading = f'<p class="timestamps-title">{escape(title)}</p>' if title else ""
    return f'<div class="timestamps">{heading}<ol>{rows}</ol></div>'


def _moment_url(video: tuple[str, str] | None, at: int) -> str:
    provider, ref = video or ("", "")
    if provider == "youtube":
        return f"https://www.youtube.com/watch?v={ref}&t={at}s"
    if provider == "vimeo":
        return f"https://vimeo.com/{ref}#t={at}s"
    return f"#t={at}"  # the video is in another block: the page finds the player above
