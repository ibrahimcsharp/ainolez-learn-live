"""Cleans HTML before it is stored or shown. Scripts, styles and event handlers never survive."""

import nh3

from modules.content_tools.embeds import is_allowed_iframe

TAGS = nh3.ALLOWED_TAGS | {"iframe", "video", "source"}
ATTRIBUTES = {
    "*": {"class", "id", "title"},
    "a": {"href"},
    "img": {"src", "alt", "width", "height", "loading"},
    "iframe": {"src", "allow", "allowfullscreen", "loading"},
    "video": {"src", "controls", "preload", "poster"},
    "source": {"src", "type"},
}


def _filter(tag: str, attribute: str, value: str) -> str | None:
    if tag == "iframe" and attribute == "src" and not is_allowed_iframe(value):
        return None
    return value


def sanitize(html: str) -> str:
    return nh3.clean(
        html,
        tags=TAGS,
        attributes=ATTRIBUTES,
        attribute_filter=_filter,
        url_schemes={"http", "https", "mailto"},
    )
