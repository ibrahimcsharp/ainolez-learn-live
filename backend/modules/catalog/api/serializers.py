"""Shapes of the public catalog API. Only sanitised HTML is ever sent."""

from rest_framework import serializers

from modules.catalog import services
from modules.catalog.models import Category, Chapter, Course, Lesson, LessonBlock


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name", "slug", "description", "icon", "color"]


class CourseCardSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id", "title", "slug", "short_description", "level", "language_key",
            "estimated_minutes", "category", "thumbnail_url",
        ]  # fmt: skip

    def get_thumbnail_url(self, course):
        return self.context.get("thumbnails", {}).get(course.thumbnail_media_id)


class LessonLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["id", "title", "slug", "estimated_minutes"]


class ChapterOutlineSerializer(serializers.ModelSerializer):
    lessons = LessonLinkSerializer(source="visible_lessons", many=True)

    class Meta:
        model = Chapter
        fields = ["title", "description", "lessons"]


class CourseDetailSerializer(CourseCardSerializer):
    intro_video_html = serializers.SerializerMethodField()

    class Meta(CourseCardSerializer.Meta):
        fields = [*CourseCardSerializer.Meta.fields, "description", "intro_video_html"]

    def get_intro_video_html(self, course):
        return services.course_video_html(course)


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["id", "title", "slug", "summary", "estimated_minutes"]


class BlockSerializer(serializers.ModelSerializer):
    """Exercise and quiz data come from the assessment module, passed in the context
    as {"exercises": {id: ...}, "quizzes": {id: ...}} without answers."""

    example = serializers.SerializerMethodField()
    exercise = serializers.SerializerMethodField()
    quiz = serializers.SerializerMethodField()

    class Meta:
        model = LessonBlock
        fields = ["id", "type", "content_html", "example", "exercise", "quiz"]

    def get_exercise(self, block):
        return self.context.get("exercises", {}).get(block.exercise_id)

    def get_quiz(self, block):
        return self.context.get("quizzes", {}).get(block.quiz_id)

    def get_example(self, block):
        example = block.code_example
        if block.type != LessonBlock.Type.EXAMPLE or example is None:
            return None
        return {
            "title": example.title,
            "language": example.language,
            "run_mode": example.run_mode,
            "starter_code": example.starter_code,
        }
