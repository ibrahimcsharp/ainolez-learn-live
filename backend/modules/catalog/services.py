"""
Catalog use cases: create and edit categories, courses, chapters, lessons,
blocks and learning paths; import lessons from Markdown; export them back.
"""

import json
from pathlib import Path

from django.db import transaction
from django.db.models import Max, Model
from django.utils import timezone

from modules.assessment import selectors as assessment_reads
from modules.assessment import services as assessment
from modules.catalog.events import CourseChanged, LessonChanged
from modules.catalog.models import (
    Category,
    Chapter,
    CodeExample,
    Course,
    LearningPath,
    LearningPathCourse,
    Lesson,
    LessonBlock,
    Status,
)
from modules.content_tools import services as content
from modules.media import selectors as media
from modules.website import selectors as website
from shared import audit
from shared.events import publish
from shared.exceptions import ServiceError
from shared.slugs import unique_slug

COURSE_FIELDS = (
    "title", "slug", "short_description", "description", "level", "language_key", "intro_video_url",
)  # fmt: skip
# Exercises of courses without a runnable language use Python.
EXERCISE_LANGUAGE = {"ai": "python", "other": "python"}

# Course slugs are top-level URLs (/python), so they must not hide app pages.
# Site pages (website module) share those URLs too: see slug_is_free().
RESERVED_SLUGS = {
    "admin", "ai", "api", "assets", "brand", "certificates", "community", "courses", "dashboard",
    "forgot-password", "leaderboard", "login", "media", "paths", "register",
    "reset-password", "search", "share", "verify-email",
}  # fmt: skip


def slug_is_free(slug: str) -> bool:
    """Whether /<slug> is free for a new course: not an app route and not a site page."""
    return slug not in RESERVED_SLUGS and not website.page_slug_taken(slug)


def save_category(category: Category | None, data: dict, by) -> Category:
    category = category or Category()
    _assign(category, data)
    category.slug = _slug(Category.objects.all(), data.get("slug"), category.name, category)
    return _save(category, by)


def save_course(course: Course | None, data: dict, by) -> Course:
    course = course or Course()
    _assign(course, data)
    course.slug = _slug(Course.objects.all(), data.get("slug"), course.title, course)
    if course.slug in RESERVED_SLUGS:
        raise ServiceError(
            f"'{course.slug}' is reserved for the site. Pick another slug.", "slug_reserved"
        )
    if website.page_slug_taken(course.slug):
        raise ServiceError(
            f"The site page /{course.slug} already uses this address. Pick another slug.",
            "slug_taken",
        )
    if course.intro_video_url:
        content.normalize_video({"url": course.intro_video_url})  # refuses unknown links
    _stamp_published(course)
    _save(course, by)
    publish(CourseChanged(course.pk))
    return course


def publish_course(course: Course, by) -> int:
    """Publish the course and all its draft lessons. Returns how many lessons went live."""
    with transaction.atomic():
        drafts = list(course.lessons.filter(status=Status.DRAFT))
        for lesson in drafts:
            lesson.status = Status.PUBLISHED
            _stamp_published(lesson)
            _save(lesson, by)
            publish(LessonChanged(lesson.pk))
        course.status = Status.PUBLISHED
        _stamp_published(course)
        _save(course, by)
        publish(CourseChanged(course.pk))
    return len(drafts)


def course_video_html(course: Course) -> str:
    if not course.intro_video_url:
        return ""
    return content.video_block_html(content.normalize_video({"url": course.intro_video_url}))


def save_chapter(chapter: Chapter | None, data: dict, by) -> Chapter:
    is_new = chapter is None
    chapter = chapter or Chapter()
    _assign(chapter, data)
    if is_new:
        chapter.sort_order = _next_order(Chapter.objects.filter(course=chapter.course))
    _save(chapter, by)
    publish(CourseChanged(chapter.course_id))
    return chapter


