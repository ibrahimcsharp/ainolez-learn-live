"""
The AI course generator (PLANNING.md 6.7):

    start_job       the admin describes a course; a job asks Claude for an outline
    save_outline    the admin edits the outline
    generate        creates the draft course, chapters and lessons, then one job per
                    lesson asks Claude for its text, exercise and quiz
    retry           queues the outline or the lessons that failed again

Nothing is published: the course and its lessons stay drafts, marked ai_generated,
until an admin reviews them.
"""

from django.db import transaction
from django.db.models import F

from modules.ai_authoring import prompts
from modules.ai_authoring.models import CourseJob
from modules.assessment import services as assessment
from modules.assistant import services as assistant
from modules.catalog import selectors as catalog_reads
from modules.catalog import services as catalog
from shared import audit, jobs
from shared.exceptions import ServiceError

LEVELS = ("beginner", "intermediate", "advanced")
LANGUAGES = ("html", "css", "javascript", "python", "sql", "ai", "other")
EXERCISE_LANGUAGE = {"ai": "python", "other": "python"}
OUTLINE_JOB, LESSON_JOB = "ai_authoring.outline", "ai_authoring.lesson"
Status = CourseJob.Status


def start_job(data: dict, by) -> CourseJob:
    _check_switched_on()
    if not data.get("topic", "").strip():
        raise ServiceError("Describe the course topic.", "no_topic")
    level, language = data.get("level", "beginner"), data.get("language_key", "python")
    if level not in LEVELS or language not in LANGUAGES:
        raise ServiceError("Pick a level and a language from the lists.", "bad_choice")
    if not 1 <= int(data.get("chapters_count", 5)) <= 15:
        raise ServiceError("Use 1 to 15 chapters.", "bad_count")
    if not 1 <= int(data.get("lessons_per_chapter", 4)) <= 10:
        raise ServiceError("Use 1 to 10 lessons per chapter.", "bad_count")
    if data.get("category_id") and not catalog_reads.category_exists(data["category_id"]):
        raise ServiceError("Pick an existing category.", "bad_category")
    job = CourseJob(**data, created_by=by, updated_by=by)
    job.save()
    jobs.enqueue(OUTLINE_JOB, {"job_id": job.pk})
    audit.record("aicoursejob.created", actor=by, entity=job)
    return job


def write_outline(job: CourseJob) -> None:
    """Job handler: ask Claude for the outline."""
    task = prompts.OUTLINE_TASK.format(
        topic=job.topic,
        level=job.level,
        audience=job.audience or "anyone who wants to learn",
        language=job.language_key,
        chapters=job.chapters_count,
        lessons=job.lessons_per_chapter,
        notes=job.notes or "none",
    )
    try:
        outline, reply = assistant.generate_json(
            system=prompts.SYSTEM, prompt=task, schema=prompts.OUTLINE_SCHEMA, max_tokens=8000
        )
    except ServiceError as exc:
        _fail(job, exc.message)
        return
    _count_tokens(job, reply)
    job.outline = _clean_outline(outline)
    job.status, job.error = Status.OUTLINE_READY, ""
    job.save(update_fields=["outline", "status", "error", "updated_at"])


def save_outline(job: CourseJob, outline: dict, by) -> CourseJob:
    if job.status != Status.OUTLINE_READY:
        raise ServiceError("The outline can only change before the lessons are written.", "locked")
    job.outline = _clean_outline(outline)
    job.updated_by = by
    job.save(update_fields=["outline", "updated_by", "updated_at"])
    return job


