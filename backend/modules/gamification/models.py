"""Tables from database/schema/0007_gamification.sql."""

from django.conf import settings
from django.db import models

from shared.models import BaseModel

USER = settings.AUTH_USER_MODEL


class PointsRule(BaseModel):
    event_key = models.CharField(max_length=50)
    points = models.IntegerField()
    daily_cap = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=255, blank=True)

    class Meta(BaseModel.Meta):
        managed = False
        db_table = "points_rules"


class PointsLedger(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="+")
    rule = models.ForeignKey(PointsRule, on_delete=models.SET_NULL, null=True, related_name="+")
    event_key = models.CharField(max_length=50)
    points = models.IntegerField()
    ref_type = models.CharField(max_length=30)
    ref_id = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = "points_ledger"


class LearnerStats(models.Model):
    user = models.OneToOneField(USER, on_delete=models.CASCADE, primary_key=True, related_name="+")
    total_points = models.IntegerField(default=0)
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_active_date = models.DateField(null=True)
    lessons_completed = models.IntegerField(default=0)
    courses_completed = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = "learner_stats"


class Badge(BaseModel):
    RULE_TYPES = {
        "points": "total_points",
        "lessons": "lessons_completed",
        "courses": "courses_completed",
        "streak": "longest_streak",
    }

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    description = models.CharField(max_length=255, blank=True)
    icon = models.CharField(max_length=50, default="🏅")
    rule = models.JSONField()  # {"type": one of RULE_TYPES, "threshold": int}

    class Meta(BaseModel.Meta):
        managed = False
        db_table = "badges"


class UserBadge(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="+")
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name="+")
    awarded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = "user_badges"
