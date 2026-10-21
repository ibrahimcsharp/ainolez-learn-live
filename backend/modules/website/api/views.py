from django.http import Http404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.website import selectors


class PublicView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]


class MenusView(PublicView):
    """The header links and the footer columns."""

    def get(self, request):
        return Response(selectors.public_menus())


class PageView(PublicView):
    def get(self, request, slug):
        page = selectors.public_page(slug)
        if page is None:
            raise Http404
        return Response({
            "id": page.pk,
            "title": page.title,
            "slug": page.slug,
            "summary": page.summary,
            "content_html": page.content_html or "",  # sanitised when saved
            "updated_at": page.updated_at,
        })  # fmt: skip