def generate(job: CourseJob, by) -> CourseJob:
    """Create the draft course from the outline and queue one job per lesson."""
    _check_switched_on()
    if job.status != Status.OUTLINE_READY:
        raise ServiceError("Generate from a ready outline.", "not_ready")
    if not job.category_id:
        raise ServiceError("Pick the category the course belongs to first.", "no_category")
    outline = job.outline
    with transaction.atomic():
        course = catalog.save_course(None, {
            "category_id": job.category_id, "title": outline["title"],
            "short_description": outline["short_description"][:300],
            "description": outline["description"], "level": job.level,
            "language_key": job.language_key, "ai_generated": True,
        }, by)  # fmt: skip
        for chapter_plan in outline["chapters"]:
            chapter = catalog.save_chapter(None, {
                "course": course, "title": chapter_plan["title"],
                "description": chapter_plan["description"][:500],
            }, by)  # fmt: skip
            for lesson_plan in chapter_plan["lessons"]:
                lesson = catalog.save_lesson(None, {
                    "chapter": chapter, "title": lesson_plan["title"],
                    "summary": lesson_plan["summary"][:500], "ai_generated": True,
                }, by)  # fmt: skip
                lesson_plan["lesson_id"] = lesson.pk
        job.course_id = course.pk
        job.outline = outline
        job.lessons_total = sum(len(c["lessons"]) for c in outline["chapters"])
        job.status, job.updated_by = Status.GENERATING, by
        job.save()
        for lesson_id in _lesson_ids(job):
            jobs.enqueue(LESSON_JOB, {"job_id": job.pk, "lesson_id": lesson_id})
    audit.record("aicoursejob.generate", actor=by, entity=job, after={"course_id": course.pk})
    return job


def write_lesson(job: CourseJob, lesson_id: int) -> None:
    """Job handler: Claude writes one lesson; it becomes blocks, an exercise and a quiz."""
    plans = [p for c in job.outline["chapters"] for p in c["lessons"]]
    plan = next((p for p in plans if p.get("lesson_id") == lesson_id), None)
    if plan is None or catalog_reads.lesson_has_blocks(lesson_id):
        return  # removed from the course, or already written
    try:
        draft, reply = assistant.generate_json(
            system=prompts.SYSTEM, prompt=_lesson_task(job, plan), schema=prompts.LESSON_SCHEMA
        )
    except ServiceError as exc:
        failed = CourseJob.objects.filter(pk=job.pk)
        failed.update(lessons_failed=F("lessons_failed") + 1, error=exc.message[:1000])
        _finish_if_done(job.pk)
        return
    _count_tokens(job, reply)
    with transaction.atomic():
        _save_lesson_draft(job, lesson_id, draft)
        CourseJob.objects.filter(pk=job.pk).update(lessons_done=F("lessons_done") + 1)
    _finish_if_done(job.pk)


def retry(job: CourseJob, by) -> CourseJob:
    """Queue the outline again (failed before one existed) or the lessons still missing."""
    _check_switched_on()
    if job.outline is None:
        job.status, job.error = Status.OUTLINE_QUEUED, ""
        job.save(update_fields=["status", "error", "updated_at"])
        jobs.enqueue(OUTLINE_JOB, {"job_id": job.pk})
        return job
    missing = [i for i in _lesson_ids(job) if not catalog_reads.lesson_has_blocks(i)]
    if job.course_id is None or not missing:
        raise ServiceError("Nothing to retry.", "nothing_to_retry")
    job.status, job.error, job.lessons_failed = Status.GENERATING, "", 0
    job.lessons_done = job.lessons_total - len(missing)
    job.updated_by = by
    job.save()
    for lesson_id in missing:
        jobs.enqueue(LESSON_JOB, {"job_id": job.pk, "lesson_id": lesson_id})
    return job


# --- helpers --------------------------------------------------------------------


def _check_switched_on() -> None:
    if not assistant.settings_row().course_generator_enabled:
        raise ServiceError(
            "The AI course generator is switched off. Switch it on first.", "generator_off"
        )


