"""Events the learning module publishes. Gamification and certification react to them."""

from dataclasses import dataclass


@dataclass(frozen=True)
class LessonCompleted:
    user_id: int
    lesson_id: int
    course_id: int


@dataclass(frozen=True)
class ExerciseSolved:
    """Published only the first time a learner solves an exercise."""

    user_id: int
    exercise_id: int


@dataclass(frozen=True)
class QuizPassed:
    user_id: int
    quiz_id: int
    percentage: float


@dataclass(frozen=True)
class CourseCompleted:
    user_id: int
    course_id: int
