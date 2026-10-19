from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.catalog import selectors as catalog
from modules.certification import selectors as certification
from modules.gamification import selectors as gamification
from modules.learning import selectors, services


class SubmitExerciseSerializer(serializers.Serializer):
    code = serializers.CharField(allow_blank=True, max_length=100_000)
    output = serializers.CharField(allow_blank=True, required=False, default="", max_length=100_000)


class SubmitQuizSerializer(serializers.Serializer):
    # {question_id: [option ids]}
    answers = serializers.DictField(child=serializers.ListField(child=serializers.IntegerField()))


def _progress(progress) -> dict:
    return {
        "progress_percent": progress.progress_percent,
        "course_completed": progress.completed,
        "just_completed": progress.just_completed,
    }


class LearnerWriteView(APIView):
    throttle_scope = "learning"


class LessonVisitView(LearnerWriteView):
    """Called when a logged-in learner opens a lesson. Returns their state for it."""

    def post(self, request, lesson_id):
        services.record_visit(request.user, lesson_id)
        lesson = catalog.visible_lesson(lesson_id)
        exercise_ids, quiz_ids = catalog.lesson_assessment_ids(lesson_id)
        solved = selectors.solved_exercise_ids(request.user, exercise_ids)
        return Response({
            "course": selectors.course_progress(request.user, lesson.course_id),
            "solved_exercise_ids": sorted(solved),
            "quiz_results": selectors.best_quiz_results(request.user, quiz_ids),
        })  # fmt: skip


class CompleteLessonView(LearnerWriteView):
    def post(self, request, lesson_id):
        return Response(_progress(services.complete_lesson(request.user, lesson_id)))


class SubmitExerciseView(LearnerWriteView):
    def post(self, request, exercise_id):
        data = SubmitExerciseSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        correct, message = services.submit_exercise(
            request.user, exercise_id, **data.validated_data
        )
        return Response({"is_correct": correct, "message": message})


class SubmitQuizView(LearnerWriteView):
    def post(self, request, quiz_id):
        data = SubmitQuizSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        attempt, feedback, progress = services.submit_quiz(
            request.user, quiz_id, data.validated_data["answers"]
        )
        return Response({
            "score": attempt.score,
            "total_points": attempt.total_points,
            "percentage": float(attempt.percentage),
            "passed": attempt.passed,
            "questions": feedback,
            **_progress(progress),
        })  # fmt: skip


class CourseProgressView(APIView):
    def get(self, request, course_id):
        progress = selectors.course_progress(request.user, course_id)
        resume = catalog.lesson_links([progress["last_lesson_id"]]).get(progress["last_lesson_id"])
        return Response({**progress, "resume": resume})


class DashboardView(APIView):
    """Everything the learner dashboard shows, in one call."""

    def get(self, request):
        enrollments = selectors.enrollments(request.user)
        courses = catalog.course_summaries(e.course_id for e in enrollments)
        resume = catalog.lesson_links(e.last_lesson_id for e in enrollments)
        return Response({
            "courses": [
                {
                    "course_id": e.course_id,
                    "title": courses[e.course_id]["title"],
                    "slug": courses[e.course_id]["slug"],
                    "status": e.status,
                    "progress_percent": e.progress_percent,
                    "resume": resume.get(e.last_lesson_id),
                }
                for e in enrollments
                if e.course_id in courses
            ],
            "stats": gamification.learner_summary(request.user.pk),
            "certificates": certification.learner_certificates(request.user.pk),
        })  # fmt: skip
