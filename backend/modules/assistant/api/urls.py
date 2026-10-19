from django.urls import path

from modules.assistant.api import views

urlpatterns = [
    path("config/", views.ConfigView.as_view()),
    path("messages/", views.MessagesView.as_view()),
    path("messages/<int:message_id>/feedback/", views.FeedbackView.as_view()),
    path("conversations/<int:conversation_id>/", views.ConversationView.as_view()),
]
