"""Read queries. Public ones only return live, active, published content."""

import re
from dataclasses import dataclass

from django.db import connection
from django.db.models import Prefetch, QuerySet

from modules.catalog.models import (
    Category,
    Chapter,
    Course,
    LearningPath,
    LearningPathCourse,
    Lesson,
    LessonBlock,
    Status,
)

SEARCH_LIMIT = 30


@dataclass
class LessonPage:
    lesson: Lesson
    blocks: list[LessonBlock]
    chapters: list[Chapter]  # the course outline, each with .visible_lessons
    previous: Lesson | None
    next: Lesson | None


def public_categories() -> QuerySet[Category]:
    return Category.objects.filter(is_active=True).order_by("sort_order", "name")


def public_courses(category_slug: str = "") -> QuerySet[Course]:
    courses = Course.objects.filter(
        status=Status.PUBLISHED,
        is_active=True,
        category__is_active=True,
        category__deleted_at__isnull=True,
    ).select_related("category")
    if category_slug:
        courses = courses.filter(category__slug=category_slug)
    return courses.order_by("category__sort_order", "title")


def public_course_links(course_ids) -> dict[int, dict]:
    """{id: {"title", "slug"}} for the given courses that are public right now."""
    ids = [i for i in course_ids if i]
    rows = public_courses().filter(pk__in=ids).values("pk", "title", "slug") if ids else []
    return {row["pk"]: {"title": row["title"], "slug": row["slug"]} for row in rows}


def course_slug_taken(slug: str) -> bool:
    """True when a live course (drafts included) already uses ``slug``."""
    return Course.objects.filter(slug=slug).exists()


def public_course(slug: str) -> tuple[Course, list[Chapter]] | None:
    course = public_courses().filter(slug=slug).first()
    return (course, _outline(course)) if course else None


def public_lesson(course_slug: str, lesson_slug: str) -> LessonPage | None:
    found = public_course(course_slug)
    if found is None:
        return None
    course, chapters = found
    ordered = [lesson for chapter in chapters for lesson in chapter.visible_lessons]
    position = next((i for i, item in enumerate(ordered) if item.slug == lesson_slug), None)
    if position is None:
        return None
    lesson = ordered[position]
    blocks = list(
        lesson.blocks.filter(is_active=True)
        .select_related("code_example")
        .order_by("sort_order", "id")
    )
    return LessonPage(
        lesson=lesson,
        blocks=blocks,
        chapters=chapters,
        previous=ordered[position - 1] if position > 0 else None,
        next=ordered[position + 1] if position + 1 < len(ordered) else None,
    )


def public_paths() -> list[tuple[LearningPath, list[Course]]]:
    """Each active path with its published courses, in path order."""
    visible = {course.pk: course for course in public_courses()}
    in_order = Prefetch("path_courses", queryset=LearningPathCourse.objects.order_by("sort_order"))
    paths = LearningPath.objects.filter(is_active=True).prefetch_related(in_order).order_by("title")
    return [
        (path, [visible[pc.course_id] for pc in path.path_courses.all() if pc.course_id in visible])
        for path in paths
    ]


