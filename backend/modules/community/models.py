"""Tables from database/schema/0009_community.sql and 0014_community_word_filter.sql."""

from django.conf import settings
from django.db import models

from shared.models import BaseModel

USER = settings.AUTH_USER_MODEL


class Status(models.TextChoices):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    HIDDEN = "hidden"


class Space(BaseModel):
    class PostingRule(models.TextChoices):
        OPEN = "open"
        APPROVAL_REQUIRED = "approval_required"

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    description = models.CharField(max_length=500, blank=True)
    icon = models.CharField(max_length=50, default="💬")
    sort_order = models.IntegerField(default=0)
    posting_rule = models.CharField(max_length=20, choices=PostingRule, default=PostingRule.OPEN)

    class Meta(BaseModel.Meta):
        managed = False
        db_table = "community_spaces"


class Post(BaseModel):
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name="posts")
    user = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="+")
    title = models.CharField(max_length=200)
    body_md = models.TextField()
    body_html = models.TextField()
    status = models.CharField(max_length=10, choices=Status, default=Status.PENDING)
    reject_reason = models.CharField(max_length=255, blank=True)
    is_pinned = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    reply_count = models.IntegerField(default=0)
    reaction_count = models.IntegerField(default=0)

    class Meta(BaseModel.Meta):
        managed = False
        db_table = "community_posts"


class Reply(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="replies")
    user = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="+")
    body_md = models.TextField()
    body_html = models.TextField()
    status = models.CharField(max_length=10, choices=Status, default=Status.PENDING)
    reject_reason = models.CharField(max_length=255, blank=True)
    is_helpful = models.BooleanField(default=False)
    reaction_count = models.IntegerField(default=0)

    class Meta(BaseModel.Meta):
        managed = False
        db_table = "community_replies"
        verbose_name_plural = "replies"


class LessonComment(BaseModel):
    lesson_id = models.BigIntegerField()  # catalog module
    user = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="+")
    body_md = models.TextField()
    body_html = models.TextField()
    status = models.CharField(max_length=10, choices=Status, default=Status.PENDING)
    reject_reason = models.CharField(max_length=255, blank=True)
    reaction_count = models.IntegerField(default=0)

    class Meta(BaseModel.Meta):
        managed = False
        db_table = "lesson_comments"


class Reaction(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="+")
    target_type = models.CharField(max_length=10)
    target_id = models.BigIntegerField()
    type = models.CharField(max_length=10, default="like")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = "reactions"


class ContentReport(models.Model):
    class Status(models.TextChoices):
        OPEN = "open"
        RESOLVED = "resolved"
        DISMISSED = "dismissed"

    reporter = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="+")
    target_type = models.CharField(max_length=10)
    target_id = models.BigIntegerField()
    reason = models.CharField(max_length=500)
    status = models.CharField(max_length=10, choices=Status, default=Status.OPEN)
    resolved_by = models.ForeignKey(
        USER, on_delete=models.SET_NULL, null=True, related_name="+", db_column="resolved_by"
    )
    resolution_note = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = "content_reports"


# Things people can like, report and moderate, by the name the API uses.
TARGETS = {"post": Post, "reply": Reply, "comment": LessonComment}


class CommunitySettings(models.Model):
    """Singleton (id = 1): the blocked-words filter."""

    class BlockedAction(models.TextChoices):
        HOLD = "hold"  # save, but wait in the moderation queue
        REFUSE = "refuse"  # ask the writer to change the text

    blocked_words = models.TextField(null=True, blank=True)
    blocked_action = models.CharField(
        max_length=10, choices=BlockedAction, default=BlockedAction.HOLD
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        USER, on_delete=models.SET_NULL, null=True, related_name="+", db_column="updated_by"
    )

    class Meta:
        managed = False
        db_table = "community_settings"

    @property
    def word_list(self) -> list[str]:
        lines = (line.strip() for line in (self.blocked_words or "").splitlines())
        return sorted({line.lower() for line in lines if line})
