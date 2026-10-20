"""Tables from database/schema/0004_catalog.sql."""

from django.db import models

from shared.models import BaseModel


class Status(models.TextChoices):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class Level(models.TextChoices):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class Category(BaseModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    description = models.CharField(max_length=500, blank=True)
    icon = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=7, default="#04AA6D")
    sort_order = models.IntegerField(default=0)

    class Meta(BaseModel.Meta):
        managed = False
        db_table = "categories"
        verbose_name_plural = "categories"


class Course(BaseModel):
    class Language(models.TextChoices):
        HTML = "html"
        CSS = "css"
        JAVASCRIPT = "javascript"
        PYTHON = "python"
        SQL = "sql"
        AI = "ai"
        OTHER = "other"

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="courses")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100)
    short_description = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True, null=True)
    level = models.CharField(max_length=20, choices=Level, default=Level.BEGINNER)
    language_key = models.CharField(max_length=20, choices=Language, default=Language.OTHER)
    thumbnail_media_id = models.BigIntegerField(null=True, blank=True)  # media module
    intro_video_url = models.CharField(max_length=500, blank=True)
    estimated_minutes = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=Status, default=Status.DRAFT)
    ai_generated = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta(BaseModel.Meta):
        managed = False
        db_table = "courses"


class Chapter(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="chapters")
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500, blank=True)
    sort_order = models.IntegerField(default=0)

    class Meta(BaseModel.Meta):
        managed = False
        db_table = "chapters"


class Lesson(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100)
    summary = models.CharField(max_length=500, blank=True)
    estimated_minutes = models.IntegerField(default=5)
    status = models.CharField(max_length=20, choices=Status, default=Status.DRAFT)
    ai_generated = models.BooleanField(default=False)
    sort_order = models.IntegerField(default=0)
    source_md = models.TextField(null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta(BaseModel.Meta):
        managed = False
        db_table = "lessons"


class CodeExample(BaseModel):
    RUN_MODES = {"html": "iframe", "css": "iframe", "javascript": "iframe",
                 "python": "pyodide", "sql": "sqljs"}  # fmt: skip

    title = models.CharField(max_length=200, blank=True)
    language = models.CharField(max_length=20)
    starter_code = models.TextField()
    run_mode = models.CharField(max_length=10)

    class Meta(BaseModel.Meta):
        managed = False
        db_table = "code_examples"


class LessonBlock(BaseModel):
    class Type(models.TextChoices):
        MARKDOWN = "markdown"
        EXAMPLE = "example"
        VIDEO = "video"
        CALLOUT = "callout"
        IMAGE = "image"
        EMBED = "embed"
        EXERCISE = "exercise"
        QUIZ = "quiz"

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="blocks")
    type = models.CharField(max_length=20, choices=Type)
    sort_order = models.IntegerField(default=0)
    content_md = models.TextField(null=True, blank=True)
    content_html = models.TextField(null=True, blank=True)
    data = models.JSONField(null=True, blank=True)
    code_example = models.ForeignKey(
        CodeExample, on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )
    media_id = models.BigIntegerField(null=True, blank=True)  # media module
    exercise_id = models.BigIntegerField(null=True, blank=True)  # assessment module
    quiz_id = models.BigIntegerField(null=True, blank=True)  # assessment module

    class Meta(BaseModel.Meta):
        managed = False
        db_table = "lesson_blocks"


class LearningPath(BaseModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100)
    description = models.CharField(max_length=1000, blank=True)
    level = models.CharField(max_length=20, choices=Level, default=Level.BEGINNER)
    courses = models.ManyToManyField(Course, through="LearningPathCourse", related_name="+")

    class Meta(BaseModel.Meta):
        managed = False
        db_table = "learning_paths"


class LearningPathCourse(models.Model):
    path = models.ForeignKey(LearningPath, on_delete=models.CASCADE, related_name="path_courses")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="+")
    sort_order = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = "learning_path_courses"
