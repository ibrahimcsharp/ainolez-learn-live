from django.urls import path

from modules.community.api import views

urlpatterns = [
    path("spaces/", views.SpacesView.as_view()),
    path("posts/", views.PostsView.as_view()),
    path("posts/<int:post_id>/", views.PostDetailView.as_view()),
    path("posts/<int:post_id>/replies/", views.RepliesView.as_view()),
    path("replies/<int:reply_id>/accept/", views.AcceptReplyView.as_view()),
    path("like/", views.LikeView.as_view()),
    path("report/", views.ReportView.as_view()),
    path("lessons/<int:lesson_id>/comments/", views.LessonCommentsView.as_view()),
]
