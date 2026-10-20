"""
The AI tutor (PLANNING.md 6.6). One question goes through:
settings and limits -> curated FAQ -> knowledge-base excerpts -> Claude -> log and usage.
"""

import difflib
import json
import re
import uuid
from dataclasses import dataclass
from datetime import timedelta
from html import escape

from django.db import transaction
from django.db.models import F, Sum
from django.utils import timezone

from modules.assistant import claude, knowledge
from modules.assistant.models import (
    FAQ,
    AISettings,
    Conversation,
    KBSource,
    Message,
    PromptVersion,
    UsageDaily,
)
from modules.catalog import selectors as catalog
from modules.content_tools import services as content
from shared import audit, jobs
from shared.exceptions import ServiceError

HISTORY_TURNS = 6
FAQ_MATCH = 0.85  # how close a question must be to a curated one (0..1)
MAX_QUESTION = 2000
MAX_CODE = 8000


@dataclass
class Ask:
    question: str
    conversation_id: int | None = None
    lesson_id: int | None = None
    code: str = ""
    language: str = ""


def settings_row() -> AISettings:
    return AISettings.objects.get(pk=1)


def current_prompt() -> PromptVersion:
    return PromptVersion.objects.filter(is_current=True).order_by("-version_no").first()


def ask(user, session_key: str | None, request: Ask) -> Message:
    """Answer one question. Returns the tutor's reply message (already saved)."""
    question = request.question.strip()[:MAX_QUESTION]
    if not question:
        raise ServiceError("Ask a question first.", "empty")
    audience = _audience(user)
    config = settings_row()
    _check_allowed(config, audience)
    conversation = _conversation(user, session_key, request)

    _save(conversation, Message.Role.USER, question, Message.AnsweredBy.LEARNER)
    if _questions_today(user, session_key) > _daily_limit(config, audience):
        return _system_reply(
            conversation, "You have reached today's question limit. Come back tomorrow!"
        )
    if _over_budget(config):
        return _system_reply(
            conversation, "The tutor is resting for the rest of the month. Please check back later."
        )

    faq = _faq_match(question)
    if faq:
        FAQ.all_objects.filter(pk=faq.pk).update(hit_count=F("hit_count") + 1)
        return _save(
            conversation,
            Message.Role.ASSISTANT,
            faq.answer_md,
            Message.AnsweredBy.FAQ,
            html=faq.answer_html,
        )

    lesson = catalog.visible_lesson(request.lesson_id) if request.lesson_id else None
    excerpts = knowledge.search(question, lesson and lesson.pk, lesson and lesson.course_id)
    prompt = current_prompt()
    reply = claude.complete(
        model=config.model,
        effort=config.effort,
        max_tokens=config.max_output_tokens,
        system=prompt.system_prompt,
        messages=[
            *_history(conversation),
            {"role": "user", "content": _user_turn(question, request, lesson, excerpts)},
        ],
    )
    text = reply.text
    if reply.refused or not text:
        text = "Sorry, I can't help with that one. Try asking about a lesson or your code."
    elif reply.cut_short:
        text += "\n\n*(My answer was cut short. Ask me to continue.)*"
    _record_usage(reply, audience)
    return _save(
        conversation,
        Message.Role.ASSISTANT,
        text,
        Message.AnsweredBy.MODEL,
        sources=_unique_sources(excerpts),
        model=reply.model,
        prompt_version=prompt,
        tokens_in=reply.tokens_in,
        tokens_out=reply.tokens_out,
        cached_tokens=reply.cached_tokens,
        latency_ms=reply.latency_ms,
    )


def generate_json(*, system: str, prompt: str, schema: dict, max_tokens: int = 16000):
    """One structured Claude call for admin tools (the course generator).
    Uses the model from the AI settings; usage is logged as audience "admin".
    Returns (data, reply)."""
    config = settings_row()
    reply = claude.complete(
        model=config.model,
        effort="high",
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": prompt}],
        json_schema=schema,
        thinking=True,
    )
    _record_usage(reply, "admin")
    if reply.refused or reply.cut_short:
        raise ServiceError("Claude could not finish this draft. Try again or shorten it.", "ai_cut")
    return json.loads(reply.text), reply


def give_feedback(user, session_key: str | None, message_id: int, value: str) -> None:
    if value not in ("up", "down"):
        raise ServiceError("Feedback is up or down.", "bad_feedback")
    message = (
        Message.objects.select_related("conversation")
        .filter(pk=message_id, role=Message.Role.ASSISTANT)
        .first()
    )
    if message is None or not _owns(message.conversation, user, session_key):
        raise ServiceError("Message not found.", "not_found", 404)
    message.feedback = value
    message.save(update_fields=["feedback"])


