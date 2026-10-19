"""
Community use cases: post, reply, comment on lessons, like, report, moderate.

New content is approved straight away only for trusted members (enough
points) in open spaces; everything else waits in the moderation queue.
"""

from django.conf import settings
from django.db import IntegrityError, transaction
from django.db.models import F
from django.utils import timezone

from modules.catalog import selectors as catalog
from modules.community import selectors
from modules.community.events import PostApproved, ReplyMarkedHelpful
from modules.community.models import (
    TARGETS,
    CommunitySettings,
    ContentReport,
    LessonComment,
    Post,
    Reaction,
    Reply,
    Space,
    Status,
)
from modules.content_tools import services as content
from modules.gamification import selectors as gamification
from modules.identity import services as identity
from shared import audit
from shared.events import publish
from shared.exceptions import ServiceError
from shared.slugs import unique_slug

MAX_BODY = 10_000
MODERATION_ACTIONS = ("approve", "reject", "hide", "pin", "unpin", "lock", "unlock", "ban")


def create_post(user, space_id: int, title: str, body_md: str) -> Post:
    flagged = _check_can_write(user, body_md, title)
    space = Space.objects.filter(pk=space_id, is_active=True).first()
    if space is None:
        raise ServiceError("Pick a space for your post.", "bad_space")
    approval = flagged or space.posting_rule != Space.PostingRule.OPEN
    status = _first_status(user, approval_required=approval)
    post = Post.objects.create(
        space=space,
        user=user,
        title=title.strip()[:200],
        body_md=body_md,
        body_html=content.render_markdown(body_md),
        status=status,
        created_by=user,
        updated_by=user,
    )
    if status == Status.APPROVED:
        publish(PostApproved(user.pk, post.pk))
    return post


def create_reply(user, post_id: int, body_md: str) -> Reply:
    flagged = _check_can_write(user, body_md)
    post = Post.objects.filter(pk=post_id, status=Status.APPROVED, is_active=True).first()
    if post is None:
        raise ServiceError("This post is not available.", "not_found", 404)
    if post.is_locked:
        raise ServiceError("This post is locked for new replies.", "locked")
    reply = Reply.objects.create(
        post=post,
        user=user,
        body_md=body_md,
        body_html=content.render_markdown(body_md),
        status=_first_status(user, approval_required=flagged),
        created_by=user,
        updated_by=user,
    )
    _recount_replies(post)
    return reply


def create_comment(user, lesson_id: int, body_md: str) -> LessonComment:
    flagged = _check_can_write(user, body_md)
    if catalog.visible_lesson(lesson_id) is None:
        raise ServiceError("This lesson is not available.", "not_found", 404)
    return LessonComment.objects.create(
        lesson_id=lesson_id,
        user=user,
        body_md=body_md,
        body_html=content.render_markdown(body_md),
        status=_first_status(user, approval_required=flagged),
        created_by=user,
        updated_by=user,
    )


def accept_reply(user, reply_id: int) -> Reply:
    """The post's author marks one reply as the helpful answer."""
    reply = Reply.objects.select_related("post").filter(pk=reply_id, status=Status.APPROVED).first()
    if reply is None or reply.post.user_id != user.pk:
        raise ServiceError("Only the person who asked can accept an answer.", "forbidden", 403)
    with transaction.atomic():
        Reply.objects.filter(post=reply.post, is_helpful=True).update(is_helpful=False)
        reply.is_helpful = True
        reply.save(update_fields=["is_helpful", "updated_at"])
        if reply.user_id != user.pk:
            publish(ReplyMarkedHelpful(reply.user_id, reply.pk))
    return reply


def toggle_like(user, target_type: str, target_id: int) -> bool:
    """Like, or un-like if already liked. Returns whether it is now liked."""
    model = _target_model(target_type)
    if not model.objects.filter(pk=target_id, status=Status.APPROVED).exists():
        raise ServiceError("This item is not available.", "not_found", 404)
    with transaction.atomic():
        deleted, _ = Reaction.objects.filter(
            user=user, target_type=target_type, target_id=target_id
        ).delete()
        if not deleted:
            Reaction.objects.create(user=user, target_type=target_type, target_id=target_id)
        model.all_objects.filter(pk=target_id).update(
            reaction_count=F("reaction_count") + (-1 if deleted else 1)
        )
    return not deleted


def report(user, target_type: str, target_id: int, reason: str) -> None:
    model = _target_model(target_type)
    if not model.objects.filter(pk=target_id).exists():
        raise ServiceError("This item is not available.", "not_found", 404)
    if not reason.strip():
        raise ServiceError("Tell us what is wrong.", "reason_required")
    try:
        ContentReport.objects.create(
            reporter=user, target_type=target_type, target_id=target_id, reason=reason.strip()[:500]
        )
    except IntegrityError:
        pass  # already reported by this person


