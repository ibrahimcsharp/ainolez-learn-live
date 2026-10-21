import json

import pytest

from modules.catalog import services as catalog
from modules.catalog.models import Status
from modules.seo import prerender
from modules.seo.services import BUILD_JOB
from modules.website.models import MenuItem, SitePage
from shared.models import Job

pytestmark = pytest.mark.django_db
ADMIN = "/api/v1/admin/website"
PUBLIC = "/api/v1/public/site"


@pytest.fixture
def course(make_user):
    author = make_user("author@example.com", "author")
    category = catalog.save_category(None, {"name": "Python"}, author)
    return catalog.save_course(
        None, {"category": category, "title": "Python", "status": Status.PUBLISHED}, author
    )


@pytest.fixture
def page(admin_api):
    response = admin_api.post(f"{ADMIN}/pages/", {
        "title": "About us",
        "summary": "Who builds ainolez.",
        "content_md": "## Our team\n\n!!! tip\n    Learn by doing.\n\n<script>alert(1)</script>",
    }, format="json")  # fmt: skip
    assert response.status_code == 201, response.json()
    return response.json()


def menu_with(admin_api, location="header", name="Test menu", show_as="links"):
    body = {"name": name, "location": location, "show_as": show_as}
    return admin_api.post(f"{ADMIN}/menus/", body).json()


# --- pages --------------------------------------------------------------------


def test_page_slug_comes_from_the_title_and_html_is_sanitised(page):
    assert page["slug"] == "about-us"
    assert "<h2" in page["content_html"] and "Our team" in page["content_html"]
    assert 'class="admonition tip"' in page["content_html"]
    assert "<script" not in page["content_html"]


def test_active_page_is_public_and_hidden_page_is_not(admin_api, api, page):
    data = api.get(f"{PUBLIC}/pages/about-us/").json()
    assert data["title"] == "About us"
    assert "Our team" in data["content_html"]

    admin_api.post(f"{ADMIN}/pages/{page['id']}/deactivate/")
    assert api.get(f"{PUBLIC}/pages/about-us/").status_code == 404


def test_trash_and_restore(admin_api, api, page):
    admin_api.post(f"{ADMIN}/pages/{page['id']}/soft-delete/")
    assert api.get(f"{PUBLIC}/pages/about-us/").status_code == 404
    trash = admin_api.get(f"{ADMIN}/pages/", {"trash": "1"}).json()["results"]
    assert [row["id"] for row in trash] == [page["id"]]

    assert admin_api.post(f"{ADMIN}/pages/{page['id']}/restore/").status_code == 200
    assert api.get(f"{PUBLIC}/pages/about-us/").status_code == 200


def test_page_and_course_slugs_never_clash(admin_api, course, page):
    for slug in ("python", "admin", "Not A Slug"):
        response = admin_api.patch(f"{ADMIN}/pages/{page['id']}/", {"slug": slug})
        assert response.status_code == 400, slug

    response = admin_api.patch(f"/api/v1/admin/catalog/courses/{course.pk}/", {"slug": "about-us"})
    assert response.status_code == 400
    assert response.json()["code"] == "slug_taken"
    assert not catalog.slug_is_free("about-us")


def test_automatic_slug_steps_around_courses_and_reserved_routes(admin_api, course):
    assert admin_api.post(f"{ADMIN}/pages/", {"title": "Python"}).json()["slug"] == "python-2"
    assert admin_api.post(f"{ADMIN}/pages/", {"title": "Login"}).json()["slug"] == "login-2"


def test_restore_is_refused_when_a_course_took_the_address(admin_api, make_user, page):
    admin_api.post(f"{ADMIN}/pages/{page['id']}/soft-delete/")
    author = make_user("other@example.com", "other")
    category = catalog.save_category(None, {"name": "Misc"}, author)
    catalog.save_course(None, {"category": category, "title": "About us"}, author)

    response = admin_api.post(f"{ADMIN}/pages/{page['id']}/restore/")
    assert response.status_code == 400
    assert response.json()["code"] == "slug_in_use"


