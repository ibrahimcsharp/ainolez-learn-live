"""
Website use cases: pages the admin writes, and the header and footer menus.

Pages live at /<slug>, the same place as courses, so a page slug may not be
a reserved app route or a course slug (and catalog refuses course slugs a
page already uses).
"""

import re

from django.db import transaction
from django.db.models import Max, Model
from django.utils.text import slugify

from modules.catalog import selectors as catalog
from modules.catalog import services as catalog_services
from modules.content_tools import services as content
from modules.website import selectors
from modules.website.events import MenuChanged, PageChanged
from modules.website.models import Menu, MenuItem, SitePage
from shared import audit, records
from shared.events import publish
from shared.exceptions import ServiceError

SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
URL_START = ("/", "https://", "http://", "mailto:")


def save_page(page: SitePage | None, data: dict, by) -> SitePage:
    """Store a page and turn its Markdown into the safe HTML the public page shows."""
    page = page or SitePage()
    wanted = (data.pop("slug", "") or "").strip()
    _assign(page, data)
    if not (page.title or "").strip():
        raise ServiceError("Give the page a title.", "no_title")
    page.slug = _page_slug(page, wanted)
    if page.kind == SitePage.Kind.CODE:
        if not (page.code_html or "").strip() and not (page.code_js or "").strip():
            raise ServiceError("Add some HTML (or JavaScript) for the page.", "no_code")
        # The page runs in a sandboxed iframe; this text-only copy is for search engines.
        page.content_html = content.sanitize(page.code_html or "")
    elif page.kind == SitePage.Kind.MARKDOWN:
        page.content_html = content.render_markdown(page.content_md or "")  # nh3-sanitised
    else:
        raise ServiceError("Choose a written page or a custom code page.", "bad_kind")
    _save(page, by)
    publish(PageChanged(page.pk))
    return page


def restore_page(page: SitePage, by) -> None:
    """Out of the Trash, unless a course or reserved route took its address meanwhile."""
    if _slug_blocked(page.slug):
        raise ServiceError(
            f"/{page.slug} is now used by a course or the site. Rename the page first.",
            "slug_in_use",
        )
    records.restore(page, by)


def save_menu(menu: Menu | None, data: dict, by) -> Menu:
    is_new = menu is None
    menu = menu or Menu()
    _assign(menu, data)
    if not (menu.name or "").strip():
        raise ServiceError("Give the menu a name.", "no_name")
    if is_new:
        menu.sort_order = _next_order(Menu.objects.filter(location=menu.location))
    _save(menu, by)
    publish(MenuChanged(menu.pk))
    return menu


def save_menu_item(item: MenuItem | None, data: dict, by) -> MenuItem:
    """A link to a page, a course or a URL (or a heading with no link, for a
    sub-menu). Only the chosen target is kept. A link can sit under a
    top-level link of the same menu, one level deep."""
    is_new = item is None
    item = item or MenuItem()
    old_parent, old_menu = item.parent_id, item.menu_id
    _assign(item, data)
    item.label = (item.label or "").strip()
    item.url = (item.url or "").strip()
    has_children = not is_new and MenuItem.objects.filter(parent=item).exists()
    if item.parent is not None:
        parent = item.parent
        if parent.pk == item.pk or parent.menu_id != item.menu_id:
            raise ServiceError("Put the link under a link of the same menu.", "bad_parent")
        if parent.parent_id is not None or has_children:
            raise ServiceError("Sub-menus go one level deep only.", "too_deep")
    kind = item.link_type
    if kind == MenuItem.LinkType.NONE:
        if item.parent is not None:
            raise ServiceError("A sub-menu link must open something.", "no_target")
        if not item.label:
            raise ServiceError("A heading needs a label.", "no_label")
        item.page, item.course_id, item.url, item.open_in_new_tab = None, None, "", False
    elif kind == MenuItem.LinkType.PAGE:
        if item.page_id is None:
            raise ServiceError("Pick the page this link opens.", "no_page")
        item.course_id, item.url = None, ""
    elif kind == MenuItem.LinkType.COURSE:
        if not item.course_id or not catalog.course_exists(item.course_id):
            raise ServiceError("Pick the course this link opens.", "no_course")
        item.page, item.url = None, ""
    elif kind == MenuItem.LinkType.URL:
        if not item.url.startswith(URL_START) or item.url.startswith("//"):
            raise ServiceError(
                "Use a path like /courses, a full https:// link or mailto:.", "bad_url"
            )
        if not item.label:
            raise ServiceError("A link to a URL needs a label.", "no_label")
        item.page, item.course_id = None, None
    else:
        raise ServiceError("Choose what the link opens: a page, a course or a URL.", "bad_type")
    if is_new or item.parent_id != old_parent or item.menu_id != old_menu:
        siblings = MenuItem.objects.filter(menu=item.menu, parent=item.parent).exclude(pk=item.pk)
        item.sort_order = _next_order(siblings)  # last among its new neighbours
    with transaction.atomic():
        _save(item, by)
        if has_children and item.menu_id != old_menu:
            MenuItem.all_objects.filter(parent=item).update(menu=item.menu)  # sub-menu moves too
    publish(MenuChanged(item.menu_id))
    return item


