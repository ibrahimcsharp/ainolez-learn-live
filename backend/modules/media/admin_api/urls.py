from rest_framework.routers import SimpleRouter

from modules.media.admin_api import views

router = SimpleRouter()
router.register("files", views.MediaFileViewSet, basename="media-file")
urlpatterns = router.urls
