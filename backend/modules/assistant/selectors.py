from datetime import timedelta

from django.db.models import Count, Q, Sum
from django.utils import timezone

from modules.assistant.models import Conversation, Message, UsageDaily


def public_config(config) -> dict:
    return {
        "enabled": config.enabled,
        "enabled_for_visitors": config.enabled_for_visitors,
        "bot_name": config.bot_name,
        "welcome_message": config.welcome_message,
        "starter_questions": config.starter_questions,
    }


def message_dict(message: Message) -> dict:
    return {
        "id": message.pk,
        "role": message.role,
        "content_html": message.content_html,
        "answered_by": message.answered_by,
        "sources": message.sources or [],
        "feedback": message.feedback,
        "created_at": message.created_at,
    }


def conversation_messages(conversation: Conversation) -> list[dict]:
    return [message_dict(m) for m in conversation.messages.order_by("id")]


def recent_conversations(only_negative: bool = False, limit: int = 100) -> list[dict]:
    rows = Conversation.objects.annotate(
        message_count=Count("messages"),
        thumbs_down=Count("messages", filter=Q(messages__feedback="down")),
    ).order_by("-updated_at")
    if only_negative:
        rows = rows.filter(thumbs_down__gt=0)
    return [
        {
            "id": c.pk,
            "title": c.title,
            "who": "learner" if c.user_id else "visitor",
            "message_count": c.message_count,
            "thumbs_down": c.thumbs_down,
            "updated_at": c.updated_at,
        }
        for c in rows[:limit]
    ]


def usage_report(days: int = 30) -> dict:
    since = timezone.now().date() - timedelta(days=days)
    rows = UsageDaily.objects.filter(date__gte=since).order_by("date", "model", "audience")
    month = UsageDaily.objects.filter(date__gte=timezone.now().date().replace(day=1)).aggregate(
        requests=Sum("requests"),
        tokens_in=Sum("tokens_in"),
        tokens_out=Sum("tokens_out"),
        cost=Sum("est_cost"),
    )
    return {
        "days": [
            {
                "date": r.date,
                "model": r.model,
                "audience": r.audience,
                "requests": r.requests,
                "tokens_in": r.tokens_in,
                "tokens_out": r.tokens_out,
                "est_cost": float(r.est_cost),
            }
            for r in rows
        ],
        "month": {k: float(v or 0) for k, v in month.items()},
        "feedback": {
            "up": Message.objects.filter(feedback="up").count(),
            "down": Message.objects.filter(feedback="down").count(),
        },
    }
