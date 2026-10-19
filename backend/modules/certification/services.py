"""Issue, approve, revoke and re-issue certificates. Rendering happens in a job."""

import secrets

from django.conf import settings
from django.utils import timezone

from modules.catalog import selectors as catalog
from modules.certification.models import Certificate, CertificateTemplate
from modules.identity import selectors as identity
from shared import audit, jobs
from shared.exceptions import ServiceError

# No 0/O or 1/I, so a code read aloud or typed from paper is not mistaken.
CODE_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"


def issue_for_course(user_id: int, course_id: int) -> Certificate:
    """Create the learner's certificate for a course (once). Called on CourseCompleted."""
    existing = Certificate.objects.filter(user_id=user_id, course_id=course_id).first()
    if existing:
        return existing
    needs_review = settings.CERTIFICATES_NEED_REVIEW
    cert = Certificate.objects.create(
        user_id=user_id,
        course_id=course_id,
        template=default_template(),
        certificate_code=_new_code(),
        status=Certificate.Status.PENDING_REVIEW if needs_review else Certificate.Status.ISSUED,
        learner_name=identity.display_name(user_id),
        course_title=catalog.course_summaries([course_id])[course_id]["title"],
        issued_at=None if needs_review else timezone.now(),
    )
    audit.record("certificate.created", entity=cert)
    if not needs_review:
        jobs.enqueue("certification.render", {"certificate_id": cert.pk, "notify": True})
    return cert


def approve(cert: Certificate, by) -> Certificate:
    if cert.status != Certificate.Status.PENDING_REVIEW:
        raise ServiceError("Only certificates waiting for review can be approved.", "bad_status")
    return _issue(cert, by, "certificate.approved", notify=True)


def reissue(cert: Certificate, by) -> Certificate:
    """Undo a revoke, or re-draw the files with the current template and name."""
    cert.learner_name = identity.display_name(cert.user_id) or cert.learner_name
    cert.template = default_template()
    cert.revoked_at = None
    cert.revoke_reason = ""
    return _issue(cert, by, "certificate.reissued", notify=False)


def revoke(cert: Certificate, reason: str, by) -> Certificate:
    if not reason.strip():
        raise ServiceError("Give a reason for revoking.", "reason_required")
    cert.status = Certificate.Status.REVOKED
    cert.revoked_at = timezone.now()
    cert.revoke_reason = reason.strip()[:255]
    cert.updated_by = by
    cert.save()
    audit.record("certificate.revoked", actor=by, entity=cert, after={"reason": cert.revoke_reason})
    return cert


def count_view(cert: Certificate) -> None:
    Certificate.objects.filter(pk=cert.pk).update(view_count=cert.view_count + 1)


def save_template(template: CertificateTemplate | None, data: dict, by) -> CertificateTemplate:
    template = template or CertificateTemplate()
    for name, value in data.items():
        setattr(template, name, value)
    is_new = template.pk is None
    if is_new:
        template.created_by = by
    template.updated_by = by
    template.save()
    if template.is_default:  # only one default
        CertificateTemplate.all_objects.exclude(pk=template.pk).update(is_default=False)
    audit.record(
        f"certificatetemplate.{'created' if is_new else 'updated'}", actor=by, entity=template
    )
    return template


def default_template() -> CertificateTemplate | None:
    return CertificateTemplate.objects.filter(is_active=True).order_by("-is_default", "id").first()


def _issue(cert: Certificate, by, action: str, notify: bool) -> Certificate:
    cert.status = Certificate.Status.ISSUED
    cert.issued_at = cert.issued_at or timezone.now()
    cert.updated_by = by
    cert.save()
    audit.record(action, actor=by, entity=cert)
    jobs.enqueue("certification.render", {"certificate_id": cert.pk, "notify": notify})
    return cert


def _new_code() -> str:
    while True:
        code = "".join(secrets.choice(CODE_ALPHABET) for _ in range(12))
        if not Certificate.all_objects.filter(certificate_code=code).exists():
            return code
