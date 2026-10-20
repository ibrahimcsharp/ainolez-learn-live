"""Tables from database/schema/0008_certification.sql."""

from django.conf import settings
from django.db import models

from shared.models import BaseModel


class CertificateTemplate(BaseModel):
    name = models.CharField(max_length=100)
    heading = models.CharField(max_length=100, default="Certificate of Completion")
    body_text = models.CharField(max_length=300, default="has successfully completed the course")
    signer_name = models.CharField(max_length=100, blank=True)
    signer_title = models.CharField(max_length=100, blank=True)
    primary_color = models.CharField(max_length=7, default="#05192D")
    accent_color = models.CharField(max_length=7, default="#03EF62")
    is_default = models.BooleanField(default=False)

    class Meta(BaseModel.Meta):
        managed = False
        db_table = "certificate_templates"


class Certificate(BaseModel):
    class Status(models.TextChoices):
        PENDING_REVIEW = "pending_review"
        ISSUED = "issued"
        REVOKED = "revoked"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="+")
    course_id = models.BigIntegerField()  # catalog module
    template = models.ForeignKey(
        CertificateTemplate, on_delete=models.SET_NULL, null=True, related_name="+"
    )
    certificate_code = models.CharField(max_length=12, unique=True)
    status = models.CharField(max_length=20, choices=Status, default=Status.ISSUED)
    learner_name = models.CharField(max_length=120)
    course_title = models.CharField(max_length=200)
    pdf_path = models.CharField(max_length=255, blank=True)
    image_path = models.CharField(max_length=255, blank=True)
    issued_at = models.DateTimeField(null=True)
    revoked_at = models.DateTimeField(null=True)
    revoke_reason = models.CharField(max_length=255, blank=True)
    view_count = models.IntegerField(default=0)

    class Meta(BaseModel.Meta):
        managed = False
        db_table = "certificates"

    @property
    def title(self) -> str:
        """Used as the confirm text for a hard delete."""
        return self.certificate_code

    @property
    def verify_url(self) -> str:
        return f"{settings.FRONTEND_URL}/certificates/{self.certificate_code}"

    @property
    def pdf_url(self) -> str:
        return settings.MEDIA_URL + self.pdf_path if self.pdf_path else ""

    @property
    def image_url(self) -> str:
        return settings.MEDIA_URL + self.image_path if self.image_path else ""
