"""
Writes the public website's SEO files into PRERENDER_DIR (public_html on cPanel):

    index.html, python/index.html, python/lists/index.html ...   one per page
    sitemap.xml, robots.txt

Each HTML file is the app's shell.html (the React build) with the page's
title, meta tags, JSON-LD and a plain copy of its content, so search engines
and link previews (LinkedIn, X, WhatsApp) see real content without running
JavaScript. Apache serves the file; React then starts and takes over.
"""

import json
import logging
import re
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

from django.conf import settings
from django.utils import timezone
from django.utils.html import escape

from modules.catalog import selectors as catalog
from modules.community import selectors as community
from modules.seo import resolver
from modules.seo.models import SeoPage, SeoSettings
from shared.exceptions import ServiceError

logger = logging.getLogger(__name__)

SHELL = "shell.html"
MANIFEST = ".prerendered.json"  # files written last time, so stale ones can be removed


def public_paths() -> list[str]:
    fixed = SeoPage.objects.filter(path__isnull=False, is_active=True).values_list(
        "path", flat=True
    )
    content = [p["url"] for p in catalog.sitemap_pages()] + [
        p["url"] for p in community.sitemap_posts()
    ]
    return list(dict.fromkeys([*fixed, *content]))


def build() -> int:
    """Rebuild every file. Returns how many pages were written."""
    if not settings.PRERENDER_DIR:
        raise ServiceError("Set PRERENDER_DIR in .env to the website folder first.", "no_target")
    root = Path(settings.PRERENDER_DIR)
    if not (root / SHELL).exists():
        raise ServiceError(
            f"{root / SHELL} is missing. Upload the website build first.", "no_shell"
        )
    shell = (root / SHELL).read_text(encoding="utf-8")
    site = resolver.settings_row()
    pages = [resolver.resolve(path, site) for path in public_paths()]

    written = []
    for meta in pages:
        if meta.status == 200 and resolver.SAFE_PATH.match(meta.path):
            relative = "index.html" if meta.path == "/" else f"{meta.path.strip('/')}/index.html"
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(render(shell, meta, site), encoding="utf-8")
            written.append(relative)
    _remove_stale(root, set(written))
    (root / "sitemap.xml").write_text(sitemap(pages, site), encoding="utf-8")
    (root / "robots.txt").write_text(robots_txt(site), encoding="utf-8")

    site.last_build_at = timezone.now()
    site.last_build_pages = len(written)
    site.save(update_fields=["last_build_at", "last_build_pages"])
    logger.info("SEO build wrote %s pages", len(written))
    return len(written)


def render(shell: str, meta: resolver.PageMeta, site: SeoSettings) -> str:
    head = "\n".join(
        [f"<title>{escape(meta.title)}</title>"]
        + [tag_html(tag) for tag in resolver.head_tags(meta, site)]
        + [
            '<script type="application/ld+json" data-seo>'
            + json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
            + "</script>"
            for data in meta.json_ld
        ]
    )
    html = re.sub(r"\s*<title>.*?</title>", "", shell, flags=re.S)
    html = re.sub(r'\s*<meta\s+name="description"[^>]*>', "", html, flags=re.S)
    html = html.replace("</head>", f"{head}\n</head>", 1)
    return html.replace('<div id="root"></div>', f'<div id="root">{meta.body_html}</div>', 1)


def tag_html(tag: dict) -> str:
    attributes = " ".join(f'{key}="{escape(value)}"' for key, value in tag.items() if key != "tag")
    return f"<{tag['tag']} {attributes} data-seo>"


def sitemap(pages: list[resolver.PageMeta], site: SeoSettings) -> str:
    entries = []
    for meta in pages:
        if not (site.allow_indexing and meta.indexable and meta.in_sitemap):
            continue
        parts = [f"<loc>{xml_escape(meta.canonical)}</loc>"]
        if meta.lastmod:
            parts.append(f"<lastmod>{meta.lastmod}</lastmod>")
        if meta.sitemap_changefreq:
            parts.append(f"<changefreq>{meta.sitemap_changefreq}</changefreq>")
        if meta.sitemap_priority:
            parts.append(f"<priority>{meta.sitemap_priority}</priority>")
        entries.append(f"  <url>{''.join(parts)}</url>")
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(entries)
        + "\n</urlset>\n"
    )


def robots_txt(site: SeoSettings) -> str:
    if not site.allow_indexing:
        return "User-agent: *\nDisallow: /\n"
    lines = ["User-agent: *", "Disallow: /admin", "Disallow: /dashboard"]
    if site.robots_txt_extra and site.robots_txt_extra.strip():
        lines += ["", site.robots_txt_extra.strip()]
    lines += ["", f"Sitemap: {settings.FRONTEND_URL.rstrip('/')}/sitemap.xml"]
    return "\n".join(lines) + "\n"


def _remove_stale(root: Path, written: set[str]) -> None:
    manifest = root / MANIFEST
    previous = set(json.loads(manifest.read_text())) if manifest.exists() else set()
    for relative in previous - written:
        file = root / relative
        if file.exists():
            file.unlink()
        folder = file.parent
        while folder != root and folder.exists() and not any(folder.iterdir()):
            folder.rmdir()
            folder = folder.parent
    manifest.write_text(json.dumps(sorted(written)))
