from modules.certification.models import Certificate

PUBLIC_STATUSES = (Certificate.Status.ISSUED, Certificate.Status.REVOKED)


def public_certificate(code: str) -> Certificate | None:
    """Issued or revoked certificates can be verified; pending ones cannot."""
    return Certificate.objects.filter(
        certificate_code=code.upper(), status__in=PUBLIC_STATUSES, is_active=True
    ).first()


def counts() -> dict[str, int]:
    live = Certificate.objects.filter(is_active=True)
    return {
        "issued": live.filter(status=Certificate.Status.ISSUED).count(),
        "pending_review": live.filter(status=Certificate.Status.PENDING_REVIEW).count(),
    }


def learner_certificates(user_id: int) -> list[dict]:
    return [
        {
            "code": cert.certificate_code,
            "course_title": cert.course_title,
            "status": cert.status,
            "issued_at": cert.issued_at,
        }
        for cert in Certificate.objects.filter(user_id=user_id, is_active=True).order_by(
            "-created_at"
        )
    ]
