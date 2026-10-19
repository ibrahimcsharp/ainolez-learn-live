from django.urls import path

from modules.content_tools.admin_api import views

urlpatterns = [
    path("md-convert/", views.MarkdownConvertView.as_view()),
]
