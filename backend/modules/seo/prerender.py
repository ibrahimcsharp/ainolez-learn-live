"""
Writes the public website's SEO files into PRERENDER_DIR (public_html on cPanel):

    index.html, python/index.html, python/lists/index.html ...   one per page
    sitemap.xml, robots.txt
    data/...        copies of the public API's answers for those pages (see write_data)

Each HTML file is the app's shell.html (the React build) with the page's
title, meta tags, JSON-LD and a plain copy of its content, so search engines
and link previews (LinkedIn, X, WhatsApp) see real content without running
JavaScript. Apache serves the file; React then starts and takes over.
"""

import json
import logging
import re
import shutil
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

from django.conf import settings
from django.test import RequestFactory
from django.urls import resolve
from django.utils import timezone
from django.utils.html import escape

from modules.catalog import selectors as catalog
from modules.community import selectors as community
from modules.seo import resolver
from modules.seo.models import SeoPage, SeoSettings
from modules.website import selectors as website
from shared.exceptions import ServiceError

logger = logging.getLogger(__name__)

SHELL = "shell.html"
MANIFEST = ".prerendered.json"  # files written last time, so stale ones can be removed


def public_paths() -> list[str]:
    fixed = SeoPage.objects.filter(path__isnull=False, is_active=True).values_list(
        "path", flat=True
    )
    content = [
        *(p["url"] for p in catalog.sitemap_pages()),
        *(p["url"] for p in website.sitemap_pages()),
        *(p["url"] for p in community.sitemap_posts()),
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
    menus = website.public_menus()
    pages = [resolver.resolve(path, site) for path in public_paths()]

    written = []
    for meta in pages:
        if meta.status == 200 and resolver.SAFE_PATH.match(meta.path):
            relative = "index.html" if meta.path == "/" else f"{meta.path.strip('/')}/index.html"
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(render(shell, meta, site, menus), encoding="utf-8")
            written.append(relative)
    _remove_stale(root, set(written))
    (root / "sitemap.xml").write_text(sitemap(pages, site), encoding="utf-8")
    (root / "robots.txt").write_text(robots_txt(site), encoding="utf-8")
    write_data(root, pages)

    site.last_build_at = timezone.now()
    site.last_build_pages = len(written)
    site.save(update_fields=["last_build_at", "last_build_pages"])
    logger.info("SEO build wrote %s pages", len(written))
    return len(written)


DATA = "data"
API = "/api/v1/public"


def write_data(root: Path, pages: list[resolver.PageMeta]) -> None:
    """Copies of the public API answers the website needs, as static files:
    /public/courses/python/ -> data/courses/python.json, and so on. The website reads
    them first (the web server sends a file at once; the API has to start Python),
    and asks the API only when a file is missing. The frontend's staticCopy() in
    shared/api/client.js maps paths the same way. The folder is replaced whole, so
    removed courses and pages disappear."""
    paths = ["/catalog/", "/site/menus/"]
    for meta in pages:
        if meta.status != 200 or not meta.entity:
            continue
        kind, parts = meta.entity[0], meta.path.strip("/").split("/")
        if kind == "course" and len(parts) == 1:
            paths.append(f"/courses/{parts[0]}/")
        elif kind == "lesson" and len(parts) == 2:
            paths.append(f"/courses/{parts[0]}/lessons/{parts[1]}/")
        elif kind == "page" and len(parts) == 1:
            paths.append(f"/site/pages/{parts[0]}/")

    fresh, current, old = root / f"{DATA}.new", root / DATA, root / f"{DATA}.old"
    shutil.rmtree(fresh, ignore_errors=True)
    for path in paths:
        data = _public_get(path)
        if data is not None:
            target = fresh / f"{path.strip('/')}.json"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(data, encoding="utf-8")
    shutil.rmtree(old, ignore_errors=True)
    if current.exists():
        current.rename(old)
    fresh.rename(current)
    shutil.rmtree(old, ignore_errors=True)
    (root / "catalog.json").unlink(missing_ok=True)  # where the catalog used to be written


def _public_get(path: str) -> str | None:
    """The JSON a GET of the public API returns, made in this process (no HTTP)."""
    host = next((h.lstrip(".") for h in settings.ALLOWED_HOSTS if h != "*"), "localhost")
    url = API + path
    match = resolve(url)
    view = match.func.cls.as_view(throttle_classes=[])  # a build is not a visitor
    response = view(RequestFactory().get(url, HTTP_HOST=host), *match.args, **match.kwargs)
    response.render()
    if response.status_code != 200:
        logger.warning("SEO build: %s answered %s", url, response.status_code)
        return None
    return response.content.decode("utf-8")


def render(
    shell: str, meta: resolver.PageMeta, site: SeoSettings, menus: dict | None = None
) -> str:
    head = "\n".join(
        [f"<title>{escape(meta.title)}</title>"]
        + [tag_html(tag) for tag in resolver.head_tags(meta, site)]
        + [
            f'<script type="application/ld+json" data-seo>{_json(data)}</script>'
            for data in meta.json_ld
        ]
        # The header and footer links, so the app draws them on first paint. MenuChanged
        # rebuilds the files. A JSON script never runs, so the strict CSP allows it.
        + (
            [f'<script type="application/json" id="site-menus">{_json(menus)}</script>']
            if menus
            else []
        )
    )
    html = re.sub(r"\s*<title>.*?</title>", "", shell, flags=re.S)
    html = re.sub(r'\s*<meta\s+name="description"[^>]*>', "", html, flags=re.S)
    html = html.replace("</head>", f"{head}\n</head>", 1)
    return html.replace('<div id="root"></div>', f'<div id="root">{meta.body_html}</div>', 1)


def _json(data) -> str:
    """JSON that is safe inside a <script> element."""
    return json.dumps(data, ensure_ascii=False).replace("</", "<\\/")


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