def save_header_order(entries: list, by) -> None:
    """Place the header bar's links and dropdown menus in the order given:
    [{"kind": "item" | "menu", "id"}...], every entry the bar shows now."""
    try:
        wanted = [(str(entry["kind"]), int(entry["id"])) for entry in entries]
    except (KeyError, TypeError, ValueError) as exc:
        raise ServiceError("Send the header entries as kind and id.", "bad_order") from exc
    current = [(entry["kind"], entry["id"]) for entry in selectors.header_bar()]
    if sorted(wanted) != sorted(current):
        raise ServiceError("The header changed meanwhile. Reload the page and try again.", "stale")
    with transaction.atomic():
        for position, (kind, pk) in enumerate(wanted):
            model = Menu if kind == "menu" else MenuItem
            model.all_objects.filter(pk=pk).update(header_position=position, updated_by=by)
    audit.record("menu.header_ordered", actor=by, after={"order": wanted})
    publish(MenuChanged(0))


# --- helpers ----------------------------------------------------------------


def _page_slug(page: SitePage, wanted: str) -> str:
    if wanted:
        if not SLUG.match(wanted):
            raise ServiceError(
                "Use lowercase letters, numbers and - in the web address.", "bad_slug"
            )
        if wanted in catalog_services.RESERVED_SLUGS:
            raise ServiceError(
                f"'{wanted}' is reserved for the site. Pick another.", "slug_reserved"
            )
        if catalog.course_slug_taken(wanted):
            raise ServiceError(f"A course already uses /{wanted}.", "slug_taken")
        if SitePage.objects.filter(slug=wanted).exclude(pk=page.pk).exists():
            raise ServiceError(f"Another page already uses /{wanted}.", "slug_taken")
        return wanted
    if page.pk and page.slug:
        return page.slug  # keep URLs stable when only the title changes
    base = slugify(page.title)[:90] or "page"
    slug, n = base, 2
    while _slug_blocked(slug) or SitePage.objects.filter(slug=slug).exists():
        slug, n = f"{base}-{n}", n + 1
    return slug


def _slug_blocked(slug: str) -> bool:
    return slug in catalog_services.RESERVED_SLUGS or catalog.course_slug_taken(slug)


def _assign(obj: Model, data: dict) -> None:
    for field, value in data.items():
        setattr(obj, field, value)


def _save(obj: Model, by) -> Model:
    is_new = obj.pk is None
    if is_new:
        obj.created_by = by
    obj.updated_by = by
    with transaction.atomic():
        obj.save()
    audit.record(
        f"{obj._meta.model_name}.{'created' if is_new else 'updated'}", actor=by, entity=obj
    )
    return obj


def _next_order(siblings) -> int:
    return (siblings.aggregate(m=Max("sort_order"))["m"] or 0) + 1