def _clean_outline(outline: dict) -> dict:
    """Keep only the fields we use, and check the shape (the admin may have edited it)."""
    try:
        chapters = [
            {
                "title": str(c["title"]).strip()[:200],
                "description": str(c.get("description", "")).strip(),
                "lessons": [
                    {
                        "title": str(lesson["title"]).strip()[:200],
                        "summary": str(lesson.get("summary", "")).strip(),
                        **({"lesson_id": lesson["lesson_id"]} if lesson.get("lesson_id") else {}),
                    }
                    for lesson in c["lessons"]
                    if str(lesson.get("title", "")).strip()
                ],
            }
            for c in outline["chapters"]
            if str(c.get("title", "")).strip()
        ]
        title = str(outline["title"]).strip()[:200]
    except (KeyError, TypeError) as exc:
        raise ServiceError("The outline is not complete.", "bad_outline") from exc
    if not title or not chapters or not all(c["lessons"] for c in chapters):
        raise ServiceError("The outline needs a title and lessons in every chapter.", "bad_outline")
    return {
        "title": title,
        "short_description": str(outline.get("short_description", "")).strip(),
        "description": str(outline.get("description", "")).strip(),
        "chapters": chapters,
    }


def _lesson_task(job: CourseJob, plan: dict) -> str:
    lines = []
    for chapter in job.outline["chapters"]:
        lines.append(f"Chapter: {chapter['title']}")
        for lesson in chapter["lessons"]:
            marker = ">>" if lesson is plan else "  "
            lines.append(f"{marker} {lesson['title']}: {lesson['summary']}")
    exercise_language = EXERCISE_LANGUAGE.get(job.language_key, job.language_key)
    fence = "html" if exercise_language == "css" else exercise_language
    return prompts.LESSON_TASK.format(
        course=job.outline["title"],
        level=job.level,
        audience=job.audience or "anyone who wants to learn",
        outline="\n".join(lines),
        title=plan["title"],
        summary=plan["summary"],
        fence=fence,
        runner=prompts.RUNNERS.get(exercise_language, ""),
        exercise_language=exercise_language,
    )


def _save_lesson_draft(job: CourseJob, lesson_id: int, draft: dict) -> None:
    by = job.created_by
    lesson = catalog.save_lesson(
        catalog_reads.get_lesson(lesson_id),
        {"summary": draft["summary"][:500], "estimated_minutes": max(1, min(draft["minutes"], 60))},
        by,
    )
    catalog.add_markdown_blocks(lesson, draft["markdown"], by)
    exercise = draft["exercise"]
    language = EXERCISE_LANGUAGE.get(job.language_key, job.language_key)
    catalog.save_block(None, {
        "lesson": lesson, "type": "exercise",
        "exercise": {**exercise, "language": language},
    }, by)  # fmt: skip
    questions = [
        q for q in draft["quiz"]
        if len(q["options"]) >= 2 and 0 <= q["correct_index"] < len(q["options"])
    ]  # fmt: skip
    if questions:
        title = f"Quiz: {lesson.title}"
        quiz = assessment.save_quiz(None, {"course_id": job.course_id, "title": title}, by)
        for q in questions:
            assessment.save_question(None, {
                "quiz": quiz, "question_text": q["question"],
                "explanation": q["explanation"][:1000],
                "options": [
                    {"option_text": text[:500], "is_correct": i == q["correct_index"]}
                    for i, text in enumerate(q["options"])
                ],
            }, by)  # fmt: skip
        catalog.save_block(None, {"lesson": lesson, "type": "quiz", "quiz_id": quiz.pk}, by)


def _lesson_ids(job: CourseJob) -> list[int]:
    plans = [p for c in job.outline["chapters"] for p in c["lessons"]]
    return [p["lesson_id"] for p in plans if p.get("lesson_id")]


def _count_tokens(job: CourseJob, reply) -> None:
    CourseJob.objects.filter(pk=job.pk).update(
        tokens_in=F("tokens_in") + reply.tokens_in,
        tokens_out=F("tokens_out") + reply.tokens_out,
        cost_usd=F("cost_usd") + round(reply.cost, 4),
    )


def _finish_if_done(job_id: int) -> None:
    job = CourseJob.objects.get(pk=job_id)
    if job.lessons_done + job.lessons_failed < job.lessons_total:
        return
    job.status = Status.DRAFTED if job.lessons_failed == 0 else Status.FAILED
    job.save(update_fields=["status", "updated_at"])


def _fail(job: CourseJob, message: str) -> None:
    job.status, job.error = Status.FAILED, message[:1000]
    job.save(update_fields=["status", "error", "updated_at"])