def test_hard_delete_removes_the_menu_links_to_the_page(admin_api, page):
    menu = menu_with(admin_api)
    admin_api.post(
        f"{ADMIN}/menu-items/", {"menu": menu["id"], "link_type": "page", "page": page["id"]}
    )
    admin_api.post(f"{ADMIN}/pages/{page['id']}/soft-delete/")
    preview = admin_api.get(f"{ADMIN}/pages/{page['id']}/hard/").json()
    assert preview["will_delete"] == {"pages": 1, "menu items": 1}

    response = admin_api.delete(
        f"{ADMIN}/pages/{page['id']}/hard/", {"confirm": "About us"}, format="json"
    )
    assert response.status_code == 204
    assert not SitePage.all_objects.filter(pk=page["id"]).exists()
    assert not MenuItem.all_objects.filter(menu_id=menu["id"]).exists()


# --- menus --------------------------------------------------------------------


def test_menu_items_link_to_pages_courses_and_urls(admin_api, api, course, page):
    header = menu_with(admin_api)
    footer = menu_with(admin_api, "footer", "Company")
    post = lambda body: admin_api.post(f"{ADMIN}/menu-items/", body, format="json")  # noqa: E731
    assert post({"menu": header["id"], "link_type": "page", "page": page["id"]}).status_code == 201
    assert post({"menu": header["id"], "link_type": "course", "course_id": course.pk,
                 "label": "Learn Python"}).status_code == 201  # fmt: skip
    assert post({"menu": footer["id"], "link_type": "url", "url": "https://github.com/ainolez",
                 "label": "GitHub", "open_in_new_tab": True}).status_code == 201  # fmt: skip

    menus = api.get(f"{PUBLIC}/menus/").json()
    assert {"label": "About us", "url": "/about-us", "new_tab": False} in menus["header"]
    assert {"label": "Learn Python", "url": "/python", "new_tab": False} in menus["header"]
    company = next(m for m in menus["footer"] if m["id"] == footer["id"])
    assert company == {"id": footer["id"], "name": "Company", "items": [
        {"label": "GitHub", "url": "https://github.com/ainolez", "new_tab": True},
    ]}  # fmt: skip


def test_hidden_menus_items_and_targets_are_left_out(admin_api, api, page):
    menu = menu_with(admin_api, "footer", "Legal")
    item = admin_api.post(
        f"{ADMIN}/menu-items/", {"menu": menu["id"], "link_type": "page", "page": page["id"]}
    ).json()
    footer_ids = lambda: [m["id"] for m in api.get(f"{PUBLIC}/menus/").json()["footer"]]  # noqa: E731
    assert menu["id"] in footer_ids()

    admin_api.post(f"{ADMIN}/pages/{page['id']}/deactivate/")
    assert menu["id"] not in footer_ids()  # a footer column with no links is not shown
    admin_api.post(f"{ADMIN}/pages/{page['id']}/activate/")
    admin_api.post(f"{ADMIN}/menu-items/{item['id']}/deactivate/")
    assert menu["id"] not in footer_ids()
    admin_api.post(f"{ADMIN}/menu-items/{item['id']}/activate/")
    admin_api.post(f"{ADMIN}/menus/{menu['id']}/soft-delete/")
    assert menu["id"] not in footer_ids()


def test_menu_item_only_keeps_its_chosen_target(admin_api, page):
    menu = menu_with(admin_api)
    item = admin_api.post(
        f"{ADMIN}/menu-items/", {"menu": menu["id"], "link_type": "page", "page": page["id"]}
    ).json()
    assert item["target"] == "Page: /about-us"
    item = admin_api.patch(
        f"{ADMIN}/menu-items/{item['id']}/",
        {"link_type": "url", "url": "/courses", "label": "Courses"},
        format="json",
    ).json()
    assert item["page"] is None and item["url"] == "/courses"


@pytest.mark.parametrize("body", [
    {"link_type": "url", "url": "javascript:alert(1)", "label": "x"},
    {"link_type": "url", "url": "//evil.example", "label": "x"},
    {"link_type": "url", "url": "/courses"},  # no label
    {"link_type": "page"},
    {"link_type": "course", "course_id": 999999},
])  # fmt: skip
def test_bad_menu_items_are_refused(admin_api, body):
    menu = menu_with(admin_api)
    response = admin_api.post(f"{ADMIN}/menu-items/", {"menu": menu["id"], **body}, format="json")
    assert response.status_code == 400