def search_lessons(query: str) -> list[Lesson]:
    """MySQL FULLTEXT search over lesson titles, summaries and block text."""
    words = [w for w in re.findall(r"\w+", query) if len(w) >= 3][:8]
    if not words:
        return []
    terms = " ".join(f"{w}*" for w in words)
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT l.id,
                   MATCH(l.title, l.summary) AGAINST (%s IN BOOLEAN MODE) * 2
                   + COALESCE(MAX(MATCH(b.content_md) AGAINST (%s IN BOOLEAN MODE)), 0) AS score
            FROM lessons l
            LEFT JOIN lesson_blocks b
                   ON b.lesson_id = l.id AND b.deleted_at IS NULL AND b.is_active = 1
            GROUP BY l.id
            HAVING score > 0
            ORDER BY score DESC
            LIMIT 200
            """,
            [terms, terms],
        )
        ranked = [row[0] for row in cursor.fetchall()]
    visible = {lesson.pk: lesson for lesson in _visible_lessons().filter(pk__in=ranked)}
    return [visible[pk] for pk in ranked if pk in visible][:SEARCH_LIMIT]


def catalog_counts() -> dict[str, int]:
    return {
        "courses_published": Course.objects.filter(status=Status.PUBLISHED).count(),
        "lessons_published": Lesson.objects.filter(status=Status.PUBLISHED).count(),
        "lessons_draft": Lesson.objects.filter(status=Status.DRAFT).count(),
    }


def _visible_lessons() -> QuerySet[Lesson]:
    return Lesson.objects.filter(
        status=Status.PUBLISHED,
        is_active=True,
        chapter__is_active=True,
        chapter__deleted_at__isnull=True,
        course__in=public_courses(),
    ).select_related("course")


def _outline(course: Course) -> list[Chapter]:
    lessons = _visible_lessons().filter(course=course).order_by("sort_order", "id")
    return list(
        course.chapters.filter(is_active=True, deleted_at__isnull=True)
        .prefetch_related(Prefetch("lessons", queryset=lessons, to_attr="visible_lessons"))
        .order_by("sort_order", "id")
    )


# --- used by the learning and certification modules ------------------------


def visible_lesson(lesson_id: int) -> Lesson | None:
    """A lesson a visitor can open, with its course."""
    return _visible_lessons().filter(pk=lesson_id).first()


def visible_lesson_ids(course_id: int) -> set[int]:
    return set(_visible_lessons().filter(course_id=course_id).values_list("pk", flat=True))


def get_lesson(lesson_id: int) -> Lesson | None:
    """A live lesson, drafts included (for admin tools)."""
    return Lesson.objects.filter(pk=lesson_id).first()


def lesson_has_blocks(lesson_id: int) -> bool:
    return LessonBlock.objects.filter(lesson_id=lesson_id).exists()


def category_exists(category_id: int) -> bool:
    return Category.objects.filter(pk=category_id).exists()


def course_exists(course_id: int) -> bool:
    return Course.objects.filter(pk=course_id).exists()


def course_summaries(course_ids) -> dict[int, dict]:
    """{course_id: {"title", "slug"}} for live courses."""
    rows = Course.objects.filter(pk__in=list(course_ids)).values("pk", "title", "slug")
    return {row["pk"]: {"title": row["title"], "slug": row["slug"]} for row in rows}


def lesson_links(lesson_ids) -> dict[int, dict]:
    """{lesson_id: {"title", "slug", "course_slug"}} for visible lessons."""
    lessons = _visible_lessons().filter(pk__in=[i for i in lesson_ids if i])
    return {
        lesson.pk: {"title": lesson.title, "slug": lesson.slug, "course_slug": lesson.course.slug}
        for lesson in lessons
    }


def lesson_assessment_ids(lesson_id: int) -> tuple[list[int], list[int]]:
    """(exercise ids, quiz ids) shown in a lesson's active blocks."""
    blocks = LessonBlock.objects.filter(lesson_id=lesson_id, is_active=True)
    rows = list(blocks.values_list("exercise_id", "quiz_id"))
    return [e for e, _ in rows if e], [q for _, q in rows if q]


def lesson_for_index(lesson_id: int) -> dict | None:
    """A visible lesson as plain text for the AI tutor's knowledge base. None if hidden."""
    lesson = visible_lesson(lesson_id)
    if lesson is None:
        return None
    parts = [f"# {lesson.title}", lesson.summary]
    blocks = (
        lesson.blocks.filter(is_active=True)
        .select_related("code_example")
        .order_by("sort_order", "id")
    )
    for block in blocks:
        if block.type in (LessonBlock.Type.MARKDOWN, LessonBlock.Type.CALLOUT):
            parts.append(block.content_md or "")
        elif block.type == LessonBlock.Type.EXAMPLE and block.code_example:
            example = block.code_example
            parts.append(
                f"Example ({example.language}):\n```{example.language}\n{example.starter_code}\n```"
            )
    return {
        "title": f"{lesson.title} · {lesson.course.title}",
        "url": f"/{lesson.course.slug}/{lesson.slug}",
        "course_id": lesson.course_id,
        "text": "\n\n".join(p for p in parts if p),
    }


def all_visible_lesson_ids() -> set[int]:
    return set(_visible_lessons().values_list("pk", flat=True))


# --- used by the seo module --------------------------------------------------


def find_page(course_slug: str, lesson_slug: str = "") -> tuple[str, int] | None:
    """("course" | "lesson", id) for a live course or lesson URL, drafts included."""
    course = Course.objects.filter(slug=course_slug).first()
    if course is None:
        return None
    if not lesson_slug:
        return ("course", course.pk)
    lesson = Lesson.objects.filter(course=course, slug=lesson_slug).first()
    return ("lesson", lesson.pk) if lesson else None


def page_urls(entity_type: str, ids) -> dict[int, str]:
    """{id: "/python" or "/python/lists"} for live courses or lessons, drafts included."""
    if entity_type == "course":
        rows = Course.objects.filter(pk__in=list(ids)).values_list("pk", "slug")
        return {pk: f"/{slug}" for pk, slug in rows}
    rows = Lesson.objects.filter(pk__in=list(ids)).values_list("pk", "course__slug", "slug")
    return {pk: f"/{course}/{lesson}" for pk, course, lesson in rows}


def sitemap_pages() -> list[dict]:
    """Every published course and lesson: {type, id, url, updated_at}."""
    pages = [
        {"type": "course", "id": c.pk, "url": f"/{c.slug}", "updated_at": c.updated_at}
        for c in public_courses()
    ]
    pages += [
        {
            "type": "lesson",
            "id": lesson.pk,
            "url": f"/{lesson.course.slug}/{lesson.slug}",
            "updated_at": lesson.updated_at,
        }
        for lesson in _visible_lessons().order_by("course_id", "sort_order")
    ]
    return pages
