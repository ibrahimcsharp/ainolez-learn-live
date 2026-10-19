from dataclasses import dataclass


@dataclass(frozen=True)
class LessonChanged:
    """A lesson or one of its blocks was created, edited, hidden, trashed or restored."""

    lesson_id: int


@dataclass(frozen=True)
class CourseChanged:
    """A course or one of its chapters was created, edited, hidden, trashed or restored."""

    course_id: int
