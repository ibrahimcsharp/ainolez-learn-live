from django.urls import path

from modules.platform_admin.admin_api import views

urlpatterns = [
    path("dashboard/", views.DashboardView.as_view()),
    path("analytics/", views.AnalyticsView.as_view()),
]
