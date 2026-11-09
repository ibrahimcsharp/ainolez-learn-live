"""SEO & GEO Center, phase 1: GEO files, AI crawlers, key moments, referrals, IndexNow,
the overview and the change log with undo."""

import pytest

from modules.catalog import services as catalog
from modules.catalog.models import LessonBlock
from modules.seo import geo, indexnow, prerender
from modules.seo.models import AiBot, ReferralVisitDaily, SeoChangeLog

PUBLIC = "/api/v1/public/seo/"
ADMIN = "/api/v1/admin/seo"
SHELL = '<html><head><title>x</title></head><body><div id="root"></div></body></html>'


@pytest.fixture
def site_dir(tmp_path, settings):
    settings.PRERENDER_DIR = str(tmp_path)
    (tmp_path / "shell.html").write_text(SHELL)
    return tmp_path


@pytest.mark.django_db
def test_build_writes_llms_txt_and_markdown_copies(admin_api, api, site_dir, course):
    prerender.build()
    llms = (site_dir / "llms.txt").read_text(encoding="utf-8")
    assert llms.startswith("# ainolez\n\n> ")
    assert "- [Python Basics](http://localhost:5173/python-basics.md): Start coding" in llms
    course_md = (site_dir / "python-basics.md").read_text(encoding="utf-8")
    assert "# Python Basics" in course_md
    assert "[Lists](http://localhost:5173/python-basics/lists.md): Store many values." in course_md
    lesson_md = (site_dir / "python-basics" / "lists.md").read_text(encoding="utf-8")
    assert "# Lists" in lesson_md and "A list holds items." in lesson_md
    full = (site_dir / "llms-full.txt").read_text(encoding="utf-8")
    assert full.index("# Python Basics") < full.index("# Lists")

    data = api.get(PUBLIC, {"path": "/python-basics/lists"}).json()
    alternate = [t for t in data["tags"] if t.get("type") == "text/markdown"]
    assert alternate[0]["href"] == "http://localhost:5173/python-basics/lists.md"

    # switched off: the next build removes the files
    admin_api.patch(f"{ADMIN}/settings/", {"geo_markdown_copies": False, "geo_llms_enabled": False},
                    format="json")  # fmt: skip
    prerender.build()
    assert not (site_dir / "python-basics.md").exists()
    assert not (site_dir / "python-basics" / "lists.md").exists()
    assert not (site_dir / "llms.txt").exists()
    assert (site_dir / "python-basics" / "lists" / "index.html").exists()


def test_reader_markdown_never_has_exercises_or_quizzes():
    blocks = [
        LessonBlock(type="markdown", content_md="Read this."),
        LessonBlock(type="exercise", content_html="solution: 42"),
        LessonBlock(type="quiz", content_html="answer: B"),
        LessonBlock(type="video", data={"provider": "youtube", "ref": "dQw4w9WgXcQ"}),
    ]
    text = catalog.reader_markdown(blocks)
    assert "Read this." in text and "42" not in text and "answer" not in text
    assert geo._clean(text).endswith("[Video](https://www.youtube.com/watch?v=dQw4w9WgXcQ)")
    assert geo._clean("```python tryit\nprint(1)\n```") == "```python\nprint(1)\n```"


@pytest.mark.django_db
def test_blocking_an_ai_crawler_and_undoing_it(admin_api):
    bot = AiBot.objects.get(user_agent="GPTBot")
    assert "GPTBot" not in prerender.robots_txt(prerender.resolver.settings_row())

    response = admin_api.patch(f"{ADMIN}/bots/{bot.pk}/", {"allowed": False}, format="json")
    assert response.status_code == 200, response.json()
    robots = admin_api.get(f"{ADMIN}/geo-file/", {"file": "robots"}).json()["text"]
    assert "User-agent: GPTBot\nDisallow: /" in robots
    assert "User-agent: *\nDisallow: /admin" in robots  # everyone else as before

    entry = SeoChangeLog.objects.get(area="ai_bot")
    assert entry.summary == "Blocked GPTBot" and entry.actor == "admin"
    undone = admin_api.post(f"{ADMIN}/changes/{entry.pk}/undo/").json()
    assert undone["undone_at"] and not undone["can_undo"]
    bot.refresh_from_db()
    assert bot.allowed
    assert admin_api.post(f"{ADMIN}/changes/{entry.pk}/undo/").status_code == 400


@pytest.mark.django_db
def test_settings_changes_are_logged_and_can_be_undone(admin_api):
    admin_api.patch(f"{ADMIN}/settings/", {"geo_site_summary": "Free coding courses."},
                    format="json")  # fmt: skip
    admin_api.patch(
        f"{ADMIN}/settings/", {"geo_site_summary": "Free coding courses."}, format="json"
    )  # fmt: skip  (same value: nothing logged)
    log = admin_api.get(f"{ADMIN}/changes/", {"area": "settings"}).json()
    assert len(log) == 1
    assert log[0]["changes"] == [
        {"field": "geo_site_summary", "old": "", "new": "Free coding courses."}
    ]
    admin_api.post(f"{ADMIN}/changes/{log[0]['id']}/undo/")
    assert admin_api.get(f"{ADMIN}/settings/").json()["geo_site_summary"] == ""


