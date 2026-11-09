"""Admin -> SEO & GEO Center: overview, site defaults, per-page settings, AI crawlers,
GEO files, the SEO report, rebuild and the change log (with undo)."""

from django.urls import path
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.routers import SimpleRouter
from rest_framework.views import APIView

from modules.seo import content, geo, prerender, resolver, selectors, services
from modules.seo.models import AiBot, SeoChangeLog, SeoPage, SeoSettings
from shared.admin_api import ServiceViewSet
from shared.exceptions import ServiceError
from shared.permissions import IsSuperAdmin

RECORD_FIELDS = ["is_active", "created_at", "updated_at", "deleted_at"]
SEO_FIELDS = [
    "meta_title", "meta_description", "keywords", "canonical_url", "robots",
    "og_title", "og_description", "og_image_url", "og_type", "twitter_card",
    "structured_data", "in_sitemap", "sitemap_priority", "sitemap_changefreq",
]  # fmt: skip


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeoSettings
        read_only_fields = [
            "last_build_at", "last_build_pages", "updated_at",
            "indexnow_key", "indexnow_last_at", "indexnow_last_result",
        ]  # fmt: skip
        fields = [*services.SETTING_FIELDS, *read_only_fields]


class PageSerializer(serializers.ModelSerializer):
    path = serializers.CharField(write_only=True, required=False, allow_blank=True)
    url = serializers.SerializerMethodField()

    class Meta:
        model = SeoPage
        fields = ["id", "path", "url", "entity_type", "entity_id", *SEO_FIELDS, *RECORD_FIELDS]
        read_only_fields = ["entity_type", "entity_id", *RECORD_FIELDS]

    def get_url(self, page) -> str:
        return selectors.page_urls([page]).get(page.pk, "")


class SettingsView(APIView):
    permission_classes = [IsSuperAdmin]

    def get(self, request):
        return Response(SettingsSerializer(resolver.settings_row()).data)

    def patch(self, request):
        serializer = SettingsSerializer(resolver.settings_row(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        site = services.update_settings(serializer.validated_data, request.user)
        return Response(SettingsSerializer(site).data)


class PageViewSet(ServiceViewSet):
    model = SeoPage
    serializer_class = PageSerializer
    save = services.save_page
    search_fields = ("path", "meta_title", "meta_description")
    filter_fields = ("entity_type",)
    ordering = ("path", "entity_type", "entity_id")


class LookupView(APIView):
    """GET ?path= : the page's settings row (or null), its automatic values and
    the final result, for the SEO form and its Google / social previews."""

    permission_classes = [IsSuperAdmin]

    def get(self, request):
        site = resolver.settings_row()
        wanted = resolver.normalize(request.query_params.get("path", "/"))
        entity = content.entity_for_path(wanted)
        rows = SeoPage.objects.all()
        row = (
            rows.filter(entity_type=entity[0], entity_id=entity[1]).first()
            if entity
            else rows.filter(path=wanted).first()
        )
        final = resolver.resolve(wanted, site)
        return Response({
            "path": wanted,
            "entity": entity and {"type": entity[0], "id": entity[1]},
            "page": PageSerializer(row).data if row else None,
            "automatic": _summary(resolver.automatic(wanted, site)),
            "result": {**_summary(final), "status": final.status, "json_ld": final.json_ld},
        })  # fmt: skip


class ReportView(APIView):
    permission_classes = [IsSuperAdmin]

    def get(self, request):
        return Response(selectors.seo_report())


class BuildView(APIView):
    """POST: write the prerendered pages, sitemap.xml and robots.txt now."""

    permission_classes = [IsSuperAdmin]

    def post(self, request):
        return Response({"pages": prerender.build()})


class BotSerializer(serializers.ModelSerializer):
    class Meta:
        model = AiBot
        fields = ["id", *services.BOT_FIELDS, *RECORD_FIELDS]
        read_only_fields = RECORD_FIELDS


class BotViewSet(ServiceViewSet):
    model = AiBot
    serializer_class = BotSerializer
    save = services.save_bot
    search_fields = ("user_agent", "owner")
    filter_fields = ("purpose",)
    ordering = ("sort_order", "user_agent")


class OverviewView(APIView):
    """GET ?days=30 : scores, the "fix next" list, traffic and recent changes."""

    permission_classes = [IsSuperAdmin]

    def get(self, request):
        days = min(max(int(request.query_params.get("days") or 30), 7), 365)
        return Response(selectors.overview(days))


class GeoFileView(APIView):
    """GET ?file=llms|llms-full|robots|markdown[&path=/python] : the text the next build
    writes, made now (a preview, nothing is written)."""

    permission_classes = [IsSuperAdmin]

    def get(self, request):
        site = resolver.settings_row()
        wanted = request.query_params.get("file", "llms")
        if wanted == "robots":
            return Response({"text": prerender.robots_txt(site)})
        if wanted == "markdown":
            meta = resolver.resolve(request.query_params.get("path", "/"), site)
            text = geo.markdown_for(meta.path, meta.entity) if meta.status == 200 else None
            if text is None:
                raise ServiceError("This page has no Markdown copy.", "no_markdown")
            return Response({"text": text})
        pages = [resolver.resolve(path, site) for path in prerender.public_paths()]
        if wanted == "llms-full":
            return Response({"text": geo.llms_full_txt(site, pages, prerender.all_markdown(pages))})
        copies = {meta.path for meta in pages if meta.has_markdown}
        return Response({"text": geo.llms_txt(site, pages, copies)})


class ChangeLogView(APIView):
    permission_classes = [IsSuperAdmin]

    def get(self, request):
        params = request.query_params
        return Response(selectors.change_log(params.get("area", ""), params.get("actor", "")))


class UndoView(APIView):
    permission_classes = [IsSuperAdmin]

    def post(self, request, pk: int):
        entry = SeoChangeLog.objects.filter(pk=pk).first()
        if entry is None:
            raise ServiceError("This change is not in the log.", "not_found")
        services.undo(entry, request.user)
        return Response(selectors.change_rows([entry])[0])


def _summary(meta: resolver.PageMeta) -> dict:
    return {
        "title": meta.title,
        "description": meta.description,
        "keywords": meta.keywords,
        "robots": meta.robots,
        "canonical": meta.canonical,
        "image": meta.image,
        "og_type": meta.og_type,
        "og_title": meta.og_title,
        "og_description": meta.og_description,
        "twitter_card": meta.twitter_card,
    }


router = SimpleRouter()
router.register("pages", PageViewSet, basename="admin-seo-page")
router.register("bots", BotViewSet, basename="admin-seo-bot")
urlpatterns = [
    path("overview/", OverviewView.as_view()),
    path("geo-file/", GeoFileView.as_view()),
    path("changes/", ChangeLogView.as_view()),
    path("changes/<int:pk>/undo/", UndoView.as_view()),
    path("settings/", SettingsView.as_view()),
    path("lookup/", LookupView.as_view()),
    path("report/", ReportView.as_view()),
    path("build/", BuildView.as_view()),
    *router.urls,
]