def test_menu_items_reorder(admin_api):
    menu = menu_with(admin_api)
    ids = [
        admin_api.post(f"{ADMIN}/menu-items/", {
            "menu": menu["id"], "link_type": "url", "url": f"/{name}", "label": name,
        }).json()["id"]
        for name in ("a", "b", "c")
    ]  # fmt: skip
    admin_api.post(f"{ADMIN}/menu-items/reorder/", {"ids": ids[::-1]}, format="json")
    rows = admin_api.get(f"{ADMIN}/menu-items/", {"menu": menu["id"]}).json()["results"]
    assert [row["label"] for row in rows] == ["c", "b", "a"]


def add_link(admin_api, menu, **body):
    response = admin_api.post(f"{ADMIN}/menu-items/", {"menu": menu["id"], **body}, format="json")
    return response


def test_sub_menus_nest_under_their_link(admin_api, api, page):
    header = menu_with(admin_api)
    footer = menu_with(admin_api, "footer", "Company")
    learn = add_link(admin_api, header, link_type="none", label="Learn").json()
    add_link(
        admin_api, header, link_type="url", url="/courses", label="All courses", parent=learn["id"]
    )
    add_link(admin_api, header, link_type="page", page=page["id"], parent=learn["id"])
    add_link(admin_api, header, link_type="none", label="Empty")  # no sub-menu: not shown
    about = add_link(admin_api, footer, link_type="page", page=page["id"]).json()
    add_link(admin_api, footer, link_type="url", url="/team", label="Team", parent=about["id"])

    menus = api.get(f"{PUBLIC}/menus/").json()
    assert {"label": "Learn", "url": None, "new_tab": False, "children": [
        {"label": "All courses", "url": "/courses", "new_tab": False},
        {"label": "About us", "url": "/about-us", "new_tab": False},
    ]} in menus["header"]  # fmt: skip
    assert not any(link["label"] == "Empty" for link in menus["header"])
    company = next(m for m in menus["footer"] if m["id"] == footer["id"])
    team = {"label": "Team", "url": "/team", "new_tab": False}
    assert company["items"] == [
        {"label": "About us", "url": "/about-us", "new_tab": False, "children": [team]}
    ]

    # a hidden link hides its sub-menu, and a hidden page leaves the heading with one link
    admin_api.post(f"{ADMIN}/menu-items/{about['id']}/deactivate/")
    assert footer["id"] not in [m["id"] for m in api.get(f"{PUBLIC}/menus/").json()["footer"]]
    admin_api.post(f"{ADMIN}/pages/{page['id']}/deactivate/")
    learn_link = next(
        x for x in api.get(f"{PUBLIC}/menus/").json()["header"] if x["label"] == "Learn"
    )
    assert [c["label"] for c in learn_link["children"]] == ["All courses"]


def test_header_menu_shown_as_a_dropdown_named_after_it(admin_api, api, page):
    games = menu_with(admin_api, name="Games", show_as="dropdown")
    add_link(admin_api, games, link_type="url", url="/tic-tac-toe", label="Tic Tac Toe")
    more = add_link(admin_api, games, link_type="none", label="More").json()
    add_link(admin_api, games, link_type="page", page=page["id"], parent=more["id"])
    menu_with(admin_api, name="Empty", show_as="dropdown")  # no links: not shown

    header = api.get(f"{PUBLIC}/menus/").json()["header"]
    assert {"label": "Games", "url": None, "new_tab": False, "children": [
        {"label": "Tic Tac Toe", "url": "/tic-tac-toe", "new_tab": False},
        {"label": "More", "url": None, "new_tab": False, "children": [
            {"label": "About us", "url": "/about-us", "new_tab": False},
        ]},
    ]} in header  # fmt: skip
    assert not any(link["label"] == "Empty" for link in header)
    # the seeded Main menu keeps its links in the bar
    assert {"label": "Courses", "url": "/courses", "new_tab": False} in header


