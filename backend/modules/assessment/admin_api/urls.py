from rest_framework.routers import SimpleRouter

from modules.assessment.admin_api import views

router = SimpleRouter()
router.register("quizzes", views.QuizViewSet, basename="admin-quiz")
router.register("questions", views.QuestionViewSet, basename="admin-question")
urlpatterns = router.urls
