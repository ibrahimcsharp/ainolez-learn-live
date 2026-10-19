"""
Database-backed job queue (shared hosting has no Redis or Celery).

    @job("identity.send_verification_email")
    def send_verification_email(payload): ...

    enqueue("identity.send_verification_email", {"user_id": 7})

Cron runs ``manage.py run_jobs`` every minute, which calls run_pending().
A failed job is retried with back-off, then marked failed.
"""

import logging
import time
from collections.abc import Callable
from datetime import timedelta

from django.db import transaction
from django.db.models import F
from django.utils import timezone

from shared.models import Job

MAX_ATTEMPTS = 3
logger = logging.getLogger(__name__)
_handlers: dict[str, Callable[[dict], None]] = {}


def job(name: str):
    """Register a function as the handler for jobs of type ``name``."""

    def register(handler: Callable[[dict], None]):
        _handlers[name] = handler
        return handler

    return register


def enqueue(name: str, payload: dict | None = None, *, delay: timedelta | None = None) -> Job:
    if name not in _handlers:
        raise ValueError(f"No job handler registered for '{name}'")
    run_after = timezone.now() + (delay or timedelta())
    return Job.objects.create(type=name, payload=payload or {}, run_after=run_after)


def run_pending(max_seconds: int = 50) -> int:
    """Run due jobs until none are left or time is up. Returns how many ran."""
    deadline = time.monotonic() + max_seconds
    count = 0
    while time.monotonic() < deadline:
        claimed = _claim_next()
        if claimed is None:
            break
        _run(claimed)
        count += 1
    return count


def _claim_next() -> Job | None:
    while True:
        candidate = (
            Job.objects.filter(status=Job.Status.QUEUED, run_after__lte=timezone.now())
            .order_by("id")
            .first()
        )
        if candidate is None:
            return None
        # The status check makes the claim safe even if two runners overlap.
        claimed = Job.objects.filter(pk=candidate.pk, status=Job.Status.QUEUED).update(
            status=Job.Status.RUNNING, started_at=timezone.now(), attempts=F("attempts") + 1
        )
        if claimed:
            candidate.refresh_from_db()
            return candidate


def _run(item: Job) -> None:
    try:
        with transaction.atomic():
            _handlers[item.type](item.payload)
    except Exception as exc:
        logger.exception("Job %s (%s) failed", item.pk, item.type)
        item.last_error = f"{type(exc).__name__}: {exc}"[:2000]
        if item.attempts >= MAX_ATTEMPTS:
            item.status = Job.Status.FAILED
            item.finished_at = timezone.now()
        else:
            item.status = Job.Status.QUEUED
            item.run_after = timezone.now() + timedelta(minutes=2**item.attempts)
    else:
        item.status = Job.Status.DONE
        item.finished_at = timezone.now()
    item.save(update_fields=["status", "last_error", "run_after", "finished_at"])
