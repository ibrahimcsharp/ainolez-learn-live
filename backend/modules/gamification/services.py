"""Points, streaks and badges. Points only ever go into the append-only ledger."""

from datetime import timedelta

from django.db import IntegrityError, transaction
from django.db.models import F, Sum
from django.utils import timezone

from modules.gamification.models import Badge, LearnerStats, PointsLedger, PointsRule, UserBadge
from shared import audit
from shared.exceptions import ServiceError
from shared.slugs import unique_slug


def award(user_id: int, event_key: str, ref_type: str, ref_id: int) -> int:
    """Add the rule's points once per (event, ref). Returns the points given (0 if none)."""
    rule = PointsRule.objects.filter(event_key=event_key, is_active=True).first()
    if rule is None or rule.points == 0:
        return 0
    points = rule.points
    if rule.daily_cap is not None:
        today = (
            PointsLedger.objects.filter(
                user_id=user_id, event_key=event_key, created_at__date=timezone.now().date()
            ).aggregate(s=Sum("points"))["s"]
            or 0
        )
        points = min(points, max(rule.daily_cap - today, 0))
        if points == 0:
            return 0
    try:
        with transaction.atomic():
            PointsLedger.objects.create(
                user_id=user_id, rule=rule, event_key=event_key,
                points=points, ref_type=ref_type, ref_id=ref_id,
            )  # fmt: skip
    except IntegrityError:  # already awarded for this ref
        return 0
    stats(user_id)
    LearnerStats.objects.filter(user_id=user_id).update(total_points=F("total_points") + points)
    return points


def record_activity(user_id: int) -> None:
    """Extend (or restart) the learner's daily streak. The first activity of a day counts."""
    today = timezone.now().date()
    row = LearnerStats.objects.select_for_update().get(pk=stats(user_id).pk)
    if row.last_active_date == today:
        return
    continues = row.last_active_date == today - timedelta(days=1)
    row.current_streak = row.current_streak + 1 if continues else 1
    row.longest_streak = max(row.longest_streak, row.current_streak)
    row.last_active_date = today
    row.save(update_fields=["current_streak", "longest_streak", "last_active_date", "updated_at"])
    if continues:
        award(user_id, "streak_day", "day", today.toordinal())


def count(user_id: int, field: str) -> None:
    """Add one to a learner_stats counter, e.g. lessons_completed."""
    stats(user_id)
    LearnerStats.objects.filter(user_id=user_id).update(**{field: F(field) + 1})


def check_badges(user_id: int) -> list[Badge]:
    """Give every active badge whose rule the learner now meets. Returns new badges."""
    row = stats(user_id)
    owned = set(UserBadge.objects.filter(user_id=user_id).values_list("badge_id", flat=True))
    new = []
    for badge in Badge.objects.filter(is_active=True).exclude(pk__in=owned):
        field = Badge.RULE_TYPES.get(badge.rule.get("type"))
        if field and getattr(row, field) >= int(badge.rule.get("threshold", 0)):
            UserBadge.objects.create(user_id=user_id, badge=badge)
            new.append(badge)
    return new


def stats(user_id: int) -> LearnerStats:
    row, _ = LearnerStats.objects.get_or_create(user_id=user_id)
    row.refresh_from_db()
    return row


def save_rule(rule: PointsRule | None, data: dict, by) -> PointsRule:
    rule = rule or PointsRule()
    for name, value in data.items():
        setattr(rule, name, value)
    return _save(rule, by)


def save_badge(badge: Badge | None, data: dict, by) -> Badge:
    badge = badge or Badge()
    for name, value in data.items():
        setattr(badge, name, value)
    rule = badge.rule or {}
    if rule.get("type") not in Badge.RULE_TYPES or not str(rule.get("threshold", "")).isdigit():
        raise ServiceError("A badge rule needs a type and a whole-number threshold.", "bad_rule")
    badge.rule = {"type": rule["type"], "threshold": int(rule["threshold"])}
    if not badge.slug:
        badge.slug = unique_slug(Badge.objects.all(), badge.name, exclude_pk=badge.pk)
    return _save(badge, by)


def _save(obj, by):
    is_new = obj.pk is None
    if is_new:
        obj.created_by = by
    obj.updated_by = by
    obj.save()
    audit.record(
        f"{obj._meta.model_name}.{'created' if is_new else 'updated'}", actor=by, entity=obj
    )
    return obj
