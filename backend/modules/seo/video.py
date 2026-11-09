"""
Video key moments: schema.org VideoObject (with a Clip per timestamp) for each
YouTube video in a page's HTML. The timestamps are the "00:40 | IDE Choice" lines
that content_tools renders as <a class="timestamp">, under the video they belong to.
Google can then show the chapters as "key moments" in search results.
"""

import re
from datetime import datetime
from html import unescape

TOKENS = re.compile(
    r'<iframe[^>]*\ssrc="https://www\.youtube-nocookie\.com/embed/([A-Za-z0-9_-]{6,20})'
    r'|<a[^>]*class="timestamp"[^>]*href="([^"]*)"[^>]*>[^<]*</a>\s*<span>([^<]*)</span>'
)
SECONDS = re.compile(r"[?&#]t=(\d+)")


def videos(html: str) -> list[dict]:
    """[{"id": youtube id, "clips": [(seconds, name), ...]}] in page order."""
    found: list[dict] = []
    for match in TOKENS.finditer(html or ""):
        video_id, href, label = match.groups()
        if video_id:
            found.append({"id": video_id, "clips": []})
        elif found and (at := SECONDS.search(unescape(href))):
            found[-1]["clips"].append((int(at[1]), unescape(label).strip()))
    return found


def video_objects(
    html: str, page_url: str, name: str, description: str, updated_at: datetime | None
) -> list[dict]:
    items = []
    found = videos(html)
    for number, video in enumerate(found, start=1):
        data = {
            "@context": "https://schema.org",
            "@type": "VideoObject",
            "name": name if len(found) == 1 else f"{name} (video {number})",
            "description": description or name,
            "thumbnailUrl": [f"https://i.ytimg.com/vi/{video['id']}/hqdefault.jpg"],
            "embedUrl": f"https://www.youtube.com/embed/{video['id']}",
        }
        if updated_at:
            data["uploadDate"] = updated_at.isoformat()
        clips = sorted(video["clips"])
        if len(clips) >= 2:
            data["hasPart"] = [
                {
                    "@type": "Clip",
                    "name": label or f"Part {i}",
                    "startOffset": start,
                    **({"endOffset": clips[i][0]} if i < len(clips) else {}),
                    "url": f"{page_url}?t={start}",  # the page jumps the video there
                }
                for i, (start, label) in enumerate(clips, start=1)
            ]
        items.append(data)
    return items
