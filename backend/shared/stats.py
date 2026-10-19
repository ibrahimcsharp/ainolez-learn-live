"""Small helpers for report queries."""

from datetime import datetime, time, timedelta

from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils import timezone


def first_day(days: int):
    """The first date of a report covering the last `days` days, today included."""
    return timezone.now().date() - timedelta(days=days - 1)


def daily_counts(queryset, field: str, days: int) -> dict[str, int]:
    """{"2026-10-19": rows, ...} for a datetime `field` over the last `days` days."""
    start = datetime.combine(first_day(days), time.min, tzinfo=timezone.get_current_timezone())
    rows = (
        queryset.filter(**{f"{field}__gte": start})
        .annotate(day=TruncDate(field))
        .values("day")
        .annotate(total=Count("pk"))
        .order_by()
    )
    return {row["day"].isoformat(): row["total"] for row in rows}
