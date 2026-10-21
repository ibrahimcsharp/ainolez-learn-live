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
    a link being {"label", "url", "new_tab"}, plus "children": [link...] when
    it has a sub-menu (a heading with no link has "url": None). A header
    menu shown as a dropdown is one such heading, named after the menu. Links to
    hidden pages or unpublished courses are left out, with their sub-menu."""
    menus, links = _navigation()
    footer = [
        {"id": menu.pk, "name": menu.name, "items": [link for _, link in links[menu.pk]]}
        for menu in menus
        if menu.location == "footer" and links[menu.pk]
    ]
    return {"header": [entry["link"] for entry in header_bar(menus, links)], "footer": footer}


def header_bar(menus=None, links=None) -> list[dict]:
    """What the header bar shows, in order: [{"kind": "item" | "menu", "id", "link"}].
    The top-level links of "links" menus and whole "dropdown" menus share one
    order (header_position, set in Admin -> Menus). Entries not placed yet come
    after the placed ones, in menu order."""
    if menus is None:
        menus, links = _navigation()
    entries = []
    for menu in menus:
        if menu.location != "header" or not links[menu.pk]:
            continue
        if menu.show_as == Menu.ShowAs.LINKS:
            for item, link in links[menu.pk]:
                entries.append(
                    {"kind": "item", "id": item.pk, "link": link, "at": item.header_position}
                )
        else:  # the menu's name in the bar, its links (and their sub-links) under it
            link = {
                "label": menu.name,
                "url": None,
                "new_tab": False,
                "children": [link for _, link in links[menu.pk]],
            }
            entries.append(
                {"kind": "menu", "id": menu.pk, "link": link, "at": menu.header_position}
            )
    placed = sorted((e for e in entries if e["at"] is not None), key=lambda e: e["at"])
    rest = [e for e in entries if e["at"] is None]
    return [{k: e[k] for k in ("kind", "id", "link")} for e in placed + rest]


def _navigation() -> tuple[list[Menu], dict[int, list[tuple[MenuItem, dict]]]]:
    """Active menus, and for each its visible top-level links (with sub-links)."""
    menus = list(Menu.objects.filter(is_active=True).order_by("location", "sort_order", "id"))
    items = list(
        MenuItem.objects.filter(menu__in=menus, is_active=True)
        .select_related("page")
        .order_by("sort_order", "id")
    )
    courses = catalog.public_course_links(
        item.course_id for item in items if item.link_type == MenuItem.LinkType.COURSE
    )
    children: dict[int, list[dict]] = {}
    for item in items:
        link = item.parent_id and _link(item, courses)
        if link:
            children.setdefault(item.parent_id, []).append(link)

    links: dict[int, list[tuple[MenuItem, dict]]] = {menu.pk: [] for menu in menus}
    for item in items:
        if item.parent_id:
            continue
        link = _link(item, courses)
        if link and item.pk in children:
            link["children"] = children[item.pk]
        if link and (link["url"] or "children" in link):  # a heading needs its sub-menu
            links[item.menu_id].append((item, link))
    return menus, links


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
        elif item.link_type == MenuItem.LinkType.NONE:
            targets[item.pk] = "Heading only: opens its sub-menu"
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
    elif item.link_type == MenuItem.LinkType.NONE:
        url, title = None, item.label
    else:
        url, title = item.url, item.url
    return {"label": item.label or title, "url": url, "new_tab": item.open_in_new_tab}
