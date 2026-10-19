import pytest
from rest_framework.test import APIClient

from modules.catalog import services as catalog
from modules.community.models import LessonComment, Post, Space, Status
from modules.gamification.models import LearnerStats
from modules.identity.models import User

pytestmark = pytest.mark.django_db
API = "/api/v1/community"
ADMIN = "/api/v1/admin/community"


@pytest.fixture
def space():
    return Space.objects.get(slug="python")


def _trusted(user):
    LearnerStats.objects.create(user=user, total_points=500)
    return user


def _post(api, space, title="How do lists work?"):
    return api.post(
        f"{API}/posts/", {"space": space.pk, "title": title, "body_md": "Help **please**"}
    )


def test_new_members_wait_for_a_moderator_and_get_points_when_approved(
    api, admin_api, make_user, space
):
    learner = make_user()
    api.force_authenticate(learner)
    response = _post(api, space)
    assert response.json()["status"] == "pending"
    assert api.get(f"{API}/posts/").json() == []  # not public yet

    post_id = response.json()["id"]
    queue = admin_api.get(f"{ADMIN}/queue/").json()["pending"]
    assert [(i["target_type"], i["id"]) for i in queue] == [("post", post_id)]

    admin_api.post(
        f"{ADMIN}/moderate/", {"target_type": "post", "target_id": post_id, "action": "approve"}
    )
    assert api.get(f"{API}/posts/?space=python").json()[0]["title"] == "How do lists work?"
    assert LearnerStats.objects.get(user=learner).total_points == 10  # first post


def test_trusted_members_post_straight_away(api, make_user, space):
    api.force_authenticate(_trusted(make_user()))
    assert _post(api, space).json()["status"] == "approved"


def test_approval_required_space_holds_even_trusted_posts(api, make_user, space):
    space.posting_rule = Space.PostingRule.APPROVAL_REQUIRED
    space.save()
    api.force_authenticate(_trusted(make_user()))
    assert _post(api, space).json()["status"] == "pending"


def test_reply_accept_like_and_lock(api, make_user, space):
    asker, helper = _trusted(make_user()), _trusted(make_user("helper@example.com", "helper"))
    api.force_authenticate(asker)
    post_id = _post(api, space).json()["id"]

    api.force_authenticate(helper)
    reply_id = api.post(f"{API}/posts/{post_id}/replies/", {"body_md": "Use `append()`"}).json()[
        "id"
    ]
    assert api.post(f"{API}/replies/{reply_id}/accept/").status_code == 403  # only the asker

    api.force_authenticate(asker)
    api.post(f"{API}/replies/{reply_id}/accept/")
    assert LearnerStats.objects.get(user=helper).total_points == 500 + 20  # helpful answer

    like = {"target_type": "post", "target_id": post_id}
    assert api.post(f"{API}/like/", like).json() == {"liked": True}
    assert api.post(f"{API}/like/", like).json() == {"liked": False}

    detail = api.get(f"{API}/posts/{post_id}/").json()
    assert detail["reply_count"] == 1 and detail["replies"][0]["is_helpful"]

    Post.objects.filter(pk=post_id).update(is_locked=True)
    assert (
        api.post(f"{API}/posts/{post_id}/replies/", {"body_md": "more"}).json()["code"] == "locked"
    )


def test_lesson_comments_wait_for_approval(api, admin_api, make_user):
    author = make_user("author@example.com", "author")
    category = catalog.save_category(None, {"name": "Web"}, author)
    course = catalog.save_course(
        None, {"category": category, "title": "HTML", "status": "published"}, author
    )
    chapter = catalog.save_chapter(None, {"course": course, "title": "Basics"}, author)
    lesson = catalog.save_lesson(
        None, {"chapter": chapter, "title": "Tags", "status": "published"}, author
    )

    learner = make_user()
    api.force_authenticate(learner)
    comment = api.post(f"{API}/lessons/{lesson.pk}/comments/", {"body_md": "Great lesson!"}).json()
    assert comment["status"] == "pending"

    visitor = APIClient()
    assert visitor.get(f"{API}/lessons/{lesson.pk}/comments/").json() == []  # approved only

    admin_api.post(
        f"{ADMIN}/moderate/",
        {"target_type": "comment", "target_id": comment["id"], "action": "approve"},
    )
    assert [c["body_html"] for c in visitor.get(f"{API}/lessons/{lesson.pk}/comments/").json()] == [
        "<p>Great lesson!</p>"
    ]


def test_report_and_ban(api, admin_api, make_user, space):
    spammer = _trusted(make_user("spam@example.com", "spammer"))
    api.force_authenticate(spammer)
    post_id = _post(api, space, "Buy cheap stuff").json()["id"]

    api.force_authenticate(make_user())
    api.post(f"{API}/report/", {"target_type": "post", "target_id": post_id, "reason": "Spam"})
    reports = admin_api.get(f"{ADMIN}/queue/").json()["reports"]
    assert reports[0]["reason"] == "Spam"

    admin_api.post(
        f"{ADMIN}/moderate/",
        {"target_type": "post", "target_id": post_id, "action": "ban", "reason": "Spam"},
    )
    assert Post.objects.get(pk=post_id).status == Status.HIDDEN
    assert User.objects.get(pk=spammer.pk).is_banned

    api.force_authenticate(User.objects.get(pk=spammer.pk))
    assert _post(api, space).json()["code"] == "banned"


def test_scripts_in_posts_are_removed(api, make_user, space):
    api.force_authenticate(_trusted(make_user()))
    api.post(
        f"{API}/posts/", {"space": space.pk, "title": "x", "body_md": "<script>alert(1)</script>hi"}
    )
    assert "<script" not in Post.objects.get().body_html
    assert LessonComment.objects.count() == 0


def test_blocked_words_hold_or_refuse(api, admin_api, make_user, space):
    words = {"blocked_words": "Spam Link\nscam\n", "blocked_action": "hold"}
    admin_api.patch(f"{ADMIN}/settings/", words)
    api.force_authenticate(_trusted(make_user()))

    def post(title, body="hi"):
        return api.post(f"{API}/posts/", {"space": space.pk, "title": title, "body_md": body})

    assert post("Easy SCAM").json()["status"] == "pending"  # trusted, but held
    queue = admin_api.get(f"{ADMIN}/queue/").json()["pending"]
    assert queue[0]["blocked_words"] == ["scam"]
    assert post("Scampi recipe").json()["status"] == "approved"  # whole words only

    admin_api.patch(f"{ADMIN}/settings/", {"blocked_action": "refuse"})
    refused = post("Hi", "a Spam\n  link")  # any case and spacing
    assert refused.status_code == 400
    assert '"spam link"' in refused.json()["detail"]


def test_word_filter_settings_are_admin_only(api, make_user):
    api.force_authenticate(make_user())
    assert api.get(f"{ADMIN}/settings/").status_code == 403
