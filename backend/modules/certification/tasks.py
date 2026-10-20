from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.mail import send_mail

from modules.certification import render
from modules.certification.models import Certificate, CertificateTemplate
from modules.certification.services import default_template
from modules.identity import selectors as identity
from shared.jobs import job


@job("certification.render")
def render_certificate(payload: dict) -> None:
    """Draw the PDF and share image, then (optionally) email the learner."""
    cert = Certificate.objects.filter(pk=payload["certificate_id"]).first()
    if cert is None or cert.status != Certificate.Status.ISSUED:
        return
    # A template removed since issuing falls back to the default, then to built-in wording.
    template = cert.template or default_template() or CertificateTemplate()
    cert.pdf_path = _store(
        f"certificates/{cert.certificate_code}.pdf", render.certificate_pdf(cert, template)
    )
    cert.image_path = _store(
        f"certificates/{cert.certificate_code}.png", render.share_image(cert, template)
    )
    cert.save(update_fields=["pdf_path", "image_path", "updated_at"])

    if payload.get("notify"):
        send_mail(
            subject=f"Your ainolez certificate: {cert.course_title}",
            message=(
                f"Congratulations {cert.learner_name}!\n\n"
                f"You finished {cert.course_title}. Your certificate is ready:\n"
                f"{cert.verify_url}\n\n"
                "Add it to your LinkedIn profile from that page.\n\nLearn it. Code it. Own it."
            ),
            from_email=None,
            recipient_list=[identity.get_email(cert.user_id)],
        )


def _store(name: str, data: bytes) -> str:
    default_storage.delete(name)  # replace an older version
    return default_storage.save(name, ContentFile(data))
