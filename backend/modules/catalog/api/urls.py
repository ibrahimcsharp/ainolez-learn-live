from django.urls import path

from modules.catalog.api import views

urlpatterns = [
    path("categories/", views.CategoriesView.as_view()),
    path("courses/", views.CoursesView.as_view()),
    path("courses/<slug:slug>/", views.CourseDetailView.as_view()),
    path("courses/<slug:course_slug>/lessons/<slug:lesson_slug>/", views.LessonView.as_view()),
    path("search/", views.SearchView.as_view()),
    path("paths/", views.PathsView.as_view()),
]
