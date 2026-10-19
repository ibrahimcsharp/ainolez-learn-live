"""Read queries: a learner's points and badges, and the leaderboards."""

from datetime import timedelta

from django.db.models import Sum
from django.utils import timezone

from modules.gamification.models import LearnerStats, PointsLedger, UserBadge
from modules.identity import selectors as identity

PERIODS = {"week": 7, "month": 30, "all": None}


def learner_summary(user_id: int) -> dict:
    row = LearnerStats.objects.filter(user_id=user_id).first()
    badges = (
        UserBadge.objects.filter(user_id=user_id).select_related("badge").order_by("awarded_at")
    )
    recent = PointsLedger.objects.filter(user_id=user_id).order_by("-created_at")[:10]
    return {
        "total_points": row.total_points if row else 0,
        "current_streak": row.current_streak if row else 0,
        "longest_streak": row.longest_streak if row else 0,
        "lessons_completed": row.lessons_completed if row else 0,
        "courses_completed": row.courses_completed if row else 0,
        "badges": [
            {
                "name": ub.badge.name,
                "icon": ub.badge.icon,
                "description": ub.badge.description,
                "awarded_at": ub.awarded_at,
            }
            for ub in badges
        ],  # fmt: skip
        "recent_points": [
            {"event_key": p.event_key, "points": p.points, "created_at": p.created_at}
            for p in recent
        ],
    }


def leaderboard(period: str = "week", limit: int = 20) -> list[dict]:
    """Top learners by points in the period. Learners who opted out are left out."""
    days = PERIODS.get(period, 7)
    ledger = PointsLedger.objects.all()
    if days:
        ledger = ledger.filter(created_at__gte=timezone.now() - timedelta(days=days))
    totals = (
        ledger.values("user_id").annotate(points=Sum("points")).order_by("-points")[: limit * 3]
    )
    names = identity.leaderboard_names([row["user_id"] for row in totals])
    ranked = [row for row in totals if row["user_id"] in names][:limit]
    return [
        {"rank": i + 1, "name": names[row["user_id"]], "points": row["points"]}
        for i, row in enumerate(ranked)
    ]


def total_points(user_id: int) -> int:
    row = LearnerStats.objects.filter(user_id=user_id).values_list("total_points", flat=True)
    return row.first() or 0
