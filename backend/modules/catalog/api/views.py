from django.http import Http404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.assessment import selectors as assessment
from modules.catalog import selectors
from modules.catalog.api import serializers as s
from modules.media import selectors as media


class PublicView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]


def _thumbnails(courses) -> dict:
    return {"thumbnails": media.urls_for(course.thumbnail_media_id for course in courses)}


def _assessments(blocks) -> dict:
    return {
        "exercises": assessment.exercises_for_learner(b.exercise_id for b in blocks),
        "quizzes": assessment.quizzes_for_learner(b.quiz_id for b in blocks),
    }


class CategoriesView(PublicView):
    def get(self, request):
        return Response(s.CategorySerializer(selectors.public_categories(), many=True).data)


class CoursesView(PublicView):
    def get(self, request):
        courses = list(selectors.public_courses(request.query_params.get("category", "")))
        return Response(
            s.CourseCardSerializer(courses, many=True, context=_thumbnails(courses)).data
        )


class CourseDetailView(PublicView):
    def get(self, request, slug):
        found = selectors.public_course(slug)
        if found is None:
            raise Http404
        course, chapters = found
        data = s.CourseDetailSerializer(course, context=_thumbnails([course])).data
        data["chapters"] = s.ChapterOutlineSerializer(chapters, many=True).data
        return Response(data)


class LessonView(PublicView):
    def get(self, request, course_slug, lesson_slug):
        page = selectors.public_lesson(course_slug, lesson_slug)
        if page is None:
            raise Http404
        link = s.LessonLinkSerializer
        blocks = s.BlockSerializer(page.blocks, many=True, context=_assessments(page.blocks))
        return Response({
            "course": {"title": page.lesson.course.title, "slug": page.lesson.course.slug},
            "lesson": s.LessonSerializer(page.lesson).data,
            "blocks": blocks.data,
            "chapters": s.ChapterOutlineSerializer(page.chapters, many=True).data,
            "previous": link(page.previous).data if page.previous else None,
            "next": link(page.next).data if page.next else None,
        })  # fmt: skip


class SearchView(PublicView):
    throttle_scope = "search"

    def get(self, request):
        lessons = selectors.search_lessons(request.query_params.get("q", ""))
        return Response([
            {
                "title": lesson.title,
                "slug": lesson.slug,
                "summary": lesson.summary,
                "course": {"title": lesson.course.title, "slug": lesson.course.slug},
            }
            for lesson in lessons
        ])  # fmt: skip


class PathsView(PublicView):
    def get(self, request):
        paths = selectors.public_paths()
        all_courses = [course for _, courses in paths for course in courses]
        context = _thumbnails(all_courses)
        return Response([
            {
                "title": path.title,
                "slug": path.slug,
                "description": path.description,
                "level": path.level,
                "courses": s.CourseCardSerializer(courses, many=True, context=context).data,
            }
            for path, courses in paths
        ])  # fmt: skip
