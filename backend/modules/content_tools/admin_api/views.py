from rest_framework.response import Response
from rest_framework.views import APIView

from modules.content_tools import services
from shared.permissions import IsSuperAdmin


class MarkdownConvertView(APIView):
    """Live preview for the Markdown converter and the block editor."""

    permission_classes = [IsSuperAdmin]

    def post(self, request):
        return Response({"html": services.render_markdown(str(request.data.get("markdown", "")))})
