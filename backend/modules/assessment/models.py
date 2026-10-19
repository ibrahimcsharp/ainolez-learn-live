"""Tables from database/schema/0005_assessment.sql."""

from django.db import models

from shared.models import BaseModel

LANGUAGES = ("html", "css", "javascript", "python", "sql")


class Exercise(BaseModel):
    class CheckType(models.TextChoices):
        EXACT = "exact"  # the code equals the expected value
        CONTAINS = "contains"  # the code contains it
        REGEX = "regex"  # the code matches the pattern
        OUTPUT = "output"  # what the code printed equals it

    title = models.CharField(max_length=200, blank=True)
    prompt_md = models.TextField()
    prompt_html = models.TextField()
    language = models.CharField(max_length=20)
    starter_code = models.TextField(blank=True)
    solution_code = models.TextField(blank=True)
    check_type = models.CharField(max_length=10, choices=CheckType, default=CheckType.OUTPUT)
    expected_value = models.TextField()
    hint = models.CharField(max_length=500, blank=True)

    class Meta(BaseModel.Meta):
        managed = False
        db_table = "exercises"


class Quiz(BaseModel):
    course_id = models.BigIntegerField()  # catalog module
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500, blank=True)
    is_final = models.BooleanField(default=False)
    pass_percentage = models.PositiveSmallIntegerField(default=70)
    max_attempts = models.IntegerField(null=True, blank=True)

    class Meta(BaseModel.Meta):
        managed = False
        db_table = "quizzes"
        verbose_name_plural = "quizzes"


class QuizQuestion(BaseModel):
    class Type(models.TextChoices):
        SINGLE = "single"
        MULTIPLE = "multiple"
        TRUE_FALSE = "true_false"

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=Type, default=Type.SINGLE)
    code_snippet = models.TextField(null=True, blank=True)
    explanation = models.CharField(max_length=1000, blank=True)
    points = models.IntegerField(default=1)
    sort_order = models.IntegerField(default=0)

    class Meta(BaseModel.Meta):
        managed = False
        db_table = "quiz_questions"


class QuizOption(models.Model):
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, related_name="options")
    option_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    sort_order = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = "quiz_options"