def save_lesson(lesson: Lesson | None, data: dict, by) -> Lesson:
    is_new = lesson is None
    lesson = lesson or Lesson()
    _assign(lesson, data)
    lesson.course_id = lesson.chapter.course_id  # slugs are unique per course
    same_course = Lesson.objects.filter(course_id=lesson.course_id)
    lesson.slug = _slug(same_course, data.get("slug"), lesson.title, lesson)
    if is_new:
        lesson.sort_order = _next_order(Lesson.objects.filter(chapter=lesson.chapter))
    _stamp_published(lesson)
    _save(lesson, by)
    publish(LessonChanged(lesson.pk))
    return lesson


def save_block(block: LessonBlock | None, data: dict, by) -> LessonBlock:
    """Store a block and turn its content into the safe HTML the public page shows."""
    is_new = block is None
    block = block or LessonBlock()
    example = data.get("example")
    exercise = data.get("exercise")
    _assign(block, {k: v for k, v in data.items() if k not in ("example", "exercise")})
    block.data = block.data or {}
    if is_new:
        block.sort_order = _next_order(LessonBlock.objects.filter(lesson=block.lesson))
    with transaction.atomic():
        if block.type == LessonBlock.Type.EXAMPLE:
            block.code_example = _save_example(block.code_example, example or {}, by)
        if block.type == LessonBlock.Type.EXERCISE:
            current = (
                assessment_reads.get_exercise(block.exercise_id) if block.exercise_id else None
            )
            block.exercise_id = assessment.save_exercise(current, exercise or {}, by).pk
        if block.type == LessonBlock.Type.QUIZ:
            _check_quiz(block)
        block.content_html = _block_html(block)
        _save(block, by)
    publish(LessonChanged(block.lesson_id))
    return block


def save_path(path: LearningPath | None, data: dict, by) -> LearningPath:
    """data may include course_ids: the path's courses in order."""
    course_ids = data.pop("course_ids", None)
    path = path or LearningPath()
    _assign(path, data)
    path.slug = _slug(LearningPath.objects.all(), data.get("slug"), path.title, path)
    with transaction.atomic():
        _save(path, by)
        if course_ids is not None:
            LearningPathCourse.objects.filter(path=path).delete()
            LearningPathCourse.objects.bulk_create(
                LearningPathCourse(path=path, course_id=cid, sort_order=i)
                for i, cid in enumerate(course_ids)
            )
    return path


def import_lessons(chapter: Chapter, files, publish: bool, by) -> list[Lesson]:
    """One lesson per .md file (a .zip gives a whole chapter), ordered by file name."""
    drafts = content.import_markdown_files(files)
    lessons = []
    with transaction.atomic():
        for draft in drafts:
            lesson = save_lesson(None, {
                "chapter": chapter, "title": draft.title, "slug": draft.slug,
                "summary": draft.summary, "estimated_minutes": draft.minutes,
                "source_md": draft.source_md,
                "status": Status.PUBLISHED if publish else Status.DRAFT,
            }, by)  # fmt: skip
            for part in draft.blocks:
                save_block(None, _block_data_from_draft(lesson, part, by), by)
            lessons.append(lesson)
    return lessons


