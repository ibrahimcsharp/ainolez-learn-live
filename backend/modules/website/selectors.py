"""Read queries. Public ones only return live, active content."""

from modules.catalog import selectors as catalog
from modules.website.models import Menu, MenuItem, SitePage


def public_page(slug: str) -> SitePage | None:
    return SitePage.objects.filter(slug=slug, is_active=True).first()


def page_slug_taken(slug: str, exclude_pk: int | None = None) -> bool:
    """True when a live page (hidden ones included) already uses ``slug``."""
    return SitePage.objects.filter(slug=slug).exclude(pk=exclude_pk).exists()


def find_page(slug: str) -> int | None:
    """The id of the live page at /<slug>, hidden ones included."""
    return SitePage.objects.filter(slug=slug).values_list("pk", flat=True).first()


def page_exists(page_id: int) -> bool:
    return SitePage.objects.filter(pk=page_id).exists()


def page_urls(ids) -> dict[int, str]:
    """{page id: "/about"} for live pages."""
    rows = SitePage.objects.filter(pk__in=list(ids)).values_list("pk", "slug")
    return {pk: f"/{slug}" for pk, slug in rows}


def sitemap_pages() -> list[dict]:
    """Every active page: {type, id, url, updated_at}."""
    return [
        {"type": "page", "id": page.pk, "url": f"/{page.slug}", "updated_at": page.updated_at}
        for page in SitePage.objects.filter(is_active=True).order_by("slug")
    ]


def public_menus() -> dict:
    """The website's navigation:
    {"header": [link...], "footer": [{"id", "name", "items": [link...]}...]},
    a link being {"label", "url", "new_tab"}. Links to hidden pages or
    unpublished courses are left out."""
    menus = list(Menu.objects.filter(is_active=True).order_by("location", "sort_order", "id"))
    items = list(
        MenuItem.objects.filter(menu__in=menus, is_active=True)
        .select_related("page")
        .order_by("sort_order", "id")
    )
    courses = catalog.public_course_links(
        item.course_id for item in items if item.link_type == MenuItem.LinkType.COURSE
    )
    links: dict[int, list[dict]] = {menu.pk: [] for menu in menus}
    for item in items:
        link = _link(item, courses)
        if link:
            links[item.menu_id].append(link)

    header = [link for menu in menus if menu.location == "header" for link in links[menu.pk]]
    footer = [
        {"id": menu.pk, "name": menu.name, "items": links[menu.pk]}
        for menu in menus
        if menu.location == "footer" and links[menu.pk]
    ]
    return {"header": header, "footer": footer}


def item_targets(items: list[MenuItem]) -> dict[int, str]:
    """{item id: what it links to} for the admin list, e.g. "/about" or "Course: Python"."""
    courses = catalog.course_summaries(
        item.course_id for item in items if item.link_type == MenuItem.LinkType.COURSE
    )
    targets = {}
    for item in items:
        if item.link_type == MenuItem.LinkType.PAGE:
            page = item.page
            gone = page is None or page.deleted_at is not None
            targets[item.pk] = "(page in the Trash)" if gone else f"Page: /{page.slug}"
        elif item.link_type == MenuItem.LinkType.COURSE:
            course = courses.get(item.course_id)
            targets[item.pk] = f"Course: /{course['slug']}" if course else "(course removed)"
        else:
            targets[item.pk] = item.url
    return targets


def _link(item: MenuItem, courses: dict[int, dict]) -> dict | None:
    if item.link_type == MenuItem.LinkType.PAGE:
        page = item.page
        if page is None or page.deleted_at is not None or not page.is_active:
            return None
        url, title = f"/{page.slug}", page.title
    elif item.link_type == MenuItem.LinkType.COURSE:
        course = courses.get(item.course_id)
        if course is None:
            return None
        url, title = f"/{course['slug']}", course["title"]
    else:
        url, title = item.url, item.url
    return {"label": item.label or title, "url": url, "new_tab": item.open_in_new_tab}
