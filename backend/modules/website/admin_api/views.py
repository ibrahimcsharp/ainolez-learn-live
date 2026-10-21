"""Admin -> Pages and Menus."""

from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.routers import SimpleRouter

from modules.website import selectors, services
from modules.website.events import MenuChanged, PageChanged
from modules.website.models import Menu, MenuItem, SitePage
from shared.admin_api import ServiceViewSet
from shared.events import publish

RECORD_FIELDS = ["is_active", "created_at", "updated_at", "deleted_at"]


class PageSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(required=False, allow_blank=True, max_length=100)

    class Meta:
        model = SitePage
        fields = ["id", "title", "slug", "summary", "content_md", "content_html", *RECORD_FIELDS]
        read_only_fields = ["content_html", *RECORD_FIELDS]


class MenuSerializer(serializers.ModelSerializer):
    item_count = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = [
            "id", "name", "location", "show_as", "sort_order", "item_count", *RECORD_FIELDS,
        ]  # fmt: skip
        read_only_fields = ["sort_order", *RECORD_FIELDS]

    def get_item_count(self, menu) -> int:
        return menu.items.count()


class MenuItemSerializer(serializers.ModelSerializer):
    target = serializers.SerializerMethodField()

    class Meta:
        model = MenuItem
        fields = [
            "id", "menu", "parent", "label", "link_type", "page", "course_id", "url",
            "open_in_new_tab", "sort_order", "target", *RECORD_FIELDS,
        ]  # fmt: skip
        read_only_fields = ["sort_order", *RECORD_FIELDS]

    def get_target(self, item) -> str:
        return selectors.item_targets([item])[item.pk]


class PageViewSet(ServiceViewSet):
    model = SitePage
    serializer_class = PageSerializer
    save = services.save_page
    search_fields = ("title", "slug")
    ordering = ("title",)

    def record_changed(self, page):
        publish(PageChanged(page.pk))

    @action(detail=True, methods=["post"])
    def restore(self, request, pk=None):
        page = self.get_object()
        services.restore_page(page, request.user)
        self.record_changed(page)
        return self._detail()


class MenuViewSet(ServiceViewSet):
    model = Menu
    serializer_class = MenuSerializer
    save = services.save_menu
    search_fields = ("name",)
    filter_fields = ("location",)
    ordering = ("location", "sort_order", "id")

    def record_changed(self, menu):
        publish(MenuChanged(menu.pk))

    @action(detail=False, methods=["post"])
    def reorder(self, request):
        response = super().reorder(request)
        publish(MenuChanged(0))
        return response

    @action(detail=False, methods=["get", "post"], url_path="header-bar")
    def header_bar(self, request):
        """GET: what the header bar shows, in order. POST {"entries": [...]}: reorder it."""
        if request.method == "POST":
            services.save_header_order(request.data.get("entries", []), request.user)
        return Response([
            {
                "kind": entry["kind"],
                "id": entry["id"],
                "label": entry["link"]["label"],
                "url": entry["link"]["url"],
                "sub_links": len(entry["link"].get("children", [])),
            }
            for entry in selectors.header_bar()
        ])  # fmt: skip


class MenuItemViewSet(ServiceViewSet):
    model = MenuItem
    serializer_class = MenuItemSerializer
    save = services.save_menu_item
    search_fields = ("label", "url")
    filter_fields = ("menu", "parent", "link_type")
    ordering = ("sort_order", "id")

    def get_queryset(self):
        return super().get_queryset().select_related("page")

    def record_changed(self, item):
        publish(MenuChanged(item.menu_id))

    @action(detail=False, methods=["post"])
    def reorder(self, request):
        response = super().reorder(request)
        publish(MenuChanged(0))
        return response


router = SimpleRouter()
router.register("pages", PageViewSet, basename="admin-site-page")
router.register("menus", MenuViewSet, basename="admin-menu")
router.register("menu-items", MenuItemViewSet, basename="admin-menu-item")
urlpatterns = router.urls
