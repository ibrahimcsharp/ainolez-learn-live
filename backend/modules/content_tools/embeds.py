"""Video and iframe embeds. Only the hosts below may be embedded."""

import re
from html import escape
from urllib.parse import parse_qs, urlparse

ALLOWED_IFRAME_HOSTS = {
    "www.youtube-nocookie.com",
    "player.vimeo.com",
    "www.loom.com",
    "drive.google.com",
    "docs.google.com",
    "codepen.io",
    "replit.com",
}
_YOUTUBE_ID = re.compile(r"^[A-Za-z0-9_-]{6,20}$")


def is_allowed_iframe(src: str) -> bool:
    url = urlparse(src)
    return url.scheme == "https" and url.hostname in ALLOWED_IFRAME_HOSTS


def parse_video(value: str, provider: str = "") -> tuple[str, str] | None:
    """Turn a video URL (or a bare id plus provider) into (provider, ref). None if unknown."""
    value = value.strip()
    if provider == "youtube" and _YOUTUBE_ID.match(value):
        return "youtube", value
    if provider == "vimeo" and value.isdigit():
        return "vimeo", value

    url = urlparse(value)
    host = (url.hostname or "").removeprefix("www.").removeprefix("m.")
    parts = [p for p in url.path.split("/") if p]
    if host == "youtu.be" and parts:
        return _youtube(parts[0])
    if host in ("youtube.com", "youtube-nocookie.com"):
        if parts[:1] == ["watch"]:
            return _youtube(parse_qs(url.query).get("v", [""])[0])
        if len(parts) >= 2 and parts[0] in ("embed", "shorts", "live"):
            return _youtube(parts[1])
    if host in ("vimeo.com", "player.vimeo.com") and parts and parts[-1].isdigit():
        return "vimeo", parts[-1]
    if host == "loom.com" and len(parts) >= 2 and parts[0] in ("share", "embed"):
        return "loom", parts[1]
    if host == "drive.google.com" and len(parts) >= 3 and parts[:2] == ["file", "d"]:
        return "drive", parts[2]
    if url.scheme == "https" and url.path.lower().endswith((".mp4", ".webm")):
        return "file", value
    return None


def video_html(provider: str, ref: str, start: int = 0, caption: str = "") -> str:
    if provider == "file":
        player = f'<video src="{escape(ref)}" controls preload="metadata"></video>'
    else:
        src = {
            "youtube": f"https://www.youtube-nocookie.com/embed/{ref}?start={start}",
            "vimeo": f"https://player.vimeo.com/video/{ref}#t={start}s",
            "loom": f"https://www.loom.com/embed/{ref}",
            "drive": f"https://drive.google.com/file/d/{ref}/preview",
        }[provider]
        player = (
            f'<iframe src="{escape(src)}" title="{escape(caption or "Video")}" loading="lazy" '
            'allow="accelerometer; encrypted-media; picture-in-picture" allowfullscreen></iframe>'
        )
    figcaption = f"<figcaption>{escape(caption)}</figcaption>" if caption else ""
    return f'<figure class="video"><div class="media-frame">{player}</div>{figcaption}</figure>'


def embed_html(src: str, title: str = "") -> str:
    if not is_allowed_iframe(src):
        raise ValueError("This site cannot be embedded.")
    return (
        f'<div class="media-frame"><iframe src="{escape(src)}" title="{escape(title or "Embed")}" '
        'loading="lazy" allowfullscreen></iframe></div>'
    )


def _youtube(video_id: str) -> tuple[str, str] | None:
    return ("youtube", video_id) if _YOUTUBE_ID.match(video_id) else None
