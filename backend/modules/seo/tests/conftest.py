import pytest

from modules.catalog import services as catalog
from modules.catalog.models import Status


@pytest.fixture
def course(make_user):
    admin = make_user("author@example.com", "author")
    category = catalog.save_category(None, {"name": "Python"}, admin)
    course = catalog.save_course(
        None,
        {
            "category": category,
            "title": "Python Basics",
            "short_description": "Start coding in Python.",
            "status": Status.PUBLISHED,
        },
        admin,
    )
    chapter = catalog.save_chapter(None, {"course": course, "title": "Start"}, admin)
    lesson = catalog.save_lesson(
        None,
        {
            "chapter": chapter,
            "title": "Lists",
            "status": Status.PUBLISHED,
            "summary": "Store many values.",
        },
        admin,
    )
    catalog.save_block(
        None, {"lesson": lesson, "type": "markdown", "content_md": "A list holds items."}, admin
    )
    return course
