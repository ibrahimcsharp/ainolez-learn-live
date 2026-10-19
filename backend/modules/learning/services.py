"""
The learning loop: open a lesson, finish it, solve exercises, take quizzes.
A course is complete when every published lesson is done and every final
quiz is passed; that publishes CourseCompleted (points, certificate...).
"""

from dataclasses import dataclass

from django.db import IntegrityError, transaction
from django.utils import timezone

from modules.assessment import selectors as assessment_reads
from modules.assessment import services as assessment
from modules.catalog import selectors as catalog
from modules.learning.events import CourseCompleted, ExerciseSolved, LessonCompleted, QuizPassed
from modules.learning.models import Enrollment, ExerciseSubmission, LessonProgress, QuizAttempt
from shared.events import publish
from shared.exceptions import ServiceError


@dataclass
class CourseProgress:
    course_id: int
    progress_percent: int
    completed: bool
    just_completed: bool = False  # this action finished the course


def record_visit(user, lesson_id: int) -> None:
    """Remember the last lesson opened, so "Resume" can return to it."""
    lesson = _lesson(lesson_id)
    enrollment = _enrollment(user, lesson.course_id)
    if enrollment.last_lesson_id != lesson.pk:
        enrollment.last_lesson_id = lesson.pk
        enrollment.save(update_fields=["last_lesson_id", "updated_at"])


def complete_lesson(user, lesson_id: int) -> CourseProgress:
    lesson = _lesson(lesson_id)
    with transaction.atomic():
        _enrollment(user, lesson.course_id)
        try:
            with transaction.atomic():
                LessonProgress.objects.create(
                    user=user, lesson_id=lesson.pk, course_id=lesson.course_id
                )
        except IntegrityError:  # already completed: nothing new happens
            return _refresh_course(user, lesson.course_id)
        publish(LessonCompleted(user.pk, lesson.pk, lesson.course_id))
        return _refresh_course(user, lesson.course_id)


def submit_exercise(user, exercise_id: int, code: str, output: str) -> tuple[bool, str]:
    exercise = assessment_reads.get_exercise(exercise_id)
    if exercise is None:
        raise ServiceError("This exercise is not available.", "not_found", 404)
    correct, message = assessment.check_exercise(exercise, code, output)
    with transaction.atomic():
        solved_before = ExerciseSubmission.objects.filter(
            user=user, exercise_id=exercise.pk, is_correct=True
        ).exists()
        ExerciseSubmission.objects.create(
            user=user, exercise_id=exercise.pk, code=code, output=output, is_correct=correct
        )
        if correct and not solved_before:
            publish(ExerciseSolved(user.pk, exercise.pk))
    return correct, message


def submit_quiz(user, quiz_id: int, answers: dict) -> tuple[QuizAttempt, dict, CourseProgress]:
    """Returns the attempt, per-question feedback and the course progress."""
    quiz = assessment_reads.get_quiz(quiz_id)
    if quiz is None:
        raise ServiceError("This quiz is not available.", "not_found", 404)
    attempts = QuizAttempt.objects.filter(user=user, quiz_id=quiz.pk)
    if quiz.max_attempts and attempts.count() >= quiz.max_attempts:
        raise ServiceError("You have used all attempts for this quiz.", "no_attempts_left", 403)

    result = assessment.grade_quiz(quiz, answers)
    with transaction.atomic():
        passed_before = attempts.filter(passed=True).exists()
        attempt = QuizAttempt.objects.create(
            user=user, quiz_id=quiz.pk, score=result.score, total_points=result.total_points,
            percentage=result.percentage, passed=result.passed, answers=answers,
        )  # fmt: skip
        _enrollment(user, quiz.course_id)
        if result.passed and not passed_before:
            publish(QuizPassed(user.pk, quiz.pk, result.percentage))
        progress = _refresh_course(user, quiz.course_id)
    return attempt, result.questions, progress


def _refresh_course(user, course_id: int) -> CourseProgress:
    """Recalculate the course %, and complete the course when every rule is met."""
    enrollment = Enrollment.objects.select_for_update().get(user=user, course_id=course_id)
    lesson_ids = catalog.visible_lesson_ids(course_id)
    done = set(
        LessonProgress.objects.filter(user=user, course_id=course_id).values_list(
            "lesson_id", flat=True
        )
    )
    percent = round(100 * len(done & lesson_ids) / len(lesson_ids)) if lesson_ids else 0
    finals = assessment_reads.final_quiz_ids(course_id)
    passed = set(
        QuizAttempt.objects.filter(user=user, quiz_id__in=finals, passed=True).values_list(
            "quiz_id", flat=True
        )
    )
    finished = bool(lesson_ids) and lesson_ids <= done and set(finals) <= passed
    just_completed = finished and enrollment.status != Enrollment.Status.COMPLETED

    enrollment.progress_percent = percent
    if just_completed:
        enrollment.status = Enrollment.Status.COMPLETED
        enrollment.completed_at = timezone.now()
    enrollment.save(update_fields=["progress_percent", "status", "completed_at", "updated_at"])
    if just_completed:
        publish(CourseCompleted(user.pk, course_id))
    return CourseProgress(
        course_id, percent, enrollment.status == Enrollment.Status.COMPLETED, just_completed
    )


def _enrollment(user, course_id: int) -> Enrollment:
    enrollment, _ = Enrollment.objects.get_or_create(user=user, course_id=course_id)
    return enrollment


def _lesson(lesson_id: int):
    lesson = catalog.visible_lesson(lesson_id)
    if lesson is None:
        raise ServiceError("This lesson is not available.", "not_found", 404)
    return lesson