def import_course_folder(folder: Path, publish: bool, by) -> Course | None:
    """
    A whole course from a folder (database/seed/courses/<slug>/):
        course.json   {title, slug, category: {name, icon, color}, level, language_key,
                       short_description, description,
                       chapters: [{title, description, lessons: ["01-intro.md", ...]}]}
        *.md          one lesson each, in the .md import format
    Returns None when a course with that slug already exists, even in the Trash, so
    running the seed again on every deploy never brings back a deleted course.
    """
    meta = json.loads((folder / "course.json").read_text(encoding="utf-8"))
    if Course.all_objects.filter(slug=meta["slug"]).exists() or not slug_is_free(meta["slug"]):
        return None
    status = Status.PUBLISHED if publish else Status.DRAFT
    with transaction.atomic():
        category = Category.objects.filter(name=meta["category"]["name"]).first()
        category = category or save_category(None, meta["category"], by)
        course = save_course(None, {
            "category": category, "status": status,
            **{key: meta[key] for key in COURSE_FIELDS if key in meta},
        }, by)  # fmt: skip
        minutes = 0
        for chapter_meta in meta["chapters"]:
            chapter = save_chapter(None, {
                "course": course, "title": chapter_meta["title"],
                "description": chapter_meta.get("description", ""),
            }, by)  # fmt: skip
            for name in chapter_meta["lessons"]:
                text = (folder / name).read_text(encoding="utf-8")
                draft = content.parse_lesson_markdown(text, name)
                lesson = save_lesson(None, {
                    "chapter": chapter, "title": draft.title, "slug": draft.slug,
                    "summary": draft.summary, "estimated_minutes": draft.minutes,
                    "source_md": text, "status": status,
                }, by)  # fmt: skip
                for part in draft.blocks:
                    save_block(None, _block_data_from_draft(lesson, part, by), by)
                minutes += draft.minutes
        course.estimated_minutes = minutes
        course.save(update_fields=["estimated_minutes"])
    return course


def add_markdown_blocks(lesson: Lesson, markdown: str, by) -> int:
    """Append the blocks of a Markdown text (the .md import format) to a lesson."""
    draft = content.parse_lesson_markdown(markdown)
    for part in draft.blocks:
        save_block(None, _block_data_from_draft(lesson, part, by), by)
    return len(draft.blocks)


def export_lesson_markdown(lesson: Lesson) -> str:
    """The lesson as one .md file that import_lessons can read back."""
    parts = [
        f"---\ntitle: {lesson.title}\nslug: {lesson.slug}\nminutes: {lesson.estimated_minutes}\n---"
    ]
    for block in lesson.blocks.filter(is_active=True).order_by("sort_order", "id"):
        parts.append(_block_markdown(block))
    return "\n\n".join(part for part in parts if part) + "\n"


# --- helpers ----------------------------------------------------------------


def _assign(obj: Model, data: dict) -> None:
    for field, value in data.items():
        setattr(obj, field, value)


def _save(obj: Model, by) -> Model:
    is_new = obj.pk is None
    if is_new:
        obj.created_by = by
    obj.updated_by = by
    obj.save()
    audit.record(
        f"{obj._meta.model_name}.{'created' if is_new else 'updated'}", actor=by, entity=obj
    )
    return obj


def _slug(live_rows, wanted: str | None, fallback_text: str, obj: Model) -> str:
    if wanted:
        if live_rows.filter(slug=wanted).exclude(pk=obj.pk).exists():
            raise ServiceError(f"The slug '{wanted}' is already used.", "slug_taken")
        return wanted
    if obj.pk and obj.slug:
        return obj.slug  # keep URLs stable when only the title changes
    return unique_slug(live_rows, fallback_text, exclude_pk=obj.pk)


def _stamp_published(obj: Course | Lesson) -> None:
    if obj.status == Status.PUBLISHED and obj.published_at is None:
        obj.published_at = timezone.now()


def _next_order(siblings) -> int:
    return (siblings.aggregate(m=Max("sort_order"))["m"] or 0) + 1


def _save_example(example: CodeExample | None, data: dict, by) -> CodeExample:
    language = data.get("language", "")
    if language not in CodeExample.RUN_MODES:
        raise ServiceError(
            "Pick the example language: HTML, CSS, JavaScript, Python or SQL.", "bad_language"
        )
    example = example or CodeExample()
    example.title = data.get("title", "")
    example.language = language
    example.run_mode = CodeExample.RUN_MODES[language]
    example.starter_code = data.get("starter_code", "")
    return _save(example, by)


def _check_quiz(block: LessonBlock) -> None:
    quiz = assessment_reads.get_quiz(block.quiz_id) if block.quiz_id else None
    if quiz is None or quiz.course_id != block.lesson.course_id:
        raise ServiceError("Pick one of this course's quizzes.", "bad_quiz")


