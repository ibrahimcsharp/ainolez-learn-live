from rest_framework.routers import SimpleRouter

from modules.catalog.admin_api import views

router = SimpleRouter()
router.register("categories", views.CategoryViewSet, basename="admin-category")
router.register("courses", views.CourseViewSet, basename="admin-course")
router.register("chapters", views.ChapterViewSet, basename="admin-chapter")
router.register("lessons", views.LessonViewSet, basename="admin-lesson")
router.register("blocks", views.BlockViewSet, basename="admin-block")
router.register("paths", views.PathViewSet, basename="admin-path")
urlpatterns = router.urls
