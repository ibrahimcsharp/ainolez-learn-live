"""Read queries of the seo module (admin screens and analytics)."""

from collections import Counter
from datetime import timedelta

from django.db.models import Sum
from django.utils import timezone

from modules.catalog import selectors as catalog
from modules.seo import prerender, resolver
from modules.seo.models import PageViewDaily, SeoPage
from modules.website import selectors as website

TITLE_MAX, DESCRIPTION_MIN, DESCRIPTION_MAX = 60, 50, 160


def page_urls(pages: list[SeoPage]) -> dict[int, str]:
    """{seo_page id: URL} for the admin list; entity rows get their item's current URL."""
    urls = {p.pk: p.path for p in pages if p.path}
    for kind in ("course", "lesson"):
        ids = {p.entity_id for p in pages if p.entity_type == kind}
        found = catalog.page_urls(kind, ids) if ids else {}
        urls |= {p.pk: found.get(p.entity_id, "") for p in pages if p.entity_type == kind}
    urls |= {p.pk: f"/community/posts/{p.entity_id}" for p in pages if p.entity_type == "post"}
    page_ids = {p.entity_id for p in pages if p.entity_type == "page"}
    found = website.page_urls(page_ids) if page_ids else {}
    urls |= {p.pk: found.get(p.entity_id, "") for p in pages if p.entity_type == "page"}
    return urls


def seo_report() -> dict:
    """Every public page with the problems a search engine would mind."""
    site = resolver.settings_row()
    pages = [resolver.resolve(path, site) for path in prerender.public_paths()]
    titles = Counter(meta.title for meta in pages if meta.indexable)
    rows = []
    for meta in pages:
        issues = []
        if meta.status != 200:
            issues.append("Not public (draft, hidden or missing)")
        elif meta.indexable:
            if len(meta.title) > TITLE_MAX:
                issues.append(f"Title is longer than {TITLE_MAX} characters")
            if titles[meta.title] > 1:
                issues.append("Another page has the same title")
            if not meta.description:
                issues.append("No description")
            elif not DESCRIPTION_MIN <= len(meta.description) <= DESCRIPTION_MAX:
                issues.append(
                    f"Description should be {DESCRIPTION_MIN}–{DESCRIPTION_MAX} characters"
                )
            if not meta.image:
                issues.append("No share image")
        rows.append({
            "path": meta.path,
            "title": meta.title,
            "description": meta.description,
            "robots": meta.robots,
            "in_sitemap": meta.indexable and meta.in_sitemap,
            "customised": meta.page_id is not None,
            "issues": issues,
        })  # fmt: skip
    return {
        "allow_indexing": site.allow_indexing,
        "last_build_at": site.last_build_at,
        "last_build_pages": site.last_build_pages,
        "robots_txt": prerender.robots_txt(site),
        "pages": rows,
    }


def views_by_day(days: int) -> dict[str, int]:
    since = timezone.now().date() - timedelta(days=days - 1)
    rows = (
        PageViewDaily.objects.filter(day__gte=since)
        .values("day")
        .annotate(total=Sum("views"))
        .order_by("day")
    )
    return {row["day"].isoformat(): row["total"] for row in rows}


def top_pages(days: int, limit: int = 20) -> list[dict]:
    since = timezone.now().date() - timedelta(days=days - 1)
    rows = (
        PageViewDaily.objects.filter(day__gte=since)
        .values("path")
        .annotate(views=Sum("views"))
        .order_by("-views")[:limit]
    )
    return [{"path": row["path"], "views": row["views"]} for row in rows]
