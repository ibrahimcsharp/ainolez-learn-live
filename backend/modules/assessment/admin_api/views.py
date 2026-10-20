from rest_framework import serializers

from modules.assessment import services
from modules.assessment.models import Quiz, QuizQuestion
from shared.admin_api import ServiceViewSet

RECORD_FIELDS = ["is_active", "created_at", "updated_at", "deleted_at"]


class QuizAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = [
            "id", "course_id", "title", "description", "is_final", "pass_percentage",
            "max_attempts", *RECORD_FIELDS,
        ]  # fmt: skip
        read_only_fields = RECORD_FIELDS


class OptionSerializer(serializers.Serializer):
    option_text = serializers.CharField(max_length=500)
    is_correct = serializers.BooleanField(default=False)


class QuestionAdminSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, required=False)

    class Meta:
        model = QuizQuestion
        fields = [
            "id", "quiz", "question_text", "question_type", "code_snippet", "explanation",
            "points", "sort_order", "options", *RECORD_FIELDS,
        ]  # fmt: skip
        read_only_fields = ["sort_order", *RECORD_FIELDS]

    def to_representation(self, question):
        data = super().to_representation(question)
        data["options"] = [
            {"id": o.pk, "option_text": o.option_text, "is_correct": o.is_correct}
            for o in question.options.order_by("sort_order")
        ]
        return data


class QuizViewSet(ServiceViewSet):
    model = Quiz
    serializer_class = QuizAdminSerializer
    save = services.save_quiz
    search_fields = ("title",)
    filter_fields = ("course_id",)
    ordering = ("title",)


class QuestionViewSet(ServiceViewSet):
    model = QuizQuestion
    serializer_class = QuestionAdminSerializer
    save = services.save_question
    filter_fields = ("quiz",)
    ordering = ("sort_order", "id")
