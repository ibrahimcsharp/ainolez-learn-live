"""Read queries. Visitors see approved content only; authors also see their own pending items."""

import re

from django.db.models import Count, Q

from modules.community.models import (
    TARGETS,
    CommunitySettings,
    ContentReport,
    LessonComment,
    Post,
    Reaction,
    Space,
    Status,
)
from modules.identity import selectors as identity

PAGE_SIZE = 20


def spaces() -> list[dict]:
    rows = (
        Space.objects.filter(is_active=True)
        .annotate(post_count=Count("posts", filter=Q(posts__status=Status.APPROVED)))
        .order_by("sort_order", "name")
    )
    return [
        {
            "id": s.pk,
            "name": s.name,
            "slug": s.slug,
            "description": s.description,
            "icon": s.icon,
            "post_count": s.post_count,
        }
        for s in rows
    ]


def posts(space_slug: str = "", query: str = "", page: int = 1) -> list[dict]:
    rows = Post.objects.filter(status=Status.APPROVED, is_active=True, space__is_active=True)
    if space_slug:
        rows = rows.filter(space__slug=space_slug)
    if query:
        rows = rows.filter(Q(title__icontains=query) | Q(body_md__icontains=query))
    rows = rows.select_related("space").order_by("-is_pinned", "-created_at")
    start = (max(page, 1) - 1) * PAGE_SIZE
    rows = list(rows[start : start + PAGE_SIZE])
    names = identity.display_names(p.user_id for p in rows)
    return [_post_summary(p, names) for p in rows]


def post_detail(post_id: int, viewer) -> dict | None:
    post = Post.objects.select_related("space").filter(pk=post_id, is_active=True).first()
    if post is None or not _visible(post, viewer):
        return None
    replies = [
        r for r in post.replies.filter(is_active=True).order_by("created_at") if _visible(r, viewer)
    ]
    names = identity.display_names({post.user_id, *(r.user_id for r in replies)})
    liked_replies = _liked(viewer, "reply", [r.pk for r in replies])
    return {
        **_post_summary(post, names),
        "body_html": post.body_html,
        "status": post.status,
        "liked": post.pk in _liked(viewer, "post", [post.pk]),
        "is_mine": bool(viewer and viewer.pk == post.user_id),
        "replies": [
            {
                "id": r.pk,
                "author": names.get(r.user_id, ""),
                "body_html": r.body_html,
                "status": r.status,
                "is_helpful": r.is_helpful,
                "likes": r.reaction_count,
                "liked": r.pk in liked_replies,
                "created_at": r.created_at,
            }
            for r in replies
        ],
    }


def lesson_comments(lesson_id: int, viewer) -> list[dict]:
    rows = [
        c
        for c in LessonComment.objects.filter(lesson_id=lesson_id, is_active=True).order_by(
            "created_at"
        )
        if _visible(c, viewer)
    ]
    names = identity.display_names(c.user_id for c in rows)
    liked = _liked(viewer, "comment", [c.pk for c in rows])
    return [
        {
            "id": c.pk,
            "author": names.get(c.user_id, ""),
            "body_html": c.body_html,
            "status": c.status,
            "likes": c.reaction_count,
            "liked": c.pk in liked,
            "created_at": c.created_at,
        }
        for c in rows
    ]


def moderation_queue() -> list[dict]:
    """Everything waiting for approval, oldest first."""
    items = []
    for target_type, model in TARGETS.items():
        for item in model.objects.filter(status=Status.PENDING).order_by("created_at")[:200]:
            items.append(
                {
                    "target_type": target_type,
                    "id": item.pk,
                    "user_id": item.user_id,
                    "title": getattr(item, "title", ""),
                    "body_html": item.body_html,
                    "blocked_words": blocked_words_in(
                        f"{getattr(item, 'title', '')} {item.body_md}"
                    ),
                    "created_at": item.created_at,
                }
            )
    names = identity.display_names(i["user_id"] for i in items)
    for item in items:
        item["author"] = names.get(item["user_id"], "")
    return sorted(items, key=lambda i: i["created_at"])


def open_reports() -> list[dict]:
    reports = ContentReport.objects.filter(status=ContentReport.Status.OPEN).order_by("created_at")
    rows = []
    for report in reports:
        target = TARGETS[report.target_type].all_objects.filter(pk=report.target_id).first()
        rows.append(
            {
                "id": report.pk,
                "target_type": report.target_type,
                "target_id": report.target_id,
                "reason": report.reason,
                "created_at": report.created_at,
                "target_html": target.body_html if target else "",
                "target_status": target and target.status,
            }
        )
    return rows


def counts() -> dict[str, int]:
    pending = sum(m.objects.filter(status=Status.PENDING).count() for m in TARGETS.values())
    reports = ContentReport.objects.filter(status=ContentReport.Status.OPEN).count()
    return {"pending": pending, "open_reports": reports}


def _post_summary(post: Post, names: dict) -> dict:
    return {
        "id": post.pk,
        "title": post.title,
        "author": names.get(post.user_id, ""),
        "space": {"name": post.space.name, "slug": post.space.slug, "icon": post.space.icon},
        "is_pinned": post.is_pinned,
        "is_locked": post.is_locked,
        "reply_count": post.reply_count,
        "likes": post.reaction_count,
        "created_at": post.created_at,
    }


def _visible(item, viewer) -> bool:
    return item.status == Status.APPROVED or bool(
        viewer
        and viewer.is_authenticated
        and viewer.pk == item.user_id
        and item.status == Status.PENDING
    )


def _liked(viewer, target_type: str, ids) -> set[int]:
    if not viewer or not viewer.is_authenticated:
        return set()
    return set(
        Reaction.objects.filter(
            user=viewer, target_type=target_type, target_id__in=list(ids)
        ).values_list("target_id", flat=True)
    )


# --- used by the seo module --------------------------------------------------


def post_exists(post_id: int) -> bool:
    return Post.objects.filter(pk=post_id).exists()


def sitemap_posts() -> list[dict]:
    """Approved posts in open spaces: {id, url, updated_at}."""
    rows = Post.objects.filter(status=Status.APPROVED, is_active=True, space__is_active=True)
    return [
        {"id": pk, "url": f"/community/posts/{pk}", "updated_at": updated_at}
        for pk, updated_at in rows.values_list("pk", "updated_at")
    ]


def community_settings() -> CommunitySettings:
    return CommunitySettings.objects.get(pk=1)


def blocked_words_in(text: str, words: list[str] | None = None) -> list[str]:
    """The blocked words and phrases found in `text`: whole words, any case, any spacing."""
    words = community_settings().word_list if words is None else words
    if not words or not text:
        return []
    phrases = (r"\s+".join(re.escape(part) for part in w.split()) for w in words)
    pattern = r"(?<!\w)(" + "|".join(phrases) + r")(?!\w)"
    return sorted({" ".join(m.lower().split()) for m in re.findall(pattern, text, re.IGNORECASE)})