def _block_html(block: LessonBlock) -> str:
    kind, data = block.type, block.data
    if kind == LessonBlock.Type.MARKDOWN:
        return content.render_markdown(block.content_md or "")
    if kind == LessonBlock.Type.CALLOUT:
        return content.callout_html(data.get("kind", "note"), block.content_md or "")
    if kind == LessonBlock.Type.VIDEO:
        block.data = content.normalize_video(data)  # store {provider, ref, start, caption}
        return content.video_block_html(block.data)
    if kind == LessonBlock.Type.EMBED:
        return content.embed_block_html(data)
    if kind == LessonBlock.Type.IMAGE:
        image = media.get_live_media(block.media_id) if block.media_id else None
        if image is None:
            raise ServiceError("Pick an image from the media library.", "missing_image")
        return content.image_html(
            image.url, data.get("alt") or image.alt_text, data.get("caption", "")
        )
    return ""  # example, exercise and quiz blocks are drawn by the frontend


def _block_data_from_draft(lesson: Lesson, draft, by) -> dict:
    data = {"lesson": lesson, "type": draft.type, "content_md": draft.content_md, "data": {}}
    if draft.type == "example":
        data["example"] = {"language": draft.data["language"], "starter_code": draft.data["code"]}
    elif draft.type == "exercise":
        language = EXERCISE_LANGUAGE.get(lesson.course.language_key, lesson.course.language_key)
        data["exercise"] = {"language": language, **draft.data}
    elif draft.type == "quiz":
        data["quiz_id"] = _quiz_from_draft(lesson, draft.data, by).pk
    else:
        data["data"] = draft.data
    return data


def _quiz_from_draft(lesson: Lesson, data: dict, by):
    """A quiz from an imported ```quiz block (see content_tools/importer.py)."""
    questions = data.get("questions") or []
    if not questions:
        raise ServiceError("A quiz block needs at least one question.", "empty_quiz")
    quiz = assessment.save_quiz(None, {
        "course_id": lesson.course_id, "title": data.get("title") or f"Quiz: {lesson.title}",
        "is_final": bool(data.get("final")),
    }, by)  # fmt: skip
    for item in questions:
        options, answer = item.get("options") or [], item.get("answer")
        if not isinstance(answer, int) or not 0 <= answer < len(options):
            raise ServiceError(f"Quiz question '{item.get('question')}': bad answer.", "bad_quiz")
        assessment.save_question(None, {
            "quiz": quiz, "question_text": item["question"],
            "code_snippet": item.get("code") or None,
            "explanation": item.get("explanation", ""),
            "options": [
                {"option_text": o, "is_correct": i == answer} for i, o in enumerate(options)
            ],
        }, by)  # fmt: skip
    return quiz


def _block_markdown(block: LessonBlock) -> str:
    data = block.data or {}
    if block.type == LessonBlock.Type.MARKDOWN:
        return block.content_md or ""
    if block.type == LessonBlock.Type.CALLOUT:
        body = "\n".join(f"    {line}" for line in (block.content_md or "").splitlines())
        return f"!!! {data.get('kind', 'note')}\n{body}"
    if block.type == LessonBlock.Type.EXAMPLE and block.code_example:
        example = block.code_example
        return f"```{example.language} tryit\n{example.starter_code}\n```"
    if block.type == LessonBlock.Type.VIDEO:
        provider, ref = data["provider"], data["ref"]
        if provider in ("youtube", "vimeo"):
            return f"{{{{{provider}:{ref}}}}}"
        url = {
            "loom": f"https://www.loom.com/share/{ref}",
            "drive": f"https://drive.google.com/file/d/{ref}/view",
        }.get(provider, ref)
        return f"{{{{video:{url}}}}}"
    return block.content_html or ""  # image and embed: their HTML is valid Markdown
