"""
Shared kernel models.

Every table is created by hand-written SQL in database/schema/, so all
models here and in the modules use ``managed = False``.
"""

from django.conf import settings
from django.db import models
from django.utils import timezone


class LiveManager(models.Manager):
    """Default manager: hides soft-deleted rows."""

    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


def _user_fk(column: str) -> models.ForeignKey:
    return models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        db_column=column,
    )


class BaseModel(models.Model):
    """Record controls used by every manageable table (PLANNING.md §4)."""

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = _user_fk("created_by")
    updated_by = _user_fk("updated_by")
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = _user_fk("deleted_by")
    alive = models.BooleanField(null=True, default=True)  # NULL once soft deleted

    objects = LiveManager()
    all_objects = models.Manager()  # includes the Trash  # noqa: DJ012

    class Meta:
        abstract = True
        default_manager_name = "objects"

    def soft_delete(self, by=None) -> None:
        self.deleted_at = timezone.now()
        self.deleted_by = by
        self.alive = None
        self.save(update_fields=["deleted_at", "deleted_by", "alive", "updated_at"])

    def restore(self) -> None:
        self.deleted_at = None
        self.deleted_by = None
        self.alive = True
        self.save(update_fields=["deleted_at", "deleted_by", "alive", "updated_at"])


class AuditLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="+"
    )
    action = models.CharField(max_length=60)
    entity_type = models.CharField(max_length=60, blank=True)
    entity_id = models.BigIntegerField(null=True)
    before_data = models.JSONField(null=True)
    after_data = models.JSONField(null=True)
    ip_address = models.CharField(max_length=45, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = "audit_logs"


class Job(models.Model):
    class Status(models.TextChoices):
        QUEUED = "queued"
        RUNNING = "running"
        DONE = "done"
        FAILED = "failed"

    type = models.CharField(max_length=100)
    payload = models.JSONField(default=dict)
    status = models.CharField(max_length=10, choices=Status, default=Status.QUEUED)
    attempts = models.PositiveSmallIntegerField(default=0)
    run_after = models.DateTimeField(default=timezone.now)
    last_error = models.CharField(max_length=2000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True)
    finished_at = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = "jobs"
