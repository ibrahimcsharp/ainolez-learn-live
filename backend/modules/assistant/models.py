"""Tables from database/schema/0010_assistant.sql."""

from django.conf import settings
from django.db import models

from shared.models import BaseModel

USER = settings.AUTH_USER_MODEL


class AISettings(models.Model):
    """Singleton (id = 1): every switch of the AI control panel."""

    class Effort(models.TextChoices):
        LOW = "low"
        MEDIUM = "medium"
        HIGH = "high"

    enabled = models.BooleanField(default=True)
    enabled_for_visitors = models.BooleanField(default=True)
    enabled_for_learners = models.BooleanField(default=True)
    bot_name = models.CharField(max_length=60, default="ainolez AI")
    welcome_message = models.CharField(max_length=500, blank=True)
    starter_questions = models.JSONField(default=list)
    model = models.CharField(max_length=60, default="claude-opus-5-5")
    effort = models.CharField(max_length=10, choices=Effort, default=Effort.MEDIUM)
    max_output_tokens = models.IntegerField(default=2000)
    visitor_daily_limit = models.IntegerField(default=5)
    learner_daily_limit = models.IntegerField(default=50)
    monthly_token_budget = models.BigIntegerField(default=20_000_000)
    log_retention_days = models.IntegerField(default=180)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        USER, on_delete=models.SET_NULL, null=True, related_name="+", db_column="updated_by"
    )

    class Meta:
        managed = False
        db_table = "ai_settings"


class PromptVersion(models.Model):
    version_no = models.IntegerField(unique=True)
    system_prompt = models.TextField()
    notes = models.CharField(max_length=255, blank=True)
    is_current = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        USER, on_delete=models.SET_NULL, null=True, related_name="+", db_column="created_by"
    )

    class Meta:
        managed = False
        db_table = "ai_prompt_versions"


class FAQ(BaseModel):
    question = models.CharField(max_length=300)
    answer_md = models.TextField()
    answer_html = models.TextField()
    keywords = models.CharField(max_length=300, blank=True)  # other phrasings, separated by |
    hit_count = models.IntegerField(default=0)

    class Meta(BaseModel.Meta):
        managed = False
        db_table = "ai_faq"
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"


class KBSource(BaseModel):
    class Type(models.TextChoices):
        LESSON = "lesson"
        DOCUMENT = "document"

    class Status(models.TextChoices):
        PENDING = "pending"
        INDEXED = "indexed"
        FAILED = "failed"

    type = models.CharField(max_length=10, choices=Type)
    lesson_id = models.BigIntegerField(null=True, blank=True)  # catalog module
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=300, blank=True)
    body = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=Status, default=Status.PENDING)
    error = models.CharField(max_length=500, blank=True)
    content_hash = models.CharField(max_length=64, blank=True)
    chunk_count = models.IntegerField(default=0)
    last_indexed_at = models.DateTimeField(null=True, blank=True)

    class Meta(BaseModel.Meta):
        managed = False
        db_table = "kb_sources"
        verbose_name = "knowledge source"


class KBChunk(models.Model):
    source = models.ForeignKey(KBSource, on_delete=models.CASCADE, related_name="chunks")
    chunk_no = models.IntegerField()
    text = models.TextField()
    lesson_id = models.BigIntegerField(null=True)
    course_id = models.BigIntegerField(null=True)

    class Meta:
        managed = False
        db_table = "kb_chunks"


class Conversation(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE, null=True, related_name="+")
    session_key = models.CharField(max_length=36, null=True)
    lesson_id = models.BigIntegerField(null=True)
    title = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = "chat_conversations"


class Message(models.Model):
    class Role(models.TextChoices):
        USER = "user"
        ASSISTANT = "assistant"

    class AnsweredBy(models.TextChoices):
        LEARNER = "learner"  # the question itself
        MODEL = "model"
        FAQ = "faq"
        SYSTEM = "system"  # limits, pauses and errors

    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    role = models.CharField(max_length=10, choices=Role)
    content = models.TextField()
    content_html = models.TextField()
    answered_by = models.CharField(max_length=10, choices=AnsweredBy)
    sources = models.JSONField(null=True)
    model = models.CharField(max_length=60, blank=True)
    prompt_version = models.ForeignKey(
        PromptVersion, on_delete=models.SET_NULL, null=True, related_name="+"
    )
    tokens_in = models.IntegerField(default=0)
    tokens_out = models.IntegerField(default=0)
    cached_tokens = models.IntegerField(default=0)
    latency_ms = models.IntegerField(default=0)
    feedback = models.CharField(max_length=4, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = "chat_messages"


class UsageDaily(models.Model):
    date = models.DateField()
    model = models.CharField(max_length=60)
    audience = models.CharField(max_length=10)
    requests = models.IntegerField(default=0)
    tokens_in = models.BigIntegerField(default=0)
    tokens_out = models.BigIntegerField(default=0)
    est_cost = models.DecimalField(max_digits=10, decimal_places=4, default=0)

    class Meta:
        managed = False
        db_table = "ai_usage_daily"
