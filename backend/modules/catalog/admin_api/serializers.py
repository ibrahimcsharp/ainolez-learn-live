from rest_framework import serializers

from modules.assessment import selectors as assessment
from modules.catalog.models import Category, Chapter, Course, LearningPath, Lesson, LessonBlock

RECORD_FIELDS = ["is_active", "created_at", "updated_at", "deleted_at"]
SLUG = {"required": False, "allow_blank": True}


class CategoryAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "icon",
            "color",
            "sort_order",
            *RECORD_FIELDS,
        ]
        read_only_fields = RECORD_FIELDS
        extra_kwargs = {"slug": SLUG}


class CourseAdminSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Course
        fields = [
            "id", "category", "category_name", "title", "slug", "short_description",
            "description", "level", "language_key", "thumbnail_media_id", "intro_video_url",
            "estimated_minutes", "status", "ai_generated", "published_at", *RECORD_FIELDS,
        ]  # fmt: skip
        read_only_fields = ["ai_generated", "published_at", *RECORD_FIELDS]
        extra_kwargs = {"slug": SLUG}


class ChapterAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ["id", "course", "title", "description", "sort_order", *RECORD_FIELDS]
        read_only_fields = ["sort_order", *RECORD_FIELDS]


class LessonAdminSerializer(serializers.ModelSerializer):
    course_slug = serializers.CharField(source="course.slug", read_only=True)

    class Meta:
        model = Lesson
        fields = [
            "id", "course", "course_slug", "chapter", "title", "slug", "summary",
            "estimated_minutes", "status", "ai_generated", "sort_order", "published_at",
            *RECORD_FIELDS,
        ]  # fmt: skip
        read_only_fields = ["course", "ai_generated", "sort_order", "published_at", *RECORD_FIELDS]
        extra_kwargs = {"slug": SLUG}


class BlockAdminSerializer(serializers.ModelSerializer):
    """For example blocks, ``example`` is {title, language, starter_code}."""

    example = serializers.DictField(required=False, write_only=True)
    exercise = serializers.DictField(required=False, write_only=True)

    class Meta:
        model = LessonBlock
        fields = [
            "id", "lesson", "type", "sort_order", "content_md", "content_html", "data",
            "media_id", "example", "exercise", "quiz_id", *RECORD_FIELDS,
        ]  # fmt: skip
        read_only_fields = ["sort_order", "content_html", *RECORD_FIELDS]

    def to_representation(self, block):
        data = super().to_representation(block)
        example = block.code_example
        data["example"] = example and {
            "title": example.title,
            "language": example.language,
            "starter_code": example.starter_code,
        }
        data["exercise"] = assessment.exercise_for_admin(block.exercise_id)
        return data


class PathAdminSerializer(serializers.ModelSerializer):
    course_ids = serializers.ListField(child=serializers.IntegerField(), required=False)

    class Meta:
        model = LearningPath
        fields = ["id", "title", "slug", "description", "level", "course_ids", *RECORD_FIELDS]
        read_only_fields = RECORD_FIELDS
        extra_kwargs = {"slug": SLUG}

    def to_representation(self, path):
        data = super().to_representation(path)
        data["course_ids"] = list(
            path.path_courses.order_by("sort_order").values_list("course_id", flat=True)
        )
        return data