def conversation_for(user, session_key: str | None, conversation_id: int) -> Conversation:
    conversation = Conversation.objects.filter(pk=conversation_id).first()
    if conversation is None or not _owns(conversation, user, session_key):
        raise ServiceError("Conversation not found.", "not_found", 404)
    return conversation


# --- admin ------------------------------------------------------------------

SETTING_FIELDS = (
    "enabled",
    "enabled_for_visitors",
    "enabled_for_learners",
    "course_generator_enabled",
    "bot_name",
    "welcome_message",
    "starter_questions",
    "model",
    "effort",
    "max_output_tokens",
    "visitor_daily_limit",
    "learner_daily_limit",
    "monthly_token_budget",
    "log_retention_days",
)


def update_settings(changes: dict, by) -> AISettings:
    config = settings_row()
    if changes.get("model", config.model) not in claude.MODELS:
        raise ServiceError("Pick one of the listed models.", "bad_model")
    for name in SETTING_FIELDS:
        if name in changes:
            setattr(config, name, changes[name])
    config.updated_by = by
    config.save()
    audit.record("aisettings.updated", actor=by, entity=config, after=changes)
    return config


def new_prompt_version(system_prompt: str, notes: str, make_current: bool, by) -> PromptVersion:
    if len(system_prompt.strip()) < 20:
        raise ServiceError("The prompt is too short.", "bad_prompt")
    latest = PromptVersion.objects.order_by("-version_no").first()
    version = PromptVersion.objects.create(
        version_no=(latest.version_no if latest else 0) + 1,
        system_prompt=system_prompt.strip(),
        notes=notes,
        created_by=by,
    )
    if make_current:
        activate_prompt(version, by)
    return version


def activate_prompt(version: PromptVersion, by) -> None:
    """Make this version the one in use (also how you roll back)."""
    with transaction.atomic():
        PromptVersion.objects.update(is_current=False)
        PromptVersion.objects.filter(pk=version.pk).update(is_current=True)
    audit.record("aiprompt.activated", actor=by, entity=version)


def save_faq(faq: FAQ | None, data: dict, by) -> FAQ:
    faq = faq or FAQ()
    for name, value in data.items():
        setattr(faq, name, value)
    faq.answer_html = content.render_markdown(faq.answer_md)
    is_new = faq.pk is None
    if is_new:
        faq.created_by = by
    faq.updated_by = by
    faq.save()
    audit.record(f"faq.{'created' if is_new else 'updated'}", actor=by, entity=faq)
    return faq


def save_document(source: KBSource | None, data: dict, by) -> KBSource:
    """Admins add knowledge as text or Markdown (e.g. site rules, a glossary)."""
    source = source or KBSource(type=KBSource.Type.DOCUMENT)
    if source.type != KBSource.Type.DOCUMENT:
        raise ServiceError(
            "Lesson sources follow their lesson; edit the lesson instead.", "read_only"
        )
    for name in ("title", "url", "body"):
        if name in data:
            setattr(source, name, data[name])
    if not (source.body or "").strip():
        raise ServiceError("A document needs some text.", "empty")
    source.status = KBSource.Status.PENDING
    if source.pk is None:
        source.created_by = by
    source.updated_by = by
    source.save()
    jobs.enqueue("assistant.index_source", {"source_id": source.pk})
    return source


def purge_old_logs() -> int:
    """Delete chats older than the retention period. Returns how many were removed."""
    cutoff = timezone.now() - timedelta(days=settings_row().log_retention_days)
    deleted, _ = Conversation.objects.filter(updated_at__lt=cutoff).delete()
    return deleted


# --- helpers ----------------------------------------------------------------


def _audience(user) -> str:
    if user and user.is_authenticated:
        return "admin" if user.is_super_admin else "learner"
    return "visitor"


def _check_allowed(config: AISettings, audience: str) -> None:
    allowed = config.enabled and (
        audience == "admin"
        or (audience == "learner" and config.enabled_for_learners)
        or (audience == "visitor" and config.enabled_for_visitors)
    )
    if not allowed:
        message = (
            "Log in to chat with the tutor."
            if audience == "visitor" and config.enabled
            else "The AI tutor is switched off."
        )
        raise ServiceError(message, "ai_disabled", 403)


def _conversation(user, session_key: str | None, request: Ask) -> Conversation:
    if request.conversation_id:
        return conversation_for(user, session_key, request.conversation_id)
    is_user = bool(user and user.is_authenticated)
    if not is_user and not _valid_session(session_key):
        raise ServiceError("Missing chat session.", "no_session")
    return Conversation.objects.create(
        user=user if is_user else None,
        session_key=None if is_user else session_key,
        lesson_id=request.lesson_id,
        title=request.question.strip()[:200],
    )


