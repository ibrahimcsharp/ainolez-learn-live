"""Read queries other modules may use."""

from datetime import timedelta

from django.db.models import Count, Q
from django.utils import timezone

from modules.identity.models import Role, User
from shared.stats import daily_counts


def get_user(user_id: int) -> User | None:
    return User.objects.select_related("role").filter(pk=user_id).first()


def get_user_by_email(email: str) -> User | None:
    return User.objects.select_related("role").filter(email__iexact=email.strip()).first()


def first_super_admin() -> User | None:
    return User.objects.filter(role__name=Role.SUPER_ADMIN, is_active=True).order_by("id").first()


def display_name(user_id: int) -> str:
    user = User.objects.filter(pk=user_id).first()
    return user.display_name if user else ""


def get_email(user_id: int) -> str:
    return User.objects.filter(pk=user_id).values_list("email", flat=True).first() or ""


def display_names(user_ids) -> dict[int, str]:
    return {user.pk: user.display_name for user in User.all_objects.filter(pk__in=list(user_ids))}


def leaderboard_names(user_ids) -> dict[int, str]:
    """{user_id: name} for active users who agreed to appear on leaderboards."""
    users = User.objects.filter(
        pk__in=list(user_ids), is_active=True, is_banned=False, show_on_leaderboard=True
    )
    return {user.pk: user.display_name for user in users}


def user_counts() -> dict[str, int]:
    week_ago = timezone.now() - timedelta(days=7)
    learners = Q(role__name=Role.LEARNER)
    return User.objects.aggregate(
        learners=Count("id", filter=learners),
        verified_learners=Count("id", filter=learners & Q(is_email_verified=True)),
        new_learners_7d=Count("id", filter=learners & Q(created_at__gte=week_ago)),
        admins=Count("id", filter=Q(role__name=Role.SUPER_ADMIN)),
    )


def signups_by_day(days: int) -> dict[str, int]:
    return daily_counts(User.objects.filter(role__name=Role.LEARNER), "created_at", days)
