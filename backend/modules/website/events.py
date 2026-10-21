from dataclasses import dataclass


@dataclass(frozen=True)
class PageChanged:
    """A site page was created, edited, hidden, trashed or restored."""

    page_id: int


@dataclass(frozen=True)
class MenuChanged:
    """A menu or one of its links was created, edited, reordered, hidden, trashed or restored."""

    menu_id: int