def moderate(moderator, target_type: str, target_id: int, action: str, reason: str = ""):
    """Approve, reject, hide, pin, lock (or undo) an item, or ban its author."""
    if action not in MODERATION_ACTIONS:
        raise ServiceError("Unknown moderation action.", "bad_action")
    item = _target_model(target_type).all_objects.filter(pk=target_id).first()
    if item is None:
        raise ServiceError("This item does not exist.", "not_found", 404)
    if action in ("pin", "unpin", "lock", "unlock") and target_type != "post":
        raise ServiceError("Only posts can be pinned or locked.", "bad_action")

    was_approved = item.status == Status.APPROVED
    with transaction.atomic():
        if action == "approve":
            item.status, item.reject_reason = Status.APPROVED, ""
        elif action in ("reject", "hide", "ban"):
            item.status = Status.REJECTED if action == "reject" else Status.HIDDEN
            item.reject_reason = reason[:255]
        elif action in ("pin", "unpin"):
            item.is_pinned = action == "pin"
        else:
            item.is_locked = action == "lock"
        item.updated_by = moderator
        item.save()
        if action == "ban":
            identity.ban_user(item.user_id, reason or "Broke the community rules.", moderator)
        if target_type == "reply":
            _recount_replies(item.post)
        if target_type == "post" and action == "approve" and not was_approved:
            publish(PostApproved(item.user_id, item.pk))
        audit.record(
            f"{target_type}.{action}", actor=moderator, entity=item, after={"reason": reason}
        )
    return item


def resolve_report(moderator, report_id: int, dismiss: bool, note: str = "") -> ContentReport:
    item = ContentReport.objects.filter(pk=report_id).first()
    if item is None:
        raise ServiceError("This report does not exist.", "not_found", 404)
    item.status = ContentReport.Status.DISMISSED if dismiss else ContentReport.Status.RESOLVED
    item.resolved_by = moderator
    item.resolution_note = note[:500]
    item.resolved_at = timezone.now()
    item.save()
    return item


def save_space(space: Space | None, data: dict, by) -> Space:
    space = space or Space()
    for name, value in data.items():
        setattr(space, name, value)
    if not space.slug:
        space.slug = unique_slug(Space.objects.all(), space.name, exclude_pk=space.pk)
    is_new = space.pk is None
    if is_new:
        space.created_by = by
    space.updated_by = by
    space.save()
    audit.record(f"space.{'created' if is_new else 'updated'}", actor=by, entity=space)
    return space


def _first_status(user, approval_required: bool = False) -> str:
    """Trusted members skip the queue, unless the space asks for approval."""
    if user.is_super_admin:
        return Status.APPROVED
    trusted = gamification.total_points(user.pk) >= settings.COMMUNITY_TRUSTED_POINTS
    return Status.APPROVED if trusted and not approval_required else Status.PENDING


def _check_can_write(user, body_md: str, title: str = "") -> bool:
    """Raises when the text cannot be saved. True when it uses blocked words
    and must wait for a moderator."""
    if user.is_banned:
        raise ServiceError("Your account cannot post in the community.", "banned", 403)
    if not body_md.strip():
        raise ServiceError("Write something first.", "empty")
    if len(body_md) > MAX_BODY:
        raise ServiceError(f"Keep it under {MAX_BODY:,} characters.", "too_long")
    if user.is_super_admin:
        return False
    rules = selectors.community_settings()
    found = selectors.blocked_words_in(f"{title} {body_md}", rules.word_list)
    if found and rules.blocked_action == CommunitySettings.BlockedAction.REFUSE:
        words = ", ".join(f'"{w}"' for w in found)
        raise ServiceError(f"Please remove words our community does not allow: {words}.", "blocked")
    return bool(found)


def _recount_replies(post: Post) -> None:
    count = post.replies.filter(status=Status.APPROVED).count()
    Post.all_objects.filter(pk=post.pk).update(reply_count=count)


def _target_model(target_type: str):
    if target_type not in TARGETS:
        raise ServiceError("Unknown item type.", "bad_target")
    return TARGETS[target_type]


def update_settings(changes: dict, by) -> CommunitySettings:
    rules = selectors.community_settings()
    if "blocked_action" in changes:
        if changes["blocked_action"] not in CommunitySettings.BlockedAction.values:
            raise ServiceError("Choose hold or refuse.", "bad_action")
        rules.blocked_action = changes["blocked_action"]
    if "blocked_words" in changes:
        lines = str(changes["blocked_words"]).splitlines()
        rules.blocked_words = "\n".join(sorted({w.strip().lower() for w in lines if w.strip()}))
    rules.updated_by = by
    rules.save()
    audit.record("communitysettings.updated", actor=by, entity=rules)
    return rules
