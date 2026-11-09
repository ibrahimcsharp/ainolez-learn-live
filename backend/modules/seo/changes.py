"""
The SEO & GEO change log: every change an admin makes in the Center, and what the site
does by itself (builds, IndexNow). Admin changes keep the old values, so they can be undone.
"""

from decimal import Decimal

from modules.seo.models import SeoChangeLog

AREAS_WITH_UNDO = ("settings", "page", "ai_bot")


def record(
    area: str,
    *,
    before: dict | None = None,
    after: dict | None = None,
    by=None,
    target: str = "",
    target_id: int | None = None,
    summary: str = "",
) -> SeoChangeLog | None:
    """Log a change. With before/after, only fields whose value changed are kept, and
    nothing is logged when none did."""
    diff = None
    if after is not None:
        before = before or {}
        diff = [
            {"field": name, "old": _plain(before.get(name)), "new": _plain(value)}
            for name, value in after.items()
            if _plain(before.get(name)) != _plain(value)
        ]
        if not diff:
            return None
        summary = summary or "Changed " + ", ".join(item["field"] for item in diff)
    return SeoChangeLog.objects.create(
        actor=SeoChangeLog.Actor.ADMIN if by else SeoChangeLog.Actor.AUTO,
        user=by,
        area=area,
        target=target[:255],
        target_id=target_id,
        summary=summary[:500],
        changes=diff,
    )


def values(obj, fields) -> dict:
    return {name: getattr(obj, name) for name in fields}


def can_undo(entry: SeoChangeLog) -> bool:
    return entry.area in AREAS_WITH_UNDO and bool(entry.changes) and entry.undone_at is None


def _plain(value):
    """JSON-safe values, so the log can be stored and compared."""
    if isinstance(value, Decimal):
        return str(value)
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return value
