"""
Works out every SEO tag of a page. The first value that is set wins:

    1. the page's seo_pages row (what the admin typed)
    2. the content (course title, lesson summary, certificate image...)
    3. seo_settings (site-wide defaults)

The same result feeds the website (`/api/v1/public/seo/?path=`) and the
prerendered HTML files, so both always show the same tags.
"""

import re
from dataclasses import dataclass, field

from django.utils.html import escape

from modules.seo import content
from modules.seo.models import SeoPage, SeoSettings

SAFE_PATH = re.compile(r"^/[a-z0-9/-]*$")  # paths the admin may add, and file names
PRIVATE = {"/admin": "Admin panel", "/dashboard": "My dashboard"}
NOINDEX = "noindex,nofollow"


@dataclass
class PageMeta:
    path: str
    status: int  # 200, or 404 when nothing lives at this path
    title: str
    description: str = ""
    keywords: str = ""
    robots: str = "index,follow"
    canonical: str = ""
    image: str = ""
    og_type: str = "website"
    og_title: str = ""
    og_description: str = ""
    twitter_card: str = "summary"
    json_ld: list[dict] = field(default_factory=list)
    body_html: str = ""
    in_sitemap: bool = False
    sitemap_priority: str | None = None
    sitemap_changefreq: str | None = None
    lastmod: str | None = None  # ISO date for the sitemap
    page_id: int | None = None  # the seo_pages row used, if any
    entity: tuple[str, int] | None = None

    @property
    def indexable(self) -> bool:
        return self.status == 200 and not self.robots.startswith("noindex")


def settings_row() -> SeoSettings:
    return SeoSettings.objects.get(pk=1)


def normalize(path: str) -> str:
    path = "/" + (path or "").split("?")[0].split("#")[0].strip().strip("/")
    return path[:255]


def is_private(path: str) -> bool:
    return "/" + path.split("/")[1] in PRIVATE


def resolve(path: str, site: SeoSettings | None = None) -> PageMeta:
    site = site or settings_row()
    path = normalize(path)
    if is_private(path):
        name = PRIVATE["/" + path.split("/")[1]]
        return PageMeta(path=path, status=200, title=_titled(site, name), robots=NOINDEX)

    rows = SeoPage.objects.filter(is_active=True)
    row = rows.filter(path=path).first()
    found = content.for_path(path, site)
    if row is None and found and found.entity:
        kind, entity_id = found.entity
        row = rows.filter(entity_type=kind, entity_id=entity_id).first()
    if row is None and found is None:
        return PageMeta(
            path=path, status=404, title=_titled(site, "Page not found"), robots=NOINDEX
        )
    return _merge(path, site, row, found)


def automatic(path: str, site: SeoSettings) -> PageMeta:
    """The values a page gets with no seo_pages row: hints in the admin form."""
    path = normalize(path)
    return _merge(path, site, None, content.for_path(path, site))


def _merge(path: str, site: SeoSettings, row: SeoPage | None, found) -> PageMeta:
    row = row or SeoPage()  # an empty row: everything automatic
    name = found.name if found else site.site_name
    title = row.meta_title or _titled(site, name)
    description = row.meta_description or (found and found.description) or site.default_description
    robots = row.robots or (found and found.robots) or "index,follow"
    image = content.absolute(row.og_image_url or (found and found.image) or site.default_image_url)
    extra = row.structured_data or []
    return PageMeta(
        path=path,
        status=200,
        title=title,
        description=description,
        keywords=row.keywords or site.default_keywords,
        robots=robots if site.allow_indexing else NOINDEX,
        canonical=row.canonical_url or content.absolute(path),
        image=image,
        og_type=row.og_type or (found.og_type if found else "website"),
        og_title=row.og_title or title,
        og_description=row.og_description or description,
        twitter_card=row.twitter_card or ("summary_large_image" if image else "summary"),
        json_ld=(found.json_ld if found else []) + (extra if isinstance(extra, list) else [extra]),
        body_html=(
            found.body_html if found and found.body_html else _plain_body(title, description)
        ),
        in_sitemap=row.in_sitemap,
        sitemap_priority=str(row.sitemap_priority) if row.sitemap_priority is not None else None,
        sitemap_changefreq=row.sitemap_changefreq,
        lastmod=found.updated_at.date().isoformat() if found and found.updated_at else None,
        page_id=row.pk,
        entity=found.entity if found else None,
    )


def head_tags(meta: PageMeta, site: SeoSettings) -> list[dict]:
    """The <meta>/<link> tags of a page, as {"tag", attribute: value...} dicts."""
    tags = [
        {"tag": "meta", "name": "description", "content": meta.description},
        {"tag": "meta", "name": "keywords", "content": meta.keywords},
        {"tag": "meta", "name": "robots", "content": meta.robots},
        {"tag": "link", "rel": "canonical", "href": meta.canonical},
        {"tag": "meta", "property": "og:site_name", "content": site.site_name},
        {"tag": "meta", "property": "og:locale", "content": site.locale},
        {"tag": "meta", "property": "og:type", "content": meta.og_type},
        {"tag": "meta", "property": "og:title", "content": meta.og_title},
        {"tag": "meta", "property": "og:description", "content": meta.og_description},
        {"tag": "meta", "property": "og:url", "content": meta.canonical},
        {"tag": "meta", "property": "og:image", "content": meta.image},
        {"tag": "meta", "property": "fb:app_id", "content": site.facebook_app_id},
        {"tag": "meta", "name": "twitter:card", "content": meta.twitter_card},
        {"tag": "meta", "name": "twitter:site", "content": site.twitter_site},
        {"tag": "meta", "name": "twitter:title", "content": meta.og_title},
        {"tag": "meta", "name": "twitter:description", "content": meta.og_description},
        {"tag": "meta", "name": "twitter:image", "content": meta.image},
        {
            "tag": "meta",
            "name": "google-site-verification",
            "content": site.google_site_verification,
        },
        {"tag": "meta", "name": "msvalidate.01", "content": site.bing_site_verification},
    ]
    if meta.status != 200:
        tags = [t for t in tags if t.get("name") == "robots"]
    return [t for t in tags if t.get("content") or t.get("href")]


def _titled(site: SeoSettings, name: str) -> str:
    if name == site.site_name or "{title}" not in site.title_template:
        return name
    return site.title_template.replace("{title}", name)


def _plain_body(title: str, description: str) -> str:
    return f"<h1>{escape(title)}</h1><p>{escape(description)}</p>"