def test_sub_menu_rules(admin_api):
    menu = menu_with(admin_api)
    other = menu_with(admin_api, name="Other")
    top = add_link(admin_api, menu, link_type="url", url="/a", label="A").json()
    child = add_link(admin_api, menu, link_type="url", url="/b", label="B", parent=top["id"]).json()
    assert child["parent"] == top["id"] and child["sort_order"] == 1

    refused = {
        "too_deep": add_link(
            admin_api, menu, link_type="url", url="/c", label="C", parent=child["id"]
        ),
        "bad_parent": add_link(
            admin_api, other, link_type="url", url="/c", label="C", parent=top["id"]
        ),
        "no_target": add_link(admin_api, menu, link_type="none", label="H", parent=top["id"]),
        "no_label": add_link(admin_api, menu, link_type="none"),
    }
    for code, response in refused.items():
        assert response.status_code == 400 and response.json()["code"] == code, code
    # a link with a sub-menu cannot itself move under another link
    second = add_link(admin_api, menu, link_type="url", url="/d", label="D").json()
    response = admin_api.patch(
        f"{ADMIN}/menu-items/{top['id']}/", {"parent": second["id"]}, format="json"
    )
    assert response.json()["code"] == "too_deep"


def test_hard_delete_removes_the_sub_menu(admin_api):
    menu = menu_with(admin_api)
    top = add_link(admin_api, menu, link_type="none", label="More").json()
    add_link(admin_api, menu, link_type="url", url="/b", label="B", parent=top["id"])
    admin_api.post(f"{ADMIN}/menu-items/{top['id']}/soft-delete/")
    assert admin_api.get(f"{ADMIN}/menu-items/{top['id']}/hard/").json()["will_delete"] == {
        "menu items": 2
    }
    admin_api.delete(f"{ADMIN}/menu-items/{top['id']}/hard/", {"confirm": "More"}, format="json")
    assert not MenuItem.all_objects.filter(menu_id=menu["id"]).exists()


def test_only_admins_manage_the_website(api, make_user):
    assert api.get(f"{ADMIN}/pages/").status_code == 401
    api.force_authenticate(make_user())
    assert api.post(f"{ADMIN}/menus/", {"name": "x", "location": "header"}).status_code == 403


# --- SEO ----------------------------------------------------------------------


def test_page_gets_seo_tags_and_a_sitemap_entry(admin_api, api, page):
    data = api.get("/api/v1/public/seo/", {"path": "/about-us"}).json()
    assert data["status"] == 200
    assert data["title"] == "About us · ainolez"
    description = next(t["content"] for t in data["tags"] if t.get("name") == "description")
    assert description == "Who builds ainolez."
    assert {item["@type"] for item in data["json_ld"]} == {"WebPage", "BreadcrumbList"}
    assert "/about-us" in prerender.public_paths()

    admin_api.post(f"{ADMIN}/pages/{page['id']}/deactivate/")
    assert api.get("/api/v1/public/seo/", {"path": "/about-us"}).json()["status"] == 404


def test_page_seo_settings_follow_a_slug_change(admin_api, api, page):
    saved = admin_api.post(
        "/api/v1/admin/seo/pages/", {"path": "/about-us", "meta_title": "Meet the team"}
    ).json()
    assert saved["entity_type"] == "page" and saved["url"] == "/about-us"

    admin_api.patch(f"{ADMIN}/pages/{page['id']}/", {"slug": "team"})
    data = api.get("/api/v1/public/seo/", {"path": "/team"}).json()
    assert data["title"] == "Meet the team"


def test_prerendered_pages_carry_the_menus(admin_api, tmp_path, settings, page):
    settings.PRERENDER_DIR = str(tmp_path)
    (tmp_path / "shell.html").write_text(
        '<html><head><title>x</title></head><body><div id="root"></div></body></html>'
    )
    menu = menu_with(admin_api, "footer", "Company </script>")
    admin_api.post(
        f"{ADMIN}/menu-items/", {"menu": menu["id"], "link_type": "page", "page": page["id"]}
    )

    prerender.build()
    html = (tmp_path / "index.html").read_text(encoding="utf-8")
    script = html.split('<script type="application/json" id="site-menus">')[1].split("</script>")[0]
    assert r"Company <\/script>" in script  # cannot close the script element early
    menus = json.loads(script)
    company = next(m for m in menus["footer"] if m["id"] == menu["id"])
    assert company["items"] == [{"label": "About us", "url": "/about-us", "new_tab": False}]


def test_menu_changes_schedule_a_prerender_rebuild(admin_api):
    Job.objects.all().delete()
    menu = menu_with(admin_api)
    assert Job.objects.filter(type=BUILD_JOB, status=Job.Status.QUEUED).exists()

    Job.objects.all().delete()
    admin_api.post(f"{ADMIN}/menus/reorder/", {"ids": [menu["id"]]}, format="json")
    assert Job.objects.filter(type=BUILD_JOB).exists()
