"""Keeps the tutor's knowledge in step with the lessons."""

from modules.catalog.events import LessonChanged
from shared import jobs
from shared.events import subscribe


@subscribe(LessonChanged)
def reindex_lesson(event: LessonChanged) -> None:
    # A job, so saving a lesson stays fast; cron picks it up within a minute.
    jobs.enqueue("assistant.index_lesson", {"lesson_id": event.lesson_id})
