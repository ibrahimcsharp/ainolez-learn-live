import pytest

from modules.assessment import services
from modules.assessment.models import Exercise, QuizQuestion
from shared.exceptions import ServiceError


@pytest.mark.parametrize(
    "check_type, expected, code, output, correct",
    [
        ("output", "hello", "", "hello  \n\n", True),  # trailing spaces and blank lines ignored
        ("output", "hello", "", "Hello", False),
        ("exact", "x = 1", " x = 1 \n", "", True),
        ("contains", "<h1>", "<body><h1>Hi</h1></body>", "", True),
        ("regex", r"for \w+ in", "for item in items:", "", True),
        ("regex", r"^print\(", "x = 1", "", False),
    ],
)
def test_check_exercise(check_type, expected, code, output, correct):
    exercise = Exercise(check_type=check_type, expected_value=expected)
    assert services.check_exercise(exercise, code, output)[0] is correct


@pytest.mark.parametrize(
    "question_type, options",
    [
        ("single", [{"option_text": "a", "is_correct": True}]),  # only one option
        ("single", [{"option_text": "a"}, {"option_text": "b"}]),  # none correct
        (
            "single",
            [{"option_text": "a", "is_correct": True}, {"option_text": "b", "is_correct": True}],
        ),
    ],
)
def test_question_options_are_validated(question_type, options):
    with pytest.raises(ServiceError):
        services._check_options(question_type, options)


def test_multiple_choice_allows_several_correct_options():
    options = [{"option_text": t, "is_correct": True} for t in ("a", "b")]
    services._check_options(QuizQuestion.Type.MULTIPLE, options)
