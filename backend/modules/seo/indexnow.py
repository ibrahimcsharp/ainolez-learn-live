"""
IndexNow (https://www.indexnow.org): after a build, tell Bing, Yandex, Seznam and others
which pages changed, so they crawl them in minutes instead of days. Google does not take
part; it reads the sitemap. The key is published at /<key>.txt by the build.
"""

import json
import logging
import secrets
import urllib.error
import urllib.request
from urllib.parse import urlparse

from django.conf import settings

logger = logging.getLogger(__name__)

ENDPOINT = "https://api.indexnow.org/indexnow"
LIMIT = 10_000  # URLs per request


def new_key() -> str:
    return secrets.token_hex(16)


def site_host() -> str:
    return urlparse(settings.FRONTEND_URL).hostname or ""


def is_public_site() -> bool:
    host = site_host()
    return bool(host) and host not in ("localhost", "127.0.0.1") and "." in host


def submit(key: str, urls: list[str]) -> str:
    """Send `urls`; returns a short result for the admin."""
    if not urls:
        return "No changed pages to send."
    if not is_public_site():
        return "Skipped: FRONTEND_URL is not a public address."
    host = site_host()
    body = {
        "host": host,
        "key": key,
        "keyLocation": f"{settings.FRONTEND_URL.rstrip('/')}/{key}.txt",
        "urlList": urls[:LIMIT],
    }
    try:
        status = send(body)
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        logger.warning("IndexNow failed: %s", exc)
        return f"Failed: {exc}"[:300]
    if status in (200, 202):
        return f"Sent {len(body['urlList'])} changed pages (HTTP {status})."
    return f"IndexNow answered HTTP {status}. Check the key file is online."


def send(body: dict) -> int:
    """POST the JSON body; returns the HTTP status. Tests replace this."""
    request = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            return response.status
    except urllib.error.HTTPError as exc:
        return exc.code
