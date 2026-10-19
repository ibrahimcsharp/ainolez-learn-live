"""Tables from database/schema/0013_ai_authoring.sql."""

from django.db import models

from shared.models import BaseModel


class CourseJob(BaseModel):
    class Status(models.TextChoices):
        OUTLINE_QUEUED = "outline_queued"
        OUTLINE_READY = "outline_ready"
        GENERATING = "generating"
        DRAFTED = "drafted"
        FAILED = "failed"

    topic = models.CharField(max_length=200)
    level = models.CharField(max_length=20, default="beginner")
    audience = models.CharField(max_length=300, blank=True)
    language_key = models.CharField(max_length=20, default="python")
    category_id = models.BigIntegerField(null=True, blank=True)  # catalog module
    chapters_count = models.PositiveSmallIntegerField(default=5)
    lessons_per_chapter = models.PositiveSmallIntegerField(default=4)
    notes = models.TextField(null=True, blank=True)
    outline = models.JSONField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status, default=Status.OUTLINE_QUEUED)
    course_id = models.BigIntegerField(null=True, blank=True)  # catalog module
    lessons_total = models.IntegerField(default=0)
    lessons_done = models.IntegerField(default=0)
    lessons_failed = models.IntegerField(default=0)
    tokens_in = models.BigIntegerField(default=0)
    tokens_out = models.BigIntegerField(default=0)
    cost_usd = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    error = models.CharField(max_length=1000, blank=True)

    class Meta(BaseModel.Meta):
        managed = False
        db_table = "ai_course_jobs"

    @property
    def title(self) -> str:
        return self.topic
