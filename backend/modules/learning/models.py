"""Tables from database/schema/0006_learning.sql: a learner's own records."""

from django.conf import settings
from django.db import models

USER = settings.AUTH_USER_MODEL


class Enrollment(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active"
        COMPLETED = "completed"

    user = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="+")
    course_id = models.BigIntegerField()  # catalog module
    status = models.CharField(max_length=10, choices=Status, default=Status.ACTIVE)
    progress_percent = models.PositiveSmallIntegerField(default=0)
    last_lesson_id = models.BigIntegerField(null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = "enrollments"


class LessonProgress(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="+")
    lesson_id = models.BigIntegerField()
    course_id = models.BigIntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = "lesson_progress"


class ExerciseSubmission(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="+")
    exercise_id = models.BigIntegerField()  # assessment module
    code = models.TextField()
    output = models.TextField(null=True)
    is_correct = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = "exercise_submissions"


class QuizAttempt(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="+")
    quiz_id = models.BigIntegerField()  # assessment module
    score = models.IntegerField()
    total_points = models.IntegerField()
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    passed = models.BooleanField()
    answers = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = "quiz_attempts"
