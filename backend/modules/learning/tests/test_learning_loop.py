"""The whole Sprint 3 loop: lessons -> exercise -> final quiz -> points -> certificate."""

import pytest
from django.core import mail

from modules.assessment import services as assessment
from modules.catalog import services as catalog
from modules.catalog.models import Status
from modules.certification.models import Certificate
from modules.gamification.models import LearnerStats, UserBadge
from shared import jobs

pytestmark = pytest.mark.django_db
LEARNER = "/api/v1/learner"


@pytest.fixture
def course(make_user):
    """A published course: lesson 1 is text, lesson 2 has an exercise and the final quiz."""
    admin = make_user("author@example.com", "author")
    category = catalog.save_category(None, {"name": "Python"}, admin)
    course = catalog.save_course(
        None, {"category": category, "title": "Python", "status": Status.PUBLISHED}, admin
    )
    chapter = catalog.save_chapter(None, {"course": course, "title": "Basics"}, admin)
    intro, practice = (
        catalog.save_lesson(
            None, {"chapter": chapter, "title": t, "status": Status.PUBLISHED}, admin
        )
        for t in ("Intro", "Practice")
    )
    catalog.save_block(None, {"lesson": intro, "type": "markdown", "content_md": "Hi"}, admin)
    exercise_block = catalog.save_block(None, {
        "lesson": practice, "type": "exercise",
        "exercise": {"prompt_md": "Print hello", "language": "python", "starter_code": "",
                     "check_type": "output", "expected_value": "hello"},
    }, admin)  # fmt: skip
    quiz = assessment.save_quiz(
        None, {"course_id": course.pk, "title": "Final", "is_final": True}, admin
    )
    questions = {
        "2 + 2?": [("4", True), ("5", False)],
        "Is 0 falsy?": [("Yes", True), ("No", False)],
    }
    for text, options in questions.items():
        assessment.save_question(None, {
            "quiz": quiz, "question_text": text,
            "options": [{"option_text": o, "is_correct": c} for o, c in options],
        }, admin)  # fmt: skip
    catalog.save_block(None, {"lesson": practice, "type": "quiz", "quiz_id": quiz.pk}, admin)
    return {"course": course, "intro": intro, "practice": practice, "quiz": quiz,
            "exercise_id": exercise_block.exercise_id}  # fmt: skip


def _answers(quiz, all_correct=True):
    answers = {}
    for question in quiz.questions.all():
        options = list(question.options.all())
        pick = [o for o in options if o.is_correct == all_correct] or options
        answers[str(question.pk)] = [pick[0].pk]
    return answers


def test_learner_finishes_course_and_gets_certificate(api, make_user, course):
    learner = make_user()
    api.force_authenticate(learner)

    first = api.post(f"{LEARNER}/lessons/{course['intro'].pk}/complete/").json()
    assert first["progress_percent"] == 50 and not first["course_completed"]

    exercise = f"{LEARNER}/exercises/{course['exercise_id']}/submit/"
    assert api.post(exercise, {"code": "print('hi')", "output": "hi"}).json()["is_correct"] is False
    assert api.post(exercise, {"code": "print('hello')", "output": "hello\n"}).json()["is_correct"]
    api.post(exercise, {"code": "print('hello')", "output": "hello"})  # no second award

    second = api.post(f"{LEARNER}/lessons/{course['practice'].pk}/complete/").json()
    assert second["progress_percent"] == 100 and not second["course_completed"]  # quiz pending

    quiz_url = f"{LEARNER}/quizzes/{course['quiz'].pk}/attempts/"
    failed = api.post(quiz_url, {"answers": _answers(course["quiz"], False)}, format="json").json()
    assert failed["passed"] is False and failed["percentage"] == 0
    passed = api.post(quiz_url, {"answers": _answers(course["quiz"])}, format="json").json()
    assert passed["passed"] and passed["just_completed"] and passed["course_completed"]

    stats = LearnerStats.objects.get(user=learner)
    assert (
        stats.total_points == 10 + 15 + 10 + 50 + 20 + 200
    )  # lessons, exercise, quiz, perfect, course
    assert (stats.lessons_completed, stats.courses_completed, stats.current_streak) == (2, 1, 1)
    badges = set(UserBadge.objects.filter(user=learner).values_list("badge__slug", flat=True))
    assert badges == {"first-steps", "course-finisher"}

    cert = Certificate.objects.get(user=learner)
    jobs.run_pending()
    cert.refresh_from_db()
    assert cert.pdf_path.endswith(".pdf") and cert.image_path.endswith(".png")
    assert "Your ainolez certificate" in mail.outbox[-1].subject

    public = api.get(f"/api/v1/public/certificates/{cert.certificate_code}/").json()
    assert (public["status"], public["course_title"]) == ("issued", "Python")
    share = api.get(f"/share/certificates/{cert.certificate_code}/").content.decode()
    assert 'property="og:image"' in share and "completed Python" in share

    dashboard = api.get(f"{LEARNER}/dashboard/").json()
    assert dashboard["courses"][0]["status"] == "completed"
    assert dashboard["certificates"][0]["code"] == cert.certificate_code


def test_completing_a_lesson_twice_gives_points_once(api, make_user, course):
    learner = make_user()
    api.force_authenticate(learner)
    for _ in range(2):
        api.post(f"{LEARNER}/lessons/{course['intro'].pk}/complete/")
    assert LearnerStats.objects.get(user=learner).total_points == 10


def test_public_lesson_never_shows_answers(api, course):
    page = api.get(f"/api/v1/public/courses/python/lessons/{course['practice'].slug}/").json()
    quiz = next(b["quiz"] for b in page["blocks"] if b["type"] == "quiz")
    exercise = next(b["exercise"] for b in page["blocks"] if b["type"] == "exercise")
    assert "is_correct" not in str(quiz) and "expected_value" not in exercise


def test_visitors_cannot_submit(api, course):
    assert api.post(f"{LEARNER}/lessons/{course['intro'].pk}/complete/").status_code == 401


def test_admin_can_revoke_a_certificate(api, admin_api, make_user, course):
    learner = make_user("amina@example.com", "amina", full_name="Amina Rahman")
    api.force_authenticate(learner)
    for lesson in (course["intro"], course["practice"]):
        api.post(f"{LEARNER}/lessons/{lesson.pk}/complete/")
    quiz_url = f"{LEARNER}/quizzes/{course['quiz'].pk}/attempts/"
    api.post(quiz_url, {"answers": _answers(course["quiz"])}, format="json")
    cert = Certificate.objects.get(user=learner)
    assert cert.learner_name == "Amina Rahman"

    url = f"/api/v1/admin/certification/certificates/{cert.pk}"
    assert admin_api.post(f"{url}/revoke/", {"reason": ""}).json()["code"] == "reason_required"
    admin_api.post(f"{url}/revoke/", {"reason": "Copied answers"})
    public = api.get(f"/api/v1/public/certificates/{cert.certificate_code}/").json()
    assert (public["status"], public["revoke_reason"]) == ("revoked", "Copied answers")


def test_leaderboard_hides_learners_who_opted_out(api, make_user, course):
    learner = make_user(full_name="Amina")
    api.force_authenticate(learner)
    api.post(f"{LEARNER}/lessons/{course['intro'].pk}/complete/")
    board = api.get("/api/v1/public/leaderboard/?period=week").json()["leaders"]
    assert board == [{"rank": 1, "name": "Amina", "points": 10}]

    api.patch("/api/v1/auth/me/", {"show_on_leaderboard": False}, format="json")
    assert api.get("/api/v1/public/leaderboard/").json()["leaders"] == []
