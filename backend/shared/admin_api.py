"""
Base viewset for every admin resource. Gives each one the same endpoints:

    GET    /                 list   (?q= ?active=1|0 ?trash=1 ?<filter>=)
    POST   /                 create
    GET    /{id}/            detail
    PATCH  /{id}/            edit
    POST   /{id}/activate/   POST /{id}/deactivate/
    POST   /{id}/soft-delete/  POST /{id}/restore/
    GET    /{id}/hard/       what a hard delete would remove
    DELETE /{id}/hard/       hard delete, body {"confirm": "<item name>"}
    POST   /bulk/            {"action": "activate|deactivate|soft-delete|restore", "ids": [..]}
    POST   /reorder/         {"ids": [..]} (resources with sort_order)
"""

from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from shared import audit, records
from shared.exceptions import ServiceError
from shared.permissions import IsSuperAdmin


class AdminPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 500


class AdminResourceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperAdmin]
    pagination_class = AdminPagination
    http_method_names = ["get", "post", "patch", "delete"]

    model = None
    search_fields: tuple[str, ...] = ()
    filter_fields: tuple[str, ...] = ()
    ordering: tuple[str, ...] = ("-id",)

    def get_queryset(self):
        queryset = self.model.all_objects.all()
        if self.action != "list":
            return queryset  # detail actions also reach items in the Trash
        params = self.request.query_params
        queryset = queryset.filter(deleted_at__isnull=params.get("trash") != "1")
        if params.get("active") in ("0", "1"):
            queryset = queryset.filter(is_active=params["active"] == "1")
        for field in self.filter_fields:
            if params.get(field):
                queryset = queryset.filter(**{field: params[field]})
        if params.get("q") and self.search_fields:
            match = Q()
            for field in self.search_fields:
                match |= Q(**{f"{field}__icontains": params["q"]})
            queryset = queryset.filter(match)
        return queryset.order_by(*self.ordering)

    # Create and edit. Override these to call a module service instead.
    def perform_create(self, serializer):
        user = self.request.user
        obj = serializer.save(created_by=user, updated_by=user)
        audit.record(f"{obj._meta.model_name}.created", actor=user, entity=obj)

    def perform_update(self, serializer):
        obj = serializer.save(updated_by=self.request.user)
        audit.record(f"{obj._meta.model_name}.updated", actor=self.request.user, entity=obj)

    def record_changed(self, obj) -> None:
        """Called after activate, deactivate, soft delete or restore. Override to react."""

    def destroy(self, request, *args, **kwargs):
        return Response(
            {"detail": "Use soft-delete, then hard delete from the Trash."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    # Record controls
    @action(detail=True, methods=["post"])
    def activate(self, request, pk=None):
        obj = self.get_object()
        records.set_active(obj, True, request.user)
        self.record_changed(obj)
        return self._detail()

    @action(detail=True, methods=["post"])
    def deactivate(self, request, pk=None):
        obj = self.get_object()
        records.set_active(obj, False, request.user)
        self.record_changed(obj)
        return self._detail()

    @action(detail=True, methods=["post"], url_path="soft-delete")
    def soft_delete(self, request, pk=None):
        obj = self.get_object()
        records.soft_delete(obj, request.user)
        self.record_changed(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"])
    def restore(self, request, pk=None):
        obj = self.get_object()
        records.restore(obj, request.user)
        self.record_changed(obj)
        return self._detail()

    @action(detail=True, methods=["get", "delete"])
    def hard(self, request, pk=None):
        obj = self.get_object()
        if request.method == "GET":
            return Response(records.hard_delete_preview(obj))
        records.hard_delete(obj, str(request.data.get("confirm", "")), request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["post"])
    def bulk(self, request):
        handlers = {
            "activate": lambda obj: records.set_active(obj, True, request.user),
            "deactivate": lambda obj: records.set_active(obj, False, request.user),
            "soft-delete": lambda obj: records.soft_delete(obj, request.user),
            "restore": lambda obj: records.restore(obj, request.user),
        }
        handler = handlers.get(request.data.get("action"))
        if handler is None:
            raise ServiceError("Unknown bulk action.", "bad_action")
        items = self.model.all_objects.filter(pk__in=request.data.get("ids", []))
        for obj in items:
            handler(obj)
            self.record_changed(obj)
        return Response({"done": len(items)})

    @action(detail=False, methods=["post"])
    def reorder(self, request):
        records.reorder(self.model, request.data.get("ids", []), request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _detail(self):
        return Response(self.get_serializer(self.get_object()).data)


class ServiceViewSet(AdminResourceViewSet):
    """Create and edit go through a module service ``save(obj_or_None, data, by)``,
    which owns the business rules and the audit entry."""

    save = None

    def perform_create(self, serializer):
        data = dict(serializer.validated_data)
        serializer.instance = type(self).save(None, data, self.request.user)

    def perform_update(self, serializer):
        type(self).save(serializer.instance, dict(serializer.validated_data), self.request.user)
