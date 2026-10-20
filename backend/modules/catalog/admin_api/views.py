from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from modules.catalog import services
from modules.catalog.admin_api import serializers as s
from modules.catalog.events import CourseChanged, LessonChanged
from modules.catalog.models import Category, Chapter, Course, LearningPath, Lesson, LessonBlock
from shared.admin_api import ServiceViewSet
from shared.events import publish


class CategoryViewSet(ServiceViewSet):
    model = Category
    serializer_class = s.CategoryAdminSerializer
    save = services.save_category
    search_fields = ("name",)
    ordering = ("sort_order", "name")


class CourseViewSet(ServiceViewSet):
    model = Course
    serializer_class = s.CourseAdminSerializer
    save = services.save_course
    search_fields = ("title", "slug")
    filter_fields = ("category", "status")
    ordering = ("title",)

    def record_changed(self, course):
        publish(CourseChanged(course.pk))

    @action(detail=True, methods=["post"], url_path="publish")
    def publish_all(self, request, pk=None):
        """Publish the course and every draft lesson in it."""
        course = self.get_object()
        lessons = services.publish_course(course, request.user)
        return Response({**self.get_serializer(course).data, "lessons_published": lessons})


class ChapterViewSet(ServiceViewSet):
    model = Chapter
    serializer_class = s.ChapterAdminSerializer
    save = services.save_chapter
    search_fields = ("title",)
    filter_fields = ("course",)
    ordering = ("sort_order", "id")

    def record_changed(self, chapter):
        publish(CourseChanged(chapter.course_id))


class LessonViewSet(ServiceViewSet):
    model = Lesson
    serializer_class = s.LessonAdminSerializer
    save = services.save_lesson
    search_fields = ("title", "slug")
    filter_fields = ("course", "chapter", "status")
    ordering = ("sort_order", "id")

    def record_changed(self, lesson):
        publish(LessonChanged(lesson.pk))

    @action(detail=False, methods=["post"], url_path="import", parser_classes=[MultiPartParser])
    def import_markdown(self, request):
        """Form fields: chapter (id), files (.md or .zip, many), publish (1 to publish now)."""
        chapter = get_object_or_404(Chapter.objects, pk=request.data.get("chapter"))
        publish = request.data.get("publish") in ("1", "true", "on")
        lessons = services.import_lessons(
            chapter, request.FILES.getlist("files"), publish, request.user
        )
        return Response(
            self.get_serializer(lessons, many=True).data, status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=["get"])
    def export(self, request, pk=None):
        lesson = self.get_object()
        response = HttpResponse(
            services.export_lesson_markdown(lesson), content_type="text/markdown"
        )
        response["Content-Disposition"] = f'attachment; filename="{lesson.slug}.md"'
        return response


class BlockViewSet(ServiceViewSet):
    model = LessonBlock
    serializer_class = s.BlockAdminSerializer
    save = services.save_block
    filter_fields = ("lesson", "type")
    ordering = ("sort_order", "id")

    def record_changed(self, block):
        publish(LessonChanged(block.lesson_id))

    def get_queryset(self):
        return super().get_queryset().select_related("code_example")


class PathViewSet(ServiceViewSet):
    model = LearningPath
    serializer_class = s.PathAdminSerializer
    save = services.save_path
    search_fields = ("title",)
    ordering = ("title",)
