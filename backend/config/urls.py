from django.conf import settings
from django.conf.urls.static import static
from django.db import connection
from django.http import JsonResponse
from django.urls import include, path

from modules.certification.api.views import CertificateView, share_page
from modules.gamification.api.views import LeaderboardView
from shared.runner import runner


def health(request):
    """Used by deploy checks: confirms the app and the database respond."""
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("api/v1/health/", health),
    path("api/v1/auth/", include("modules.identity.api.urls")),
    # Public website
    path("api/v1/public/", include("modules.catalog.api.urls")),
    path("api/v1/public/certificates/<str:code>/", CertificateView.as_view()),
    path("api/v1/public/leaderboard/", LeaderboardView.as_view()),
    path("api/v1/public/seo/", include("modules.seo.api.urls")),
    path("share/certificates/<str:code>/", share_page),
    path("runner/", runner),
    path("api/v1/community/", include("modules.community.api.urls")),
    path("api/v1/assistant/", include("modules.assistant.api.urls")),
    # Learner portal
    path("api/v1/learner/", include("modules.learning.api.urls")),
    # Admin panel
    path("api/v1/admin/platform/", include("modules.platform_admin.admin_api.urls")),
    path("api/v1/admin/catalog/", include("modules.catalog.admin_api.urls")),
    path("api/v1/admin/assessment/", include("modules.assessment.admin_api.urls")),
    path("api/v1/admin/gamification/", include("modules.gamification.admin_api.views")),
    path("api/v1/admin/certification/", include("modules.certification.admin_api.views")),
    path("api/v1/admin/community/", include("modules.community.admin_api.views")),
    path("api/v1/admin/assistant/", include("modules.assistant.admin_api.views")),
    path("api/v1/admin/seo/", include("modules.seo.admin_api.views")),
    path("api/v1/admin/ai-authoring/", include("modules.ai_authoring.admin_api.views")),
    path("api/v1/admin/media/", include("modules.media.admin_api.urls")),
    path("api/v1/admin/content-tools/", include("modules.content_tools.admin_api.urls")),
]

# Apache serves uploads on the server; Django only does it on your PC.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
