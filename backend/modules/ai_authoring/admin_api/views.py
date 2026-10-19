"""Admin -> AI course generator."""

from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.routers import SimpleRouter

from modules.ai_authoring import services
from modules.ai_authoring.models import CourseJob
from shared.admin_api import AdminResourceViewSet

RECORD_FIELDS = ["is_active", "created_at", "updated_at", "deleted_at"]


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseJob
        fields = [
            "id", "topic", "level", "audience", "language_key", "category_id",
            "chapters_count", "lessons_per_chapter", "notes", "outline", "status",
            "course_id", "lessons_total", "lessons_done", "lessons_failed",
            "tokens_in", "tokens_out", "cost_usd", "error", *RECORD_FIELDS,
        ]  # fmt: skip
        read_only_fields = [
            "outline", "status", "course_id", "lessons_total", "lessons_done",
            "lessons_failed", "tokens_in", "tokens_out", "cost_usd", "error", *RECORD_FIELDS,
        ]  # fmt: skip


class JobViewSet(AdminResourceViewSet):
    """POST / starts a job (Claude writes the outline). Then:
    PATCH /{id}/outline/ {outline}, POST /{id}/generate/ {category_id}, POST /{id}/retry/."""

    model = CourseJob
    serializer_class = JobSerializer
    search_fields = ("topic",)
    filter_fields = ("status",)

    def perform_create(self, serializer):
        serializer.instance = services.start_job(dict(serializer.validated_data), self.request.user)

    def perform_update(self, serializer):
        # Only the category can change after the start (it is needed to generate).
        job = serializer.instance
        if "category_id" in serializer.validated_data:
            job.category_id = serializer.validated_data["category_id"]
            job.save(update_fields=["category_id", "updated_at"])

    @action(detail=True, methods=["patch"])
    def outline(self, request, pk=None):
        job = services.save_outline(
            self.get_object(), request.data.get("outline") or {}, request.user
        )
        return Response(self.get_serializer(job).data)

    @action(detail=True, methods=["post"])
    def generate(self, request, pk=None):
        job = services.generate(self.get_object(), request.user)
        return Response(self.get_serializer(job).data, status=status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=["post"])
    def retry(self, request, pk=None):
        job = services.retry(self.get_object(), request.user)
        return Response(self.get_serializer(job).data, status=status.HTTP_202_ACCEPTED)


router = SimpleRouter()
router.register("jobs", JobViewSet, basename="admin-ai-course-job")
urlpatterns = router.urls
