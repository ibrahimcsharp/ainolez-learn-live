from dataclasses import dataclass


@dataclass(frozen=True)
class PageChanged:
    """A site page was created, edited, hidden, trashed or restored."""

    page_id: int
