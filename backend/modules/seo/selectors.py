"""Read queries of the seo module (admin screens and analytics)."""

from collections import Counter
from datetime import timedelta

from django.db.models import Sum
from django.utils import timezone

from modules.catalog import selectors as catalog
from modules.seo import changes, geo, prerender, resolver
from modules.seo.models import AiBot, PageViewDaily, ReferralVisitDaily, SeoChangeLog, SeoPage
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


# --- SEO & GEO Center ------------------------------------------------------------

NOT_PUBLIC = "Not public (draft, hidden or missing)"


def site_checks(site) -> list[dict]:
    """Site-wide SEO basics, in the same shape as geo.checks."""
    built = site.last_build_at and site.last_build_at > timezone.now() - timedelta(days=2)
    return [
        {"key": "indexing", "ok": site.allow_indexing, "label": "Search engines may index the site",
         "tip": "Turn on 'Let search engines index the site' (off only on staging).",
         "fix": "allow_indexing"},
        {"key": "build", "ok": bool(built), "label": "Pages and sitemap built in the last 2 days",
         "tip": "Press 'Rebuild now'. Builds also run after edits and every night.", "fix": ""},
        {"key": "google", "ok": bool(site.google_site_verification),
         "label": "Google Search Console verified",
         "tip": "Add the HTML tag code from Search Console in Site defaults, then submit "
         "/sitemap.xml there.", "fix": ""},
        {"key": "bing", "ok": bool(site.bing_site_verification),
         "label": "Bing Webmaster Tools verified",
         "tip": "Bing powers ChatGPT search and Copilot. Add its code in Site defaults.",
         "fix": ""},
        {"key": "image", "ok": bool(site.default_image_url), "label": "Default share image",
         "tip": "Pages without their own image use it on LinkedIn, X and WhatsApp.", "fix": ""},
        {"key": "description", "ok": bool(site.default_description),
         "label": "Default description", "tip": "Used by pages that have none.", "fix": ""},
    ]  # fmt: skip


def overview(days: int = 30) -> dict:
    site = resolver.settings_row()
    report = seo_report()
    public = [row for row in report["pages"] if NOT_PUBLIC not in row["issues"]]
    indexable = [row for row in public if row["robots"].startswith("index")]
    clean = [row for row in indexable if not row["issues"]]
    seo_site = site_checks(site)
    page_part = len(clean) / len(indexable) if indexable else 1
    site_part = sum(c["ok"] for c in seo_site) / len(seo_site)
    geo_checks = geo.checks(site)

    issues = Counter(issue for row in indexable for issue in row["issues"])
    fix_next = [
        {"kind": "seo", "label": c["label"], "tip": c["tip"], "fix": c["fix"], "count": None}
        for c in seo_site
        if not c["ok"]
    ]
    fix_next += [
        {"kind": "geo", "label": c["label"], "tip": c["tip"], "fix": c["fix"], "count": None}
        for c in geo_checks
        if not c["ok"]
    ]
    fix_next += [
        {"kind": "page", "label": issue, "tip": "Open the SEO report to fix these pages.",
         "fix": "", "count": count}
        for issue, count in issues.most_common()
    ]  # fmt: skip

    return {
        "seo": {
            "score": round(100 * (page_part * 0.7 + site_part * 0.3)),
            "pages": len(indexable),
            "pages_ok": len(clean),
            "checks": seo_site,
        },
        "geo": {
            "score": round(100 * sum(c["ok"] for c in geo_checks) / len(geo_checks)),
            "checks": geo_checks,
        },
        "fix_next": fix_next,
        "traffic": traffic(days),
        "build": {
            "last_build_at": site.last_build_at,
            "pages": site.last_build_pages,
            "llms": site.geo_llms_enabled,
            "markdown": site.geo_markdown_copies,
            "indexnow_enabled": site.indexnow_enabled,
            "indexnow_last_at": site.indexnow_last_at,
            "indexnow_last_result": site.indexnow_last_result,
        },
        "recent_changes": change_rows(SeoChangeLog.objects.order_by("-id")[:8]),
        "days": days,
    }


def traffic(days: int) -> dict:
    since = timezone.now().date() - timedelta(days=days - 1)
    rows = ReferralVisitDaily.objects.filter(day__gte=since)
    by_day: dict[str, dict] = {}
    for row in rows.values("day", "kind").annotate(total=Sum("visits")).order_by("day"):
        by_day.setdefault(row["day"].isoformat(), {})[row["kind"]] = row["total"]
    sources = rows.values("kind", "source").annotate(visits=Sum("visits")).order_by("-visits")[:30]
    ai_pages = (
        rows.filter(kind="ai").values("path").annotate(visits=Sum("visits")).order_by("-visits")
    )[:10]
    views = views_by_day(days)
    return {
        "views_by_day": views,
        "views_total": sum(views.values()),
        "referrals_by_day": by_day,
        "totals": {
            kind: sum(day.get(kind, 0) for day in by_day.values())
            for kind in ("search", "ai", "social")
        },
        "sources": list(sources),
        "ai_pages": list(ai_pages),
    }


def change_rows(entries) -> list[dict]:
    return [
        {
            "id": entry.id,
            "created_at": entry.created_at,
            "actor": entry.actor,
            "user": entry.user.email if entry.user_id else "",
            "area": entry.area,
            "target": entry.target,
            "summary": entry.summary,
            "changes": entry.changes,
            "undone_at": entry.undone_at,
            "can_undo": changes.can_undo(entry),
        }
        for entry in entries
    ]


def change_log(area: str = "", actor: str = "", limit: int = 200) -> list[dict]:
    entries = SeoChangeLog.objects.select_related("user").order_by("-id")
    if area:
        entries = entries.filter(area=area)
    if actor:
        entries = entries.filter(actor=actor)
    return change_rows(entries[:limit])


def ai_bots() -> list[AiBot]:
    return list(AiBot.objects.order_by("sort_order", "user_agent"))
