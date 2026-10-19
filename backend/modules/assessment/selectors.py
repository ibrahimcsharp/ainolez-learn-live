"""Read queries. The learner versions never include answers or solutions."""

from django.db.models import Prefetch

from modules.assessment.models import Exercise, Quiz, QuizQuestion


def get_exercise(exercise_id: int) -> Exercise | None:
    return Exercise.objects.filter(pk=exercise_id, is_active=True).first()


def get_quiz(quiz_id: int) -> Quiz | None:
    return Quiz.objects.filter(pk=quiz_id, is_active=True).first()


def final_quiz_ids(course_id: int) -> list[int]:
    return list(
        Quiz.objects.filter(course_id=course_id, is_final=True, is_active=True).values_list(
            "pk", flat=True
        )
    )


def exercises_for_learner(ids) -> dict[int, dict]:
    return {
        e.pk: {
            "id": e.pk,
            "title": e.title,
            "prompt_html": e.prompt_html,
            "language": e.language,
            "starter_code": e.starter_code,
            "hint": e.hint,
            "check_type": e.check_type,
        }
        for e in Exercise.objects.filter(pk__in=[i for i in ids if i], is_active=True)
    }


def exercise_for_admin(exercise_id: int | None) -> dict | None:
    exercise = Exercise.all_objects.filter(pk=exercise_id).first() if exercise_id else None
    if exercise is None:
        return None
    return {"id": exercise.pk, **{f: getattr(exercise, f) for f in (
        "title", "prompt_md", "prompt_html", "language", "starter_code", "solution_code",
        "check_type", "expected_value", "hint",
    )}}  # fmt: skip


def quizzes_for_learner(ids) -> dict[int, dict]:
    questions = QuizQuestion.objects.filter(is_active=True).order_by("sort_order", "id")
    quizzes = Quiz.objects.filter(pk__in=[i for i in ids if i], is_active=True).prefetch_related(
        Prefetch("questions", queryset=questions.prefetch_related("options"))
    )
    return {
        quiz.pk: {
            "id": quiz.pk,
            "title": quiz.title,
            "description": quiz.description,
            "is_final": quiz.is_final,
            "pass_percentage": quiz.pass_percentage,
            "questions": [
                {
                    "id": q.pk,
                    "text": q.question_text,
                    "type": q.question_type,
                    "code_snippet": q.code_snippet,
                    "points": q.points,
                    "options": [
                        {"id": o.pk, "text": o.option_text}
                        for o in sorted(q.options.all(), key=lambda o: o.sort_order)
                    ],
                }
                for q in quiz.questions.all()
            ],
        }
        for quiz in quizzes
    }
