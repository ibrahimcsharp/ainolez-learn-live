from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.routers import SimpleRouter

from modules.certification import services
from modules.certification.models import Certificate, CertificateTemplate
from shared.admin_api import AdminResourceViewSet, ServiceViewSet

RECORD_FIELDS = ["is_active", "created_at", "updated_at", "deleted_at"]


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = [
            "id", "certificate_code", "status", "learner_name", "course_title", "course_id",
            "issued_at", "revoked_at", "revoke_reason", "view_count", "verify_url", "pdf_url",
            *RECORD_FIELDS,
        ]  # fmt: skip
        read_only_fields = fields


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CertificateTemplate
        fields = [
            "id", "name", "heading", "body_text", "signer_name", "signer_title",
            "primary_color", "accent_color", "is_default", *RECORD_FIELDS,
        ]  # fmt: skip
        read_only_fields = RECORD_FIELDS


class CertificateViewSet(AdminResourceViewSet):
    """Certificates are issued automatically; admins review, revoke and re-issue them."""

    model = Certificate
    serializer_class = CertificateSerializer
    search_fields = ("learner_name", "course_title", "certificate_code")
    filter_fields = ("status", "course_id")
    ordering = ("-created_at",)

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        return Response(self.get_serializer(services.approve(self.get_object(), request.user)).data)

    @action(detail=True, methods=["post"])
    def revoke(self, request, pk=None):
        cert = services.revoke(self.get_object(), str(request.data.get("reason", "")), request.user)
        return Response(self.get_serializer(cert).data)

    @action(detail=True, methods=["post"])
    def reissue(self, request, pk=None):
        return Response(self.get_serializer(services.reissue(self.get_object(), request.user)).data)


class TemplateViewSet(ServiceViewSet):
    model = CertificateTemplate
    serializer_class = TemplateSerializer
    save = services.save_template
    ordering = ("-is_default", "name")


router = SimpleRouter()
router.register("certificates", CertificateViewSet, basename="admin-certificate")
router.register("templates", TemplateViewSet, basename="admin-certificate-template")
urlpatterns = router.urls
