"""The AI tutor, with the Claude API call replaced by a fake (no network, no cost)."""

import uuid

import pytest

from modules.assistant import claude, knowledge
from modules.assistant.models import FAQ, AISettings, KBChunk, Message, UsageDaily
from modules.catalog import services as catalog
from shared import jobs

API = "/api/v1/assistant"
SESSION = str(uuid.uuid4())


@pytest.fixture
def fake_claude(monkeypatch):
    """Records every call and answers with a fixed reply."""
    calls = []

    def complete(**kwargs):
        calls.append(kwargs)
        return claude.ModelReply(
            text="Lists keep items in order [1].",
            model=kwargs["model"],
            tokens_in=900,
            tokens_out=40,
            cached_tokens=0,
            cost=0.0044,
            latency_ms=12,
            refused=False,
            cut_short=False,
        )

    monkeypatch.setattr(claude, "complete", complete)
    return calls


@pytest.fixture
def lesson(make_user):
    author = make_user("author@example.com", "author")
    category = catalog.save_category(None, {"name": "Python"}, author)
    course = catalog.save_course(
        None, {"category": category, "title": "Python", "status": "published"}, author
    )
    chapter = catalog.save_chapter(None, {"course": course, "title": "Basics"}, author)
    lesson = catalog.save_lesson(
        None, {"chapter": chapter, "title": "Lists", "status": "published"}, author
    )
    catalog.save_block(
        None,
        {
            "lesson": lesson,
            "type": "markdown",
            "content_md": "A list stores many values. Use append to add an item to the list.",
        },
        author,
    )
    jobs.run_pending()  # LessonChanged -> index job
    lesson.author = author
    return lesson


def _ask(api, question, **extra):
    return api.post(
        f"{API}/messages/",
        {"question": question, **extra},
        format="json",
        HTTP_X_CHAT_SESSION=SESSION,
    )


@pytest.mark.django_db
def test_editing_a_lesson_reindexes_it(lesson):
    assert "append" in KBChunk.objects.get(lesson_id=lesson.pk).text
    block = lesson.blocks.get()
    catalog.save_block(
        block, {"content_md": "Tuples cannot change after you create them."}, lesson.author
    )
    jobs.run_pending()
    assert "Tuples" in KBChunk.objects.get(lesson_id=lesson.pk).text


@pytest.mark.django_db
def test_hidden_lessons_leave_the_knowledge_base(lesson):
    lesson.status = "draft"
    lesson.save()
    knowledge.index_lesson(lesson.pk)
    assert not KBChunk.objects.exists()


# FULLTEXT only sees committed rows.
def test_answer_uses_the_open_lesson_and_cites_it(committed_db, api, fake_claude, lesson):
    response = _ask(
        api,
        "How do I add something to a list?",
        lesson_id=lesson.pk,
        code="xs = []",
        language="python",
    )
    answer = response.json()["answer"]
    assert answer["answered_by"] == "model"
    assert answer["sources"] == [{"title": "Lists · Python", "url": "/python/lists"}]

    prompt = fake_claude[0]["messages"][-1]["content"]
    assert "Use append to add an item" in prompt
    assert '<learner_code language="python">' in prompt
    assert fake_claude[0]["model"] == "claude-opus-5-5"
    assert UsageDaily.objects.get().tokens_in == 900

    # The follow-up continues the same conversation and sends the history.
    _ask(api, "And how do I remove one?", conversation_id=response.json()["conversation_id"])
    history = fake_claude[1]["messages"]
    assert [m["role"] for m in history] == ["user", "assistant", "user"]


@pytest.mark.django_db
def test_curated_faq_answers_without_calling_the_model(api, fake_claude):
    FAQ.objects.create(
        question="Is ainolez free?", answer_md="Yes, always.", answer_html="<p>Yes, always.</p>"
    )
    answer = _ask(api, "is ainolez free").json()["answer"]
    assert (answer["answered_by"], answer["content_html"]) == ("faq", "<p>Yes, always.</p>")
    assert fake_claude == []


@pytest.mark.django_db
def test_visitor_daily_limit(api, fake_claude):
    AISettings.objects.filter(pk=1).update(visitor_daily_limit=1)
    first = _ask(api, "What is HTML?").json()
    second = _ask(api, "What is CSS?", conversation_id=first["conversation_id"]).json()
    assert "limit" in second["answer"]["content_html"]
    assert len(fake_claude) == 1


@pytest.mark.django_db
def test_monthly_budget_pauses_the_tutor(api, fake_claude):
    AISettings.objects.filter(pk=1).update(monthly_token_budget=100)
    UsageDaily.objects.create(
        date=__import__("datetime").date.today(), model="m", audience="visitor", tokens_in=100
    )
    assert _ask(api, "Hello?").json()["answer"]["answered_by"] == "system"
    assert fake_claude == []


@pytest.mark.django_db
def test_visitors_cannot_read_other_peoples_chats(api, fake_claude):
    conversation_id = _ask(api, "What is HTML?").json()["conversation_id"]
    other = api.get(
        f"{API}/conversations/{conversation_id}/", HTTP_X_CHAT_SESSION=str(uuid.uuid4())
    )
    assert other.status_code == 404
    mine = api.get(f"{API}/conversations/{conversation_id}/", HTTP_X_CHAT_SESSION=SESSION).json()
    assert len(mine["messages"]) == 2


@pytest.mark.django_db
def test_feedback(api, fake_claude):
    answer = _ask(api, "What is HTML?").json()["answer"]
    api.post(
        f"{API}/messages/{answer['id']}/feedback/", {"value": "down"}, HTTP_X_CHAT_SESSION=SESSION
    )
    assert Message.objects.get(pk=answer["id"]).feedback == "down"


@pytest.mark.django_db
def test_switched_off_for_visitors(api, fake_claude):
    AISettings.objects.filter(pk=1).update(enabled_for_visitors=False)
    assert _ask(api, "Hi").json()["code"] == "ai_disabled"


@pytest.mark.django_db
def test_admin_can_switch_model_and_roll_back_the_prompt(admin_api):
    response = admin_api.patch(
        "/api/v1/admin/assistant/settings/", {"model": "claude-haiku-5-5"}, format="json"
    )
    assert response.json()["model"] == "claude-haiku-5-5"
    assert (
        admin_api.patch(
            "/api/v1/admin/assistant/settings/", {"model": "gpt-x"}, format="json"
        ).status_code
        == 400
    )

    admin_api.post(
        "/api/v1/admin/assistant/prompts/",
        {"system_prompt": "You are a pirate tutor. Arr, explain code."},
    )
    versions = admin_api.get("/api/v1/admin/assistant/prompts/").json()
    assert [(v["version_no"], v["is_current"]) for v in versions] == [(2, True), (1, False)]
    admin_api.post(f"/api/v1/admin/assistant/prompts/{versions[1]['id']}/activate/")
    assert admin_api.get("/api/v1/admin/assistant/prompts/").json()[1]["is_current"]
