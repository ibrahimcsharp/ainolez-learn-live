import pytest

from modules.catalog import services as catalog
from modules.catalog.models import Status
from modules.seo import prerender, resolver
from modules.seo.models import SeoPage

PUBLIC = "/api/v1/public/seo/"
ADMIN = "/api/v1/admin/seo"


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


def tag(data, key, value):
    return next(
        (t.get("content") or t.get("href") for t in data["tags"] if t.get(key) == value), None
    )


@pytest.mark.django_db
def test_lesson_gets_automatic_tags_from_its_content(api, course):
    data = api.get(PUBLIC, {"path": "/python-basics/lists"}).json()
    assert data["title"] == "Lists · Python Basics · ainolez"
    assert tag(data, "name", "description") == "Store many values."
    assert tag(data, "rel", "canonical") == "http://localhost:5173/python-basics/lists"
    assert tag(data, "property", "og:type") == "article"
    assert {item["@type"] for item in data["json_ld"]} == {"LearningResource", "BreadcrumbList"}


@pytest.mark.django_db
def test_admin_settings_win_and_follow_a_slug_change(admin_api, api, course):
    saved = admin_api.post(f"{ADMIN}/pages/", {
        "path": "/python-basics",
        "meta_title": "Learn Python free",
        "robots": "noindex,follow",
        "structured_data": {"@type": "FAQPage"},
    }, format="json")  # fmt: skip
    assert saved.status_code == 201, saved.json()
    assert saved.json()["entity_type"] == "course" and saved.json()["url"] == "/python-basics"

    course.slug = "python"
    course.save()
    data = api.get(PUBLIC, {"path": "/python"}).json()
    assert data["title"] == "Learn Python free"
    assert tag(data, "name", "robots") == "noindex,follow"
    assert {"@type": "FAQPage"} in data["json_ld"]


@pytest.mark.django_db
def test_fixed_pages_unknown_pages_and_private_pages(api):
    assert api.get(PUBLIC, {"path": "/login"}).json()["title"] == "Log in · ainolez"
    missing = api.get(PUBLIC, {"path": "/no-such-course"}).json()
    assert missing["status"] == 404 and tag(missing, "name", "robots") == "noindex,nofollow"
    assert (
        tag(api.get(PUBLIC, {"path": "/admin/courses"}).json(), "name", "robots")
        == "noindex,nofollow"
    )


@pytest.mark.django_db
def test_staging_switch_makes_every_page_noindex(admin_api, api):
    assert (
        admin_api.patch(f"{ADMIN}/settings/", {"allow_indexing": False}, format="json").status_code
        == 200
    )
    assert tag(api.get(PUBLIC, {"path": "/"}).json(), "name", "robots") == "noindex,nofollow"
    assert prerender.robots_txt(resolver.settings_row()) == "User-agent: *\nDisallow: /\n"


@pytest.mark.django_db
def test_bad_input_is_refused(admin_api):
    for body in (
        {"path": "/admin/x"},
        {"path": "/../etc"},
        {"path": "/courses"},  # already seeded
        {"path": "/new-page", "og_image_url": "javascript:alert(1)"},
        {"path": "/new-page", "structured_data": "not json-ld"},
    ):
        assert admin_api.post(f"{ADMIN}/pages/", body, format="json").status_code == 400, body


@pytest.mark.django_db
def test_page_views_are_counted(api, course):
    api.get(PUBLIC, {"path": "/python-basics"})
    api.get(PUBLIC, {"path": "/python-basics"})
    api.get(PUBLIC, {"path": "/dashboard"})
    from modules.seo import selectors

    assert selectors.top_pages(7) == [{"path": "/python-basics", "views": 2}]


@pytest.mark.django_db
def test_build_writes_pages_sitemap_and_robots(tmp_path, settings, course):
    settings.PRERENDER_DIR = str(tmp_path)
    (tmp_path / "shell.html").write_text(
        '<html><head><title>x</title>\n<meta\n name="description" content="old">\n</head>'
        '<body><div id="root"></div></body></html>'
    )
    (tmp_path / "old-course").mkdir()
    (tmp_path / "old-course" / "index.html").write_text("stale")
    (tmp_path / ".prerendered.json").write_text('["old-course/index.html"]')

    assert prerender.build() >= 3
    lesson = (tmp_path / "python-basics" / "lists" / "index.html").read_text(encoding="utf-8")
    assert "<title>Lists · Python Basics · ainolez</title>" in lesson
    assert 'content="old"' not in lesson and "<p>A list holds items.</p>" in lesson
    assert '"@type": "LearningResource"' in lesson
    assert not (tmp_path / "old-course").exists()
    sitemap = (tmp_path / "sitemap.xml").read_text()
    assert "<loc>http://localhost:5173/python-basics/lists</loc>" in sitemap
    assert "/login" not in sitemap  # noindex pages stay out
    assert "Sitemap: http://localhost:5173/sitemap.xml" in (tmp_path / "robots.txt").read_text()
    assert SeoPage.objects.filter(path="/").exists()
