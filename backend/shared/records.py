"""
Universal record controls (PLANNING.md §4): activate, deactivate, soft delete,
restore, hard delete and reorder. Every action is audit-logged.
"""

from collections.abc import Iterable

from django.db import IntegrityError, router, transaction
from django.db.models import Model
from django.db.models.deletion import Collector, ProtectedError

from shared import audit
from shared.exceptions import ServiceError


def display_name(obj: Model) -> str:
    """What the admin must type to confirm a hard delete."""
    for field in ("title", "name", "original_name"):
        if hasattr(obj, field):
            return getattr(obj, field)
    return str(obj.pk)


def set_active(obj: Model, active: bool, by) -> None:
    obj.is_active = active
    obj.updated_by = by
    obj.save(update_fields=["is_active", "updated_by", "updated_at"])
    audit.record(f"{_label(obj)}.{'activated' if active else 'deactivated'}", actor=by, entity=obj)


def soft_delete(obj: Model, by) -> None:
    obj.soft_delete(by=by)
    audit.record(f"{_label(obj)}.trashed", actor=by, entity=obj)


def restore(obj: Model, by) -> None:
    try:
        with transaction.atomic():
            obj.restore()
    except IntegrityError as exc:  # its slug was reused while it sat in the Trash
        raise ServiceError(
            "Another live item already uses this slug. Rename one of them first.", "slug_in_use"
        ) from exc
    audit.record(f"{_label(obj)}.restored", actor=by, entity=obj)


def hard_delete_preview(obj: Model) -> dict:
    """Everything a hard delete would remove, counted per kind of record."""
    collector = Collector(using=router.db_for_write(type(obj)))
    try:
        collector.collect([obj])
    except ProtectedError as exc:  # e.g. a course that has certificates
        kinds = {str(row._meta.verbose_name_plural) for row in exc.protected_objects}
        raise ServiceError(
            f"This item cannot be deleted forever because it has {', '.join(sorted(kinds))}.",
            "protected",
        ) from exc
    counts: dict[str, int] = {}
    for model, rows in collector.data.items():
        counts[str(model._meta.verbose_name_plural)] = len(rows)
    for queryset in collector.fast_deletes:  # leaf rows Django deletes in one query
        name = str(queryset.model._meta.verbose_name_plural)
        counts[name] = counts.get(name, 0) + queryset.count()
    return {
        "confirm_text": display_name(obj),
        "will_delete": {k: v for k, v in counts.items() if v},
    }


def hard_delete(obj: Model, confirm_text: str, by) -> None:
    """Permanent. Only for items already in the Trash, confirmed by typing their name."""
    if obj.deleted_at is None:
        raise ServiceError("Move the item to the Trash before deleting it forever.", "not_trashed")
    if confirm_text.strip() != display_name(obj):
        raise ServiceError("The confirmation text does not match the item name.", "bad_confirm")
    preview = hard_delete_preview(obj)
    audit.record(f"{_label(obj)}.hard_deleted", actor=by, entity=obj, before=preview)
    obj.delete()


def reorder(model: type[Model], ids: Iterable[int], by) -> None:
    """Set sort_order to match the order of ``ids`` (from a drag and drop)."""
    with transaction.atomic():
        for position, pk in enumerate(ids):
            model.all_objects.filter(pk=pk).update(sort_order=position, updated_by=by)


def _label(obj: Model) -> str:
    return obj._meta.model_name
