"""Build exercises and quizzes, and grade a learner's answers."""

import re
from dataclasses import dataclass, field

from django.db import transaction
from django.db.models import Max

from modules.assessment.models import LANGUAGES, Exercise, Quiz, QuizOption, QuizQuestion
from modules.catalog import selectors as catalog
from modules.content_tools import services as content
from shared import audit
from shared.exceptions import ServiceError

EXERCISE_FIELDS = (
    "title", "prompt_md", "language", "starter_code", "solution_code",
    "check_type", "expected_value", "hint",
)  # fmt: skip


@dataclass
class QuizResult:
    score: int
    total_points: int
    percentage: float
    passed: bool
    # {question_id: {"correct": bool, "correct_option_ids": [...], "explanation": str}}
    questions: dict = field(default_factory=dict)


def save_exercise(exercise: Exercise | None, data: dict, by) -> Exercise:
    exercise = exercise or Exercise()
    for name in EXERCISE_FIELDS:
        if name in data:
            setattr(exercise, name, data[name])
    if exercise.language not in LANGUAGES:
        raise ServiceError("Pick the exercise language.", "bad_language")
    if not exercise.prompt_md.strip() or not exercise.expected_value.strip():
        raise ServiceError(
            "An exercise needs a task and an expected answer.", "incomplete_exercise"
        )
    if exercise.check_type == Exercise.CheckType.REGEX:
        try:
            re.compile(exercise.expected_value)
        except re.error as exc:
            raise ServiceError(f"The pattern is not a valid regex: {exc}", "bad_regex") from exc
    exercise.prompt_html = content.render_markdown(exercise.prompt_md)
    return _save(exercise, by)


def save_quiz(quiz: Quiz | None, data: dict, by) -> Quiz:
    quiz = quiz or Quiz()
    for name, value in data.items():
        setattr(quiz, name, value)
    if not catalog.course_exists(quiz.course_id):
        raise ServiceError("Pick an existing course for this quiz.", "bad_course")
    return _save(quiz, by)


def save_question(question: QuizQuestion | None, data: dict, by) -> QuizQuestion:
    """data["options"] (when given) replaces the options: [{"option_text", "is_correct"}]."""
    options = data.pop("options", None)
    is_new = question is None
    question = question or QuizQuestion()
    for name, value in data.items():
        setattr(question, name, value)
    if options is not None:
        _check_options(question.question_type, options)
    if is_new:
        siblings = QuizQuestion.objects.filter(quiz=question.quiz)
        question.sort_order = (siblings.aggregate(m=Max("sort_order"))["m"] or 0) + 1
    with transaction.atomic():
        _save(question, by)
        if options is not None:
            question.options.all().delete()
            QuizOption.objects.bulk_create(
                QuizOption(question=question, option_text=o["option_text"],
                           is_correct=bool(o.get("is_correct")), sort_order=i)
                for i, o in enumerate(options)
            )  # fmt: skip
    return question


def check_exercise(exercise: Exercise, code: str, output: str) -> tuple[bool, str]:
    """Compare the learner's code (or what it printed) with the expected value."""
    expected = exercise.expected_value.strip()
    kind = exercise.check_type
    if kind == Exercise.CheckType.OUTPUT:
        correct = _lines(output) == _lines(expected)
    elif kind == Exercise.CheckType.EXACT:
        correct = _lines(code) == _lines(expected)
    elif kind == Exercise.CheckType.CONTAINS:
        correct = expected in code
    else:
        correct = re.search(expected, code, re.MULTILINE) is not None
    return (
        correct,
        "Correct, well done!" if correct else "Not quite yet. Check your code and try again.",
    )


def grade_quiz(quiz: Quiz, answers: dict) -> QuizResult:
    """answers: {question_id: [option ids]}. A question scores only if exactly right."""
    questions = quiz.questions.filter(is_active=True).prefetch_related("options")
    result = QuizResult(score=0, total_points=0, percentage=0.0, passed=False)
    for question in questions:
        right = {o.pk for o in question.options.all() if o.is_correct}
        chosen = {int(i) for i in answers.get(str(question.pk), answers.get(question.pk, []))}
        correct = bool(right) and chosen == right
        result.total_points += question.points
        result.score += question.points if correct else 0
        result.questions[question.pk] = {
            "correct": correct,
            "correct_option_ids": sorted(right),
            "explanation": question.explanation,
        }
    if result.total_points:
        result.percentage = round(100 * result.score / result.total_points, 2)
    result.passed = result.total_points > 0 and result.percentage >= quiz.pass_percentage
    return result


def _check_options(question_type: str, options: list[dict]) -> None:
    correct = sum(1 for o in options if o.get("is_correct"))
    if len(options) < 2 or any(not str(o.get("option_text", "")).strip() for o in options):
        raise ServiceError("Give at least two answer options, none of them empty.", "bad_options")
    if correct == 0:
        raise ServiceError("Mark at least one option as correct.", "bad_options")
    if question_type != QuizQuestion.Type.MULTIPLE and correct != 1:
        raise ServiceError("This question type needs exactly one correct option.", "bad_options")


def _lines(text: str) -> list[str]:
    """Text as lines with trailing spaces and blank edges removed, for fair comparing."""
    return [line.rstrip() for line in (text or "").strip().splitlines()]


def _save(obj, by):
    is_new = obj.pk is None
    if is_new:
        obj.created_by = by
    obj.updated_by = by
    obj.save()
    audit.record(
        f"{obj._meta.model_name}.{'created' if is_new else 'updated'}", actor=by, entity=obj
    )
    return obj
