"""Read queries about a learner's progress."""

from django.db.models import Count, Q

from modules.learning.models import Enrollment, ExerciseSubmission, LessonProgress, QuizAttempt
from shared.stats import daily_counts, first_day


def course_progress(user, course_id: int) -> dict:
    enrollment = Enrollment.objects.filter(user=user, course_id=course_id).first()
    return {
        "enrolled": enrollment is not None,
        "progress_percent": enrollment.progress_percent if enrollment else 0,
        "completed": bool(enrollment and enrollment.status == Enrollment.Status.COMPLETED),
        "last_lesson_id": enrollment.last_lesson_id if enrollment else None,
        "completed_lesson_ids": sorted(
            LessonProgress.objects.filter(user=user, course_id=course_id).values_list(
                "lesson_id", flat=True
            )
        ),
    }


def enrollments(user) -> list[Enrollment]:
    return list(Enrollment.objects.filter(user=user).order_by("-updated_at"))


def solved_exercise_ids(user, exercise_ids) -> set[int]:
    return set(
        ExerciseSubmission.objects.filter(
            user=user, exercise_id__in=list(exercise_ids), is_correct=True
        ).values_list("exercise_id", flat=True)
    )


def best_quiz_results(user, quiz_ids) -> dict[int, dict]:
    """{quiz_id: {"percentage", "passed", "attempts"}} for quizzes the learner tried."""
    best: dict[int, dict] = {}
    for attempt in QuizAttempt.objects.filter(user=user, quiz_id__in=list(quiz_ids)):
        current = best.setdefault(
            attempt.quiz_id, {"percentage": 0, "passed": False, "attempts": 0}
        )
        current["attempts"] += 1
        current["percentage"] = max(current["percentage"], float(attempt.percentage))
        current["passed"] = current["passed"] or attempt.passed
    return best


def activity_by_day(days: int) -> dict[str, dict[str, int]]:
    """Per-day counts of enrolments, finished lessons and finished courses."""
    return {
        "enrolments": daily_counts(Enrollment.objects.all(), "started_at", days),
        "lessons_completed": daily_counts(LessonProgress.objects.all(), "completed_at", days),
        "courses_completed": daily_counts(Enrollment.objects.all(), "completed_at", days),
    }


def top_courses(days: int, limit: int = 10) -> list[dict]:
    """Courses with the most enrolments in the period, with their completions."""
    since = Q(started_at__date__gte=first_day(days))
    rows = (
        Enrollment.objects.values("course_id")
        .annotate(
            enrolments=Count("pk", filter=since),
            completions=Count("pk", filter=Q(completed_at__date__gte=first_day(days))),
            learners=Count("pk"),
        )
        .filter(enrolments__gt=0)
        .order_by("-enrolments")[:limit]
    )
    return list(rows)