@pytest.mark.django_db
def test_video_timestamps_become_key_moments(api, course, make_user):
    lesson = course.chapters.first().lessons.first()
    catalog.save_block(None, {
        "lesson": lesson,
        "type": "markdown",
        "content_md": "{{youtube:dQw4w9WgXcQ}}\n\nChapters\n00:00 | Start\n00:40 | Setup\n"
                      "1:02:03 | Wrap up",
    }, make_user("editor@example.com", "editor"))  # fmt: skip
    data = api.get(PUBLIC, {"path": "/python-basics/lists"}).json()
    video = next(item for item in data["json_ld"] if item["@type"] == "VideoObject")
    assert video["embedUrl"] == "https://www.youtube.com/embed/dQw4w9WgXcQ"
    assert video["thumbnailUrl"] == ["https://i.ytimg.com/vi/dQw4w9WgXcQ/hqdefault.jpg"]
    clips = video["hasPart"]
    assert [(c["name"], c["startOffset"]) for c in clips] == [
        ("Start", 0), ("Setup", 40), ("Wrap up", 3723)
    ]  # fmt: skip
    assert clips[1]["endOffset"] == 3723 and "endOffset" not in clips[2]
    assert clips[1]["url"] == "http://localhost:5173/python-basics/lists?t=40"


@pytest.mark.parametrize(
    "referrer, utm, expected",
    [
        ("https://chatgpt.com/", "", ("ai", "ChatGPT")),
        ("", "chatgpt.com", ("ai", "ChatGPT")),
        ("https://www.perplexity.ai/search?q=x", "", ("ai", "Perplexity")),
        ("https://gemini.google.com/app", "", ("ai", "Gemini")),
        ("https://www.google.co.uk/", "", ("search", "Google")),
        ("https://www.bing.com/search?q=x", "", ("search", "Bing")),
        ("https://lnkd.in/abc", "", ("social", "LinkedIn")),
        ("https://example.com/", "", None),
        ("", "", None),
    ],
)
def test_classify_where_a_visit_came_from(referrer, utm, expected):
    assert geo.classify(referrer, utm) == expected


@pytest.mark.django_db
def test_referrals_are_counted(api, course):
    api.get(PUBLIC, {"path": "/python-basics", "ref": "https://chatgpt.com/"})
    api.get(PUBLIC, {"path": "/python-basics", "utm": "chatgpt.com"})
    api.get(PUBLIC, {"path": "/python-basics", "ref": "https://example.com/"})
    api.get(PUBLIC, {"path": "/dashboard", "ref": "https://chatgpt.com/"})  # private: no
    rows = list(ReferralVisitDaily.objects.values("kind", "source", "path", "visits"))
    assert rows == [{"kind": "ai", "source": "ChatGPT", "path": "/python-basics", "visits": 2}]


@pytest.mark.django_db
def test_indexnow_sends_pages_first_all_then_only_changed(
    admin_api, site_dir, settings, course, monkeypatch
):
    settings.FRONTEND_URL = "https://ainolez.com"
    sent = []
    monkeypatch.setattr(indexnow, "send", lambda body: sent.append(body) or 200)
    key = admin_api.patch(f"{ADMIN}/settings/", {"indexnow_enabled": True},
                          format="json").json()["indexnow_key"]  # fmt: skip
    assert len(key) == 32

    prerender.build()
    assert (site_dir / f"{key}.txt").read_text() == key
    assert sent[0]["host"] == "ainolez.com" and sent[0]["key"] == key
    assert "https://ainolez.com/python-basics/lists" in sent[0]["urlList"]

    prerender.build()  # nothing changed
    assert len(sent) == 1
    course.title = "Python Basics 2"
    course.save()
    prerender.build()
    assert sent[1]["urlList"] == ["https://ainolez.com/python-basics"]
    assert SeoChangeLog.objects.filter(area="indexnow").count() == 2


@pytest.mark.django_db
def test_overview_scores_and_fix_next(admin_api, course):
    data = admin_api.get(f"{ADMIN}/overview/").json()
    assert 0 <= data["seo"]["score"] <= 100 and 0 <= data["geo"]["score"] <= 100
    keys = {c["key"]: c for c in data["geo"]["checks"]}
    assert keys["llms"]["ok"] and not keys["indexnow"]["ok"]
    assert keys["indexnow"]["fix"] == "indexnow_enabled"
    assert any(item["label"].startswith("IndexNow") for item in data["fix_next"])
    assert set(data["traffic"]["totals"]) == {"search", "ai", "social"}


@pytest.mark.django_db
def test_center_needs_a_super_admin(api, make_user):
    api.force_authenticate(make_user())
    assert api.get(f"{ADMIN}/overview/").status_code == 403
    assert api.get(f"{ADMIN}/bots/").status_code == 403
