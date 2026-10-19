from datetime import timedelta

import pytest
from django.utils import timezone

from modules.gamification import services
from modules.gamification.models import LearnerStats

pytestmark = pytest.mark.django_db


def test_learning_on_the_next_day_extends_the_streak(make_user):
    user = make_user()
    yesterday = timezone.now().date() - timedelta(days=1)
    LearnerStats.objects.create(
        user=user, current_streak=3, longest_streak=3, last_active_date=yesterday
    )

    services.record_activity(user.pk)
    services.record_activity(user.pk)  # the same day counts once

    stats = LearnerStats.objects.get(user=user)
    assert (stats.current_streak, stats.longest_streak, stats.total_points) == (4, 4, 5)


def test_a_missed_day_restarts_the_streak(make_user):
    user = make_user()
    long_ago = timezone.now().date() - timedelta(days=5)
    LearnerStats.objects.create(
        user=user, current_streak=9, longest_streak=9, last_active_date=long_ago
    )
    services.record_activity(user.pk)
    stats = LearnerStats.objects.get(user=user)
    assert (stats.current_streak, stats.longest_streak) == (1, 9)


def test_daily_cap_limits_points(make_user):
    from modules.gamification.models import PointsRule

    PointsRule.objects.filter(event_key="lesson_completed").update(daily_cap=15)
    user = make_user()
    given = [services.award(user.pk, "lesson_completed", "lesson", i) for i in (1, 2, 3)]
    assert given == [10, 5, 0]
