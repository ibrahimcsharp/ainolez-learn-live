from rest_framework import serializers
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.assistant import selectors, services


class AssistantView(APIView):
    """Open to visitors and learners. Visitors send a random X-Chat-Session id."""

    permission_classes = [AllowAny]

    @property
    def session_key(self) -> str | None:
        return self.request.headers.get("X-Chat-Session")


class AskInput(serializers.Serializer):
    question = serializers.CharField(max_length=services.MAX_QUESTION)
    conversation_id = serializers.IntegerField(required=False, allow_null=True)
    lesson_id = serializers.IntegerField(required=False, allow_null=True)
    code = serializers.CharField(
        required=False, allow_blank=True, default="", max_length=services.MAX_CODE
    )
    language = serializers.CharField(required=False, allow_blank=True, default="", max_length=20)


class ConfigView(AssistantView):
    def get(self, request):
        return Response(selectors.public_config(services.settings_row()))


class MessagesView(AssistantView):
    throttle_scope = "assistant"

    def post(self, request):
        data = AskInput(data=request.data)
        data.is_valid(raise_exception=True)
        answer = services.ask(request.user, self.session_key, services.Ask(**data.validated_data))
        return Response(
            {"conversation_id": answer.conversation_id, "answer": selectors.message_dict(answer)}
        )


class ConversationView(AssistantView):
    def get(self, request, conversation_id):
        conversation = services.conversation_for(request.user, self.session_key, conversation_id)
        return Response(
            {"id": conversation.pk, "messages": selectors.conversation_messages(conversation)}
        )


class FeedbackView(AssistantView):
    def post(self, request, message_id):
        services.give_feedback(
            request.user, self.session_key, message_id, str(request.data.get("value", ""))
        )
        return Response({"detail": "Thanks for the feedback!"})
