from django.http import Http404
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.community import selectors, services


class CommunityView(APIView):
    """Anyone can read; writing needs an account. Writes are rate limited."""

    permission_classes = [IsAuthenticatedOrReadOnly]
    throttle_scope = "community"

    def get_throttles(self):
        return super().get_throttles() if self.request.method == "POST" else []

    def validated(self, serializer_class):
        serializer = serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data


class PostInput(serializers.Serializer):
    space = serializers.IntegerField()
    title = serializers.CharField(max_length=200)
    body_md = serializers.CharField()


class BodyInput(serializers.Serializer):
    body_md = serializers.CharField()


class TargetInput(serializers.Serializer):
    target_type = serializers.ChoiceField(choices=["post", "reply", "comment"])
    target_id = serializers.IntegerField()
    reason = serializers.CharField(required=False, allow_blank=True, max_length=500)


def _created(item) -> Response:
    message = "Posted." if item.status == "approved" else "Thanks! A moderator will check it soon."
    return Response(
        {"id": item.pk, "status": item.status, "detail": message}, status.HTTP_201_CREATED
    )


class SpacesView(CommunityView):
    def get(self, request):
        return Response(selectors.spaces())


class PostsView(CommunityView):
    def get(self, request):
        params = request.query_params
        page = int(params["page"]) if params.get("page", "").isdigit() else 1
        return Response(selectors.posts(params.get("space", ""), params.get("q", "").strip(), page))

    def post(self, request):
        data = self.validated(PostInput)
        return _created(
            services.create_post(request.user, data["space"], data["title"], data["body_md"])
        )


class PostDetailView(CommunityView):
    def get(self, request, post_id):
        post = selectors.post_detail(post_id, request.user)
        if post is None:
            raise Http404
        return Response(post)


class RepliesView(CommunityView):
    def post(self, request, post_id):
        return _created(
            services.create_reply(request.user, post_id, self.validated(BodyInput)["body_md"])
        )


class AcceptReplyView(CommunityView):
    def post(self, request, reply_id):
        services.accept_reply(request.user, reply_id)
        return Response({"detail": "Marked as the helpful answer."})


class LikeView(CommunityView):
    def post(self, request):
        data = self.validated(TargetInput)
        return Response(
            {"liked": services.toggle_like(request.user, data["target_type"], data["target_id"])}
        )


class ReportView(CommunityView):
    def post(self, request):
        data = self.validated(TargetInput)
        services.report(
            request.user, data["target_type"], data["target_id"], data.get("reason", "")
        )
        return Response({"detail": "Thanks, a moderator will take a look."})


class LessonCommentsView(CommunityView):
    def get(self, request, lesson_id):
        return Response(selectors.lesson_comments(lesson_id, request.user))

    def post(self, request, lesson_id):
        comment = services.create_comment(
            request.user, lesson_id, self.validated(BodyInput)["body_md"]
        )
        return _created(comment)
