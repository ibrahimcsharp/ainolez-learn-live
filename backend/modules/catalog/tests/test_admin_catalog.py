import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from modules.catalog.models import Chapter, Course, Lesson, LessonBlock

pytestmark = pytest.mark.django_db
ADMIN = "/api/v1/admin/catalog"

CHAPTER_MD = b"""# Python Lists

A list keeps items in order.

```python tryit
print([1, 2, 3])
```

{{youtube:dQw4w9WgXcQ}}
"""


@pytest.fixture
def course(admin_api):
    category = admin_api.post(f"{ADMIN}/categories/", {"name": "Python"}).json()
    return admin_api.post(
        f"{ADMIN}/courses/", {"category": category["id"], "title": "Python Tutorial"}
    ).json()


@pytest.fixture
def chapter(admin_api, course):
    return admin_api.post(f"{ADMIN}/chapters/", {"course": course["id"], "title": "Basics"}).json()


def test_slug_is_made_from_the_title(course):
    assert course["slug"] == "python-tutorial"
    assert course["status"] == "draft"


def test_reserved_course_slug_is_refused(admin_api, course):
    response = admin_api.patch(f"{ADMIN}/courses/{course['id']}/", {"slug": "admin"})
    assert response.json()["code"] == "slug_reserved"


def test_learner_cannot_use_admin_api(api, make_user):
    api.force_authenticate(make_user())
    assert api.get(f"{ADMIN}/courses/").status_code == 403


def test_import_markdown_creates_lesson_with_blocks(admin_api, chapter):
    response = admin_api.post(
        f"{ADMIN}/lessons/import/",
        {"chapter": chapter["id"], "files": [SimpleUploadedFile("01-lists.md", CHAPTER_MD)]},
        format="multipart",
    )
    assert response.status_code == 201
    lesson = Lesson.objects.get()
    assert (lesson.title, lesson.slug, lesson.status) == ("Python Lists", "python-lists", "draft")
    blocks = list(lesson.blocks.order_by("sort_order"))
    assert [b.type for b in blocks] == ["markdown", "example", "video"]
    assert blocks[1].code_example.run_mode == "pyodide"
    assert "youtube-nocookie.com/embed/dQw4w9WgXcQ" in blocks[2].content_html

    exported = admin_api.get(f"{ADMIN}/lessons/{lesson.pk}/export/").content.decode()
    assert "```python tryit" in exported and "{{youtube:dQw4w9WgXcQ}}" in exported


def test_markdown_block_html_is_sanitised(admin_api, chapter):
    lesson = admin_api.post(
        f"{ADMIN}/lessons/", {"chapter": chapter["id"], "title": "Intro"}
    ).json()
    block = admin_api.post(
        f"{ADMIN}/blocks/",
        {"lesson": lesson["id"], "type": "markdown", "content_md": "Hi <script>x()</script>"},
        format="json",
    ).json()
    assert "<script" not in block["content_html"]


def test_example_block_needs_a_known_language(admin_api, chapter):
    lesson = admin_api.post(
        f"{ADMIN}/lessons/", {"chapter": chapter["id"], "title": "Intro"}
    ).json()
    response = admin_api.post(
        f"{ADMIN}/blocks/",
        {"lesson": lesson["id"], "type": "example", "example": {"language": "cobol"}},
        format="json",
    )
    assert response.json()["code"] == "bad_language"


def test_reorder_blocks(admin_api, chapter):
    lesson = admin_api.post(
        f"{ADMIN}/lessons/", {"chapter": chapter["id"], "title": "Intro"}
    ).json()
    first, second = (
        admin_api.post(
            f"{ADMIN}/blocks/",
            {"lesson": lesson["id"], "type": "markdown", "content_md": text},
            format="json",
        ).json()["id"]
        for text in ("one", "two")
    )
    admin_api.post(f"{ADMIN}/blocks/reorder/", {"ids": [second, first]}, format="json")
    ordered = LessonBlock.objects.order_by("sort_order").values_list("id", flat=True)
    assert list(ordered) == [second, first]


def test_soft_delete_restore_and_hard_delete(admin_api, course, chapter):
    url = f"{ADMIN}/courses/{course['id']}"
    assert admin_api.post(f"{url}/soft-delete/").status_code == 204
    assert admin_api.get(f"{ADMIN}/courses/").json()["count"] == 0
    assert admin_api.get(f"{ADMIN}/courses/?trash=1").json()["count"] == 1

    lesson = admin_api.post(
        f"{ADMIN}/lessons/", {"chapter": chapter["id"], "title": "Intro"}
    ).json()
    admin_api.post(
        f"{ADMIN}/blocks/",
        {"lesson": lesson["id"], "type": "markdown", "content_md": "Hi"},
        format="json",
    )
    preview = admin_api.get(f"{url}/hard/").json()
    assert preview["will_delete"] == {
        "courses": 1, "chapters": 1, "lessons": 1, "lesson blocks": 1
    }  # fmt: skip

    assert admin_api.delete(f"{url}/hard/", {"confirm": "wrong"}).json()["code"] == "bad_confirm"
    assert admin_api.delete(f"{url}/hard/", {"confirm": "Python Tutorial"}).status_code == 204
    assert not Course.all_objects.exists() and not Chapter.all_objects.exists()


def test_hard_delete_needs_the_item_in_trash_first(admin_api, course):
    response = admin_api.delete(
        f"{ADMIN}/courses/{course['id']}/hard/", {"confirm": "Python Tutorial"}
    )
    assert response.json()["code"] == "not_trashed"


def test_restore_is_refused_when_the_slug_was_reused(admin_api, course):
    admin_api.post(f"{ADMIN}/courses/{course['id']}/soft-delete/")
    admin_api.post(
        f"{ADMIN}/courses/",
        {"category": Course.all_objects.get().category_id, "title": "Python Tutorial"},
    )
    response = admin_api.post(f"{ADMIN}/courses/{course['id']}/restore/")
    assert response.json()["code"] == "slug_in_use"


def test_bulk_deactivate(admin_api):
    ids = [admin_api.post(f"{ADMIN}/categories/", {"name": n}).json()["id"] for n in ("A", "B")]
    response = admin_api.post(
        f"{ADMIN}/categories/bulk/", {"action": "deactivate", "ids": ids}, format="json"
    )
    assert response.json() == {"done": 2}
    assert admin_api.get(f"{ADMIN}/categories/?active=0").json()["count"] == 2


def test_publish_course_publishes_its_draft_lessons(admin_api, course, chapter):
    admin_api.post(f"{ADMIN}/lessons/", {"chapter": chapter["id"], "title": "Lists"})
    response = admin_api.post(f"{ADMIN}/courses/{course['id']}/publish/").json()
    assert response["status"] == "published" and response["lessons_published"] == 1
    assert not Lesson.objects.filter(course_id=course["id"], status="draft").exists()


def test_course_intro_video(admin_api, api, course):
    url = f"{ADMIN}/courses/{course['id']}/"
    bad = admin_api.patch(url, {"intro_video_url": "https://example.com/v"})
    assert bad.status_code == 400
    admin_api.patch(url, {"intro_video_url": "https://youtu.be/dQw4w9WgXcQ", "status": "published"})
    page = api.get(f"/api/v1/public/courses/{course['slug']}/").json()
    assert "youtube-nocookie.com/embed/dQw4w9WgXcQ" in page["intro_video_html"]
