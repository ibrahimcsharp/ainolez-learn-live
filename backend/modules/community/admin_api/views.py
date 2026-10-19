from django.urls import path
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.routers import SimpleRouter
from rest_framework.views import APIView

from modules.community import selectors, services
from modules.community.models import Space
from shared.admin_api import ServiceViewSet
from shared.permissions import IsSuperAdmin

RECORD_FIELDS = ["is_active", "created_at", "updated_at", "deleted_at"]


class SpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Space
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "icon",
            "sort_order",
            "posting_rule",
            *RECORD_FIELDS,
        ]
        read_only_fields = RECORD_FIELDS
        extra_kwargs = {"slug": {"required": False, "allow_blank": True}}


class SpaceViewSet(ServiceViewSet):
    model = Space
    serializer_class = SpaceSerializer
    save = services.save_space
    ordering = ("sort_order", "name")


class QueueView(APIView):
    """The moderation queue and the open reports."""

    permission_classes = [IsSuperAdmin]

    def get(self, request):
        return Response(
            {"pending": selectors.moderation_queue(), "reports": selectors.open_reports()}
        )


class ModerateView(APIView):
    """Body: {target_type, target_id, action, reason}."""

    permission_classes = [IsSuperAdmin]

    def post(self, request):
        data = request.data
        item = services.moderate(
            request.user, str(data.get("target_type", "")), int(data.get("target_id", 0)),
            str(data.get("action", "")), str(data.get("reason", "")),
        )  # fmt: skip
        return Response({"id": item.pk, "status": item.status})


class ResolveReportView(APIView):
    """Body: {dismiss: bool, note}."""

    permission_classes = [IsSuperAdmin]

    def post(self, request, report_id):
        dismiss = bool(request.data.get("dismiss"))
        report = services.resolve_report(
            request.user, report_id, dismiss, str(request.data.get("note", ""))
        )
        return Response({"id": report.pk, "status": report.status})


class SettingsView(APIView):
    """The blocked-words filter: GET, and PATCH {blocked_words, blocked_action}."""

    permission_classes = [IsSuperAdmin]

    def get(self, request):
        return Response(self._data(selectors.community_settings()))

    def patch(self, request):
        return Response(self._data(services.update_settings(request.data, request.user)))

    @staticmethod
    def _data(rules):
        return {"blocked_words": rules.blocked_words or "", "blocked_action": rules.blocked_action}


router = SimpleRouter()
router.register("spaces", SpaceViewSet, basename="admin-space")
urlpatterns = [
    path("queue/", QueueView.as_view()),
    path("settings/", SettingsView.as_view()),
    path("moderate/", ModerateView.as_view()),
    path("reports/<int:report_id>/resolve/", ResolveReportView.as_view()),
    *router.urls,
]
