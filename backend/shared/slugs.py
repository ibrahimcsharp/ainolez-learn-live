from django.db.models import QuerySet
from django.utils.text import slugify


def unique_slug(queryset: QuerySet, text: str, exclude_pk: int | None = None) -> str:
    """slugify(text), with -2, -3 ... added if a live row in ``queryset`` already has it."""
    base = slugify(text)[:90] or "item"
    taken = set(queryset.exclude(pk=exclude_pk).values_list("slug", flat=True))
    slug, n = base, 2
    while slug in taken:
        slug, n = f"{base}-{n}", n + 1
    return slug
