from django.urls import path

from modules.website.api import views

urlpatterns = [
    path("menus/", views.MenusView.as_view()),
    path("pages/<slug:slug>/", views.PageView.as_view()),
]
