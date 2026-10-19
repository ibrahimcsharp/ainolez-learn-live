"""The AI course generator, with the Claude API call replaced by a fake."""

import json

import pytest

from modules.ai_authoring.models import CourseJob
from modules.assessment.models import Quiz
from modules.assistant import claude
from modules.catalog import services as catalog
from modules.catalog.models import Course, LessonBlock
from shared import jobs
from shared.exceptions import ServiceError

API = "/api/v1/admin/ai-authoring/jobs"
OUTLINE = {
    "title": "Python for Absolute Beginners",
    "short_description": "Your first steps in Python.",
    "description": "Write and run Python in the browser.",
    "chapters": [
        {"title": "Getting started", "description": "Hello", "lessons": [
            {"title": "Print", "summary": "Show text."},
            {"title": "Variables", "summary": "Store values."},
        ]},
    ],
}  # fmt: skip
LESSON = {
    "summary": "Show text with print().",
    "minutes": 6,
    "markdown": (
        "## Your first line\n\nUse print.\n\n```python tryit\nprint('Hi')\n```\n\n"
        "## Summary\n\n- print shows text"
    ),
    "exercise": {
        "title": "Say hello",
        "prompt_md": "Print `Hello`.",
        "starter_code": "# your code",
        "solution_code": "print('Hello')",
        "check_type": "output",
        "expected_value": "Hello",
        "hint": "Use print().",
    },
    "quiz": [
        {"question": "What shows text?", "options": ["print", "show"], "correct_index": 0,
         "explanation": "print writes output."},
        {"question": "Broken", "options": ["only one"], "correct_index": 0, "explanation": ""},
    ],
}  # fmt: skip


@pytest.fixture
def fake_claude(monkeypatch):
    calls = []

    def complete(**kwargs):
        calls.append(kwargs)
        is_outline = "chapters" in kwargs["json_schema"]["properties"]
        return claude.ModelReply(
            text=json.dumps(OUTLINE if is_outline else LESSON),
            model=kwargs["model"],
            tokens_in=1000,
            tokens_out=500,
            cached_tokens=0,
            cost=0.01,
            latency_ms=5,
            refused=False,
            cut_short=False,
        )

    monkeypatch.setattr(claude, "complete", complete)
    return calls


@pytest.fixture
def category(make_user):
    return catalog.save_category(None, {"name": "Python"}, make_user("a@example.com", "author"))


@pytest.mark.django_db
def test_outline_edit_and_lessons_become_draft_content(admin_api, fake_claude, category):
    started = admin_api.post(
        API + "/", {"topic": "Python basics", "chapters_count": 1}, format="json"
    )
    assert started.status_code == 201, started.json()
    job_id = started.json()["id"]
    jobs.run_pending()
    job = admin_api.get(f"{API}/{job_id}/").json()
    assert job["status"] == "outline_ready" and fake_claude[0]["thinking"] is True

    outline = job["outline"]
    outline["chapters"][0]["lessons"][1]["title"] = "Variables and names"
    assert (
        admin_api.patch(f"{API}/{job_id}/outline/", {"outline": outline}, format="json").status_code
        == 200
    )
    assert admin_api.post(f"{API}/{job_id}/generate/").status_code == 400  # no category yet
    admin_api.patch(f"{API}/{job_id}/", {"category_id": category.pk}, format="json")
    assert admin_api.post(f"{API}/{job_id}/generate/").status_code == 202
    jobs.run_pending()

    job = CourseJob.objects.get(pk=job_id)
    assert (job.status, job.lessons_done, job.tokens_in) == ("drafted", 2, 3000)
    course = Course.objects.get(pk=job.course_id)
    assert course.status == "draft" and course.ai_generated
    lesson = course.lessons.get(title="Variables and names")
    assert (
        lesson.ai_generated
        and lesson.status == "draft"
        and lesson.summary == "Show text with print()."
    )
    types = list(
        LessonBlock.objects.filter(lesson=lesson)
        .order_by("sort_order")
        .values_list("type", flat=True)
    )
    assert types == ["markdown", "example", "markdown", "exercise", "quiz"]
    quiz = Quiz.objects.get(course_id=course.pk, title="Quiz: Variables and names")
    assert quiz.questions.count() == 1  # the broken question was dropped


@pytest.mark.django_db
def test_a_failed_outline_can_be_retried(admin_api, monkeypatch, category):
    def busy(**kwargs):
        raise ServiceError("The AI tutor is busy right now.", "ai_busy", 503)

    monkeypatch.setattr(claude, "complete", busy)
    job_id = admin_api.post(API + "/", {"topic": "SQL"}, format="json").json()["id"]
    jobs.run_pending()
    job = CourseJob.objects.get(pk=job_id)
    assert job.status == "failed" and "busy" in job.error
    assert admin_api.post(f"{API}/{job_id}/retry/").json()["status"] == "outline_queued"


@pytest.mark.django_db
def test_bad_requests_are_refused(admin_api, api):
    assert admin_api.post(API + "/", {"topic": ""}, format="json").status_code == 400
    assert (
        admin_api.post(API + "/", {"topic": "x", "chapters_count": 40}, format="json").status_code
        == 400
    )
    assert api.post(API + "/", {"topic": "x"}, format="json").status_code == 401
