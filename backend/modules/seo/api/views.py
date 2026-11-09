from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.seo import resolver, services


class PageSeoView(APIView):
    """GET ?path=/python/lists : the title, meta tags and JSON-LD of that page.
    The website calls it on every page view, which also counts the view. On the first
    page of a visit it also sends ref (document.referrer) and utm (utm_source), so
    visits from search engines, AI engines and social sites are counted."""

    permission_classes = [AllowAny]
    authentication_classes = []
    throttle_scope = "page_views"

    def get(self, request):
        site = resolver.settings_row()
        meta = resolver.resolve(request.query_params.get("path", "/"), site)
        if meta.status == 200 and not resolver.is_private(meta.path):
            services.record_view(meta.path)
            params = request.query_params
            if params.get("ref") or params.get("utm"):
                services.record_referral(meta.path, params.get("ref", ""), params.get("utm", ""))
        return Response({
            "status": meta.status,
            "title": meta.title,
            "tags": resolver.head_tags(meta, site),
            "json_ld": meta.json_ld,
        })  # fmt: skip
