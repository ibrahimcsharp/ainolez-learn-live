"""Write-only audit trail: who did what, and when."""

from django.db import models

from shared.models import AuditLog


def record(
    action: str,
    *,
    actor=None,
    entity: models.Model | None = None,
    before: dict | None = None,
    after: dict | None = None,
    ip: str = "",
) -> None:
    AuditLog.objects.create(
        user=actor,
        action=action,
        entity_type=entity._meta.label_lower if entity else "",
        entity_id=entity.pk if entity else None,
        before_data=before,
        after_data=after,
        ip_address=ip,
    )


def client_ip(request) -> str:
    return request.META.get("REMOTE_ADDR", "")