def _owns(conversation: Conversation, user, session_key: str | None) -> bool:
    if user and user.is_authenticated:
        return conversation.user_id == user.pk
    return (
        conversation.user_id is None
        and bool(session_key)
        and conversation.session_key == session_key
    )


def _valid_session(session_key: str | None) -> bool:
    try:
        return bool(session_key) and str(uuid.UUID(session_key)) == session_key
    except ValueError:
        return False


def _questions_today(user, session_key: str | None) -> int:
    today = Message.objects.filter(
        role=Message.Role.USER,
        created_at__gte=timezone.now().replace(hour=0, minute=0, second=0, microsecond=0),
    )
    if user and user.is_authenticated:
        return today.filter(conversation__user=user).count()
    return today.filter(conversation__session_key=session_key).count()


def _daily_limit(config: AISettings, audience: str) -> int:
    return {"visitor": config.visitor_daily_limit, "learner": config.learner_daily_limit}.get(
        audience, 10**9
    )


def _over_budget(config: AISettings) -> bool:
    if not config.monthly_token_budget:
        return False
    first = timezone.now().date().replace(day=1)
    # The budget pauses the tutor; admin tools (course generator) are counted apart.
    used = (
        UsageDaily.objects.filter(date__gte=first)
        .exclude(audience="admin")
        .aggregate(t=Sum(F("tokens_in") + F("tokens_out")))["t"]
    )
    return (used or 0) >= config.monthly_token_budget


def _faq_match(question: str) -> FAQ | None:
    wanted = _normalise(question)
    best, best_score = None, FAQ_MATCH
    for faq in FAQ.objects.filter(is_active=True):
        for phrasing in [faq.question, *faq.keywords.split("|")]:
            if phrasing.strip():
                score = difflib.SequenceMatcher(None, wanted, _normalise(phrasing)).ratio()
                if score >= best_score:
                    best, best_score = faq, score
    return best


def _normalise(text: str) -> str:
    return " ".join(re.findall(r"\w+", text.lower()))


def _history(conversation: Conversation) -> list[dict]:
    """The last few questions and answers, as plain text (no old excerpts)."""
    earlier = list(conversation.messages.order_by("-id")[1 : HISTORY_TURNS * 2 + 1])[::-1]
    turns = [{"role": m.role, "content": m.content} for m in earlier]
    while turns and turns[0]["role"] != "user":  # the API wants a user turn first
        turns.pop(0)
    return turns


def _user_turn(question: str, request: Ask, lesson, excerpts) -> str:
    parts = []
    if excerpts:
        body = "\n".join(
            f'<excerpt id="{i}" title="{escape(e.title)}" url="{escape(e.url)}">\n'
            f"{e.text}\n</excerpt>"
            for i, e in enumerate(excerpts, 1)
        )
        parts.append(f"ainolez lesson excerpts:\n<excerpts>\n{body}\n</excerpts>")
    if lesson:
        parts.append(f'The learner is reading the lesson "{lesson.title}".')
    if request.code.strip():
        language = re.sub(r"\W", "", request.language)[:20]
        parts.append(
            f'<learner_code language="{language}">\n{request.code[:MAX_CODE]}\n</learner_code>'
        )
    parts.append(f"Question: {question}")
    return "\n\n".join(parts)


def _unique_sources(excerpts) -> list[dict]:
    seen, sources = set(), []
    for excerpt in excerpts:
        if excerpt.url not in seen:
            seen.add(excerpt.url)
            sources.append({"title": excerpt.title, "url": excerpt.url})
    return sources


def _record_usage(reply: claude.ModelReply, audience: str) -> None:
    row, _ = UsageDaily.objects.get_or_create(
        date=timezone.now().date(), model=reply.model, audience=audience
    )
    UsageDaily.objects.filter(pk=row.pk).update(
        requests=F("requests") + 1,
        tokens_in=F("tokens_in") + reply.tokens_in,
        tokens_out=F("tokens_out") + reply.tokens_out,
        est_cost=F("est_cost") + round(reply.cost, 4),
    )


def _system_reply(conversation: Conversation, text: str) -> Message:
    return _save(conversation, Message.Role.ASSISTANT, text, Message.AnsweredBy.SYSTEM)


def _save(conversation, role, text, answered_by, html=None, **fields) -> Message:
    message = Message.objects.create(
        conversation=conversation,
        role=role,
        content=text,
        answered_by=answered_by,
        content_html=html if html is not None else content.render_markdown(text),
        **fields,
    )
    Conversation.objects.filter(pk=conversation.pk).update(updated_at=timezone.now())
    return message
