"""Admin -> SEO: site defaults, per-page settings, the SEO report and rebuild."""

from django.urls import path
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.routers import SimpleRouter
from rest_framework.views import APIView

from modules.seo import content, prerender, resolver, selectors, services
from modules.seo.models import SeoPage, SeoSettings
from shared.admin_api import ServiceViewSet
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
        fields = [*services.SETTING_FIELDS, "last_build_at", "last_build_pages", "updated_at"]
        read_only_fields = ["last_build_at", "last_build_pages", "updated_at"]


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
urlpatterns = [
    path("settings/", SettingsView.as_view()),
    path("lookup/", LookupView.as_view()),
    path("report/", ReportView.as_view()),
    path("build/", BuildView.as_view()),
    *router.urls,
]
