from rest_framework import serializers
from rest_framework.routers import SimpleRouter

from modules.gamification import services
from modules.gamification.models import Badge, PointsRule
from shared.admin_api import ServiceViewSet

RECORD_FIELDS = ["is_active", "created_at", "updated_at", "deleted_at"]


class PointsRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointsRule
        fields = ["id", "event_key", "points", "daily_cap", "description", *RECORD_FIELDS]
        read_only_fields = RECORD_FIELDS


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ["id", "name", "slug", "description", "icon", "rule", *RECORD_FIELDS]
        read_only_fields = RECORD_FIELDS
        extra_kwargs = {"slug": {"required": False, "allow_blank": True}}


class PointsRuleViewSet(ServiceViewSet):
    model = PointsRule
    serializer_class = PointsRuleSerializer
    save = services.save_rule
    ordering = ("event_key",)


class BadgeViewSet(ServiceViewSet):
    model = Badge
    serializer_class = BadgeSerializer
    save = services.save_badge
    search_fields = ("name",)
    ordering = ("name",)


router = SimpleRouter()
router.register("points-rules", PointsRuleViewSet, basename="admin-points-rule")
router.register("badges", BadgeViewSet, basename="admin-badge")
urlpatterns = router.urls
