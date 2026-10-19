"""The AI control panel (PLANNING.md 6.6, item 12)."""

from django.shortcuts import get_object_or_404
from django.urls import path
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.routers import SimpleRouter
from rest_framework.views import APIView

from modules.assistant import claude, knowledge, selectors, services
from modules.assistant.models import FAQ, AISettings, Conversation, KBSource, PromptVersion
from shared import jobs
from shared.admin_api import ServiceViewSet
from shared.exceptions import ServiceError
from shared.permissions import IsSuperAdmin

RECORD_FIELDS = ["is_active", "created_at", "updated_at", "deleted_at"]


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AISettings
        fields = [*services.SETTING_FIELDS, "updated_at"]
        read_only_fields = ["updated_at"]


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ["id", "question", "answer_md", "keywords", "hit_count", *RECORD_FIELDS]
        read_only_fields = ["hit_count", *RECORD_FIELDS]


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = KBSource
        fields = [
            "id",
            "type",
            "lesson_id",
            "title",
            "url",
            "body",
            "status",
            "error",
            "chunk_count",
            "last_indexed_at",
            *RECORD_FIELDS,
        ]
        read_only_fields = [
            "type",
            "lesson_id",
            "status",
            "error",
            "chunk_count",
            "last_indexed_at",
            *RECORD_FIELDS,
        ]


class SettingsView(APIView):
    permission_classes = [IsSuperAdmin]

    def get(self, request):
        data = SettingsSerializer(services.settings_row()).data
        return Response({**data, "models": claude.MODELS})

    def patch(self, request):
        serializer = SettingsSerializer(services.settings_row(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        config = services.update_settings(serializer.validated_data, request.user)
        return Response({**SettingsSerializer(config).data, "models": claude.MODELS})


class PromptsView(APIView):
    """GET the versions; POST {system_prompt, notes, make_current} saves a new one."""

    permission_classes = [IsSuperAdmin]

    def get(self, request):
        versions = PromptVersion.objects.order_by("-version_no")
        return Response(
            [
                {
                    "id": v.pk,
                    "version_no": v.version_no,
                    "system_prompt": v.system_prompt,
                    "notes": v.notes,
                    "is_current": v.is_current,
                    "created_at": v.created_at,
                }
                for v in versions
            ]
        )

    def post(self, request):
        version = services.new_prompt_version(
            str(request.data.get("system_prompt", "")),
            str(request.data.get("notes", ""))[:255],
            bool(request.data.get("make_current", True)),
            request.user,
        )
        return Response(
            {"id": version.pk, "version_no": version.version_no}, status=status.HTTP_201_CREATED
        )


class ActivatePromptView(APIView):
    permission_classes = [IsSuperAdmin]

    def post(self, request, version_id):
        services.activate_prompt(get_object_or_404(PromptVersion, pk=version_id), request.user)
        return Response({"detail": "This version is now in use."})


class FAQViewSet(ServiceViewSet):
    model = FAQ
    serializer_class = FAQSerializer
    save = services.save_faq
    search_fields = ("question", "keywords")
    ordering = ("question",)


class SourceViewSet(ServiceViewSet):
    model = KBSource
    serializer_class = SourceSerializer
    save = services.save_document
    search_fields = ("title",)
    filter_fields = ("type", "status")
    ordering = ("type", "title")

    @action(detail=True, methods=["post"])
    def reindex(self, request, pk=None):
        jobs.enqueue("assistant.index_source", {"source_id": self.get_object().pk})
        return Response({"detail": "Re-indexing within a minute."})

    @action(detail=False, methods=["post"], url_path="reindex-all")
    def reindex_all(self, request):
        jobs.enqueue("assistant.index_everything")
        return Response({"detail": "Re-indexing everything within a minute."})

    @action(detail=False, methods=["get"])
    def search(self, request):
        """Test what the tutor would read for a question."""
        lesson_id = request.query_params.get("lesson_id")
        excerpts = knowledge.search(
            request.query_params.get("q", ""), int(lesson_id) if lesson_id else None
        )
        return Response([{"title": e.title, "url": e.url, "text": e.text[:600]} for e in excerpts])


class ConversationsView(APIView):
    permission_classes = [IsSuperAdmin]

    def get(self, request):
        return Response(selectors.recent_conversations(request.query_params.get("negative") == "1"))


class ConversationDetailView(APIView):
    permission_classes = [IsSuperAdmin]

    def get(self, request, conversation_id):
        conversation = get_object_or_404(Conversation, pk=conversation_id)
        return Response(
            {
                "id": conversation.pk,
                "title": conversation.title,
                "messages": selectors.conversation_messages(conversation),
            }
        )


class UsageView(APIView):
    permission_classes = [IsSuperAdmin]

    def get(self, request):
        config = services.settings_row()
        return Response(
            {**selectors.usage_report(), "monthly_token_budget": config.monthly_token_budget}
        )


class TestConnectionView(APIView):
    """Checks the API key and model with a tiny request."""

    permission_classes = [IsSuperAdmin]

    def post(self, request):
        config = services.settings_row()
        try:
            reply = claude.complete(
                model=config.model,
                effort="low",
                max_tokens=200,
                system="You are a connection test.",
                messages=[{"role": "user", "content": "Reply with: OK"}],
            )
        except ServiceError as exc:
            return Response({"ok": False, "detail": exc.message})
        return Response(
            {"ok": True, "model": reply.model, "latency_ms": reply.latency_ms, "reply": reply.text}
        )


router = SimpleRouter()
router.register("faq", FAQViewSet, basename="admin-faq")
router.register("sources", SourceViewSet, basename="admin-kb-source")
urlpatterns = [
    path("settings/", SettingsView.as_view()),
    path("prompts/", PromptsView.as_view()),
    path("prompts/<int:version_id>/activate/", ActivatePromptView.as_view()),
    path("conversations/", ConversationsView.as_view()),
    path("conversations/<int:conversation_id>/", ConversationDetailView.as_view()),
    path("usage/", UsageView.as_view()),
    path("test/", TestConnectionView.as_view()),
    *router.urls,
]
