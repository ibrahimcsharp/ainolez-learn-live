from django.urls import path

from modules.learning.api import views

urlpatterns = [
    path("lessons/<int:lesson_id>/visit/", views.LessonVisitView.as_view()),
    path("lessons/<int:lesson_id>/complete/", views.CompleteLessonView.as_view()),
    path("exercises/<int:exercise_id>/submit/", views.SubmitExerciseView.as_view()),
    path("quizzes/<int:quiz_id>/attempts/", views.SubmitQuizView.as_view()),
    path("courses/<int:course_id>/progress/", views.CourseProgressView.as_view()),
    path("dashboard/", views.DashboardView.as_view()),
]
