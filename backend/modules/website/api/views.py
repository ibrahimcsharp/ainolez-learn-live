from django.conf import settings
from django.http import Http404, HttpResponse
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.website import code_page, selectors
from modules.website.models import SitePage


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
            "kind": page.kind,
            # a code page shows its own document (page_frame) in an iframe
            "content_html": page.content_html or "" if page.kind == SitePage.Kind.MARKDOWN else "",
            "frame_path": frame_path(page) if page.kind == SitePage.Kind.CODE else None,
            "updated_at": page.updated_at,
        })  # fmt: skip


def frame_path(page: SitePage) -> str:
    """Where page_frame serves it; the version makes a saved change show at once."""
    return f"/api/v1/public/site/pages/{page.slug}/frame/?v={int(page.updated_at.timestamp())}"


# The frame's scripts get an opaque origin even when the URL is opened directly.
FRAME_SANDBOX = (
    "sandbox allow-scripts allow-forms allow-modals allow-popups "
    "allow-popups-to-escape-sandbox allow-downloads"
)


def page_frame(request, slug):
    """The document of a custom code page (see code_page.py), shown in an iframe."""
    page = selectors.public_page(slug)
    if page is None or page.kind != SitePage.Kind.CODE:
        raise Http404
    code = (page.code_html or "", page.code_css or "", page.code_js or "")
    html = code_page.document(page.title, *code)
    response = HttpResponse(html)
    response["Content-Security-Policy"] = (
        f"{FRAME_SANDBOX}; frame-ancestors 'self' {settings.FRONTEND_URL}"
    )
    response["X-Robots-Tag"] = "noindex"  # the page itself (/<slug>) is what search shows
    response["Cache-Control"] = "public, max-age=300"
    return response
