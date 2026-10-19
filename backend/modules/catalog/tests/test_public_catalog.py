import pytest

from modules.catalog import services
from modules.catalog.models import Status

PUBLIC = "/api/v1/public"


@pytest.fixture
def published(make_user):
    """A published course with two published lessons and one draft."""
    admin = make_user("admin@example.com", "admin")
    category = services.save_category(None, {"name": "Python"}, admin)
    course = services.save_course(
        None, {"category": category, "title": "Python", "status": Status.PUBLISHED}, admin
    )
    chapter = services.save_chapter(None, {"course": course, "title": "Basics"}, admin)
    for title, status in (
        ("Lists", Status.PUBLISHED),
        ("Loops", Status.PUBLISHED),
        ("Secret", Status.DRAFT),
    ):
        lesson = services.save_lesson(
            None, {"chapter": chapter, "title": title, "status": status}, admin
        )
        services.save_block(
            None,
            {
                "lesson": lesson,
                "type": "markdown",
                "content_md": f"Learn about {title} with enumerate",
            },
            admin,
        )
    return course


@pytest.mark.django_db
def test_course_outline_hides_drafts(api, published):
    data = api.get(f"{PUBLIC}/courses/python/").json()
    assert [lesson["slug"] for lesson in data["chapters"][0]["lessons"]] == ["lists", "loops"]


@pytest.mark.django_db
def test_lesson_page_has_blocks_and_neighbours(api, published):
    data = api.get(f"{PUBLIC}/courses/python/lessons/lists/").json()
    assert data["blocks"][0]["content_html"] == "<p>Learn about Lists with enumerate</p>"
    assert data["previous"] is None and data["next"]["slug"] == "loops"


@pytest.mark.django_db
def test_draft_lesson_and_draft_course_are_not_public(api, published):
    assert api.get(f"{PUBLIC}/courses/python/lessons/secret/").status_code == 404
    published.status = Status.DRAFT
    published.save()
    assert api.get(f"{PUBLIC}/courses/python/").status_code == 404
    assert api.get(f"{PUBLIC}/courses/").json() == []


@pytest.mark.django_db
def test_inactive_category_hides_its_courses(api, published):
    published.category.is_active = False
    published.category.save()
    assert api.get(f"{PUBLIC}/courses/").json() == []


# FULLTEXT indexes only see committed rows, so this test commits for real.
def test_search_finds_published_lessons_only(committed_db, api, published):
    results = api.get(f"{PUBLIC}/search/?q=enumerate").json()
    assert sorted(r["slug"] for r in results) == ["lists", "loops"]
    assert api.get(f"{PUBLIC}/search/?q=loops").json()[0]["slug"] == "loops"
