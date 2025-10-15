from collections import Counter

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import filters, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response

from core.accounts.models import Roles

from .models import Base, Record, FieldTypes
from .permissions import BaseObjectPermission, RecordPermission
from .serializers import (
    AnalyticsSerializer,
    BaseSerializer,
    FieldSerializer,
    RecordSerializer,
)


class BaseViewSet(viewsets.ModelViewSet):
    queryset = Base.objects.all().prefetch_related("fields", "memberships__user")
    serializer_class = BaseSerializer
    permission_classes = [BaseObjectPermission]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "created_at", "updated_at"]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if not user.is_authenticated:
            return qs.none()
        if user.role in {Roles.MASTER, Roles.MASTER_EDITOR, Roles.MASTER_VIEWER}:
            return qs
        return qs.filter(memberships__user=user).distinct()

    def perform_create(self, serializer):
        user = self.request.user
        if not user.can_create_bases:
            raise PermissionDenied("You do not have permission to create bases.")
        serializer.save(created_by=user)

    def perform_destroy(self, instance):
        user = self.request.user
        if not user.can_delete_bases and instance.created_by_id != user.id:
            raise PermissionDenied("You cannot delete this base.")
        super().perform_destroy(instance)

    @action(detail=True, methods=["get"], url_path="fields")
    def list_fields(self, request, pk=None):
        base = self.get_object()
        serializer = FieldSerializer(base.fields.all(), many=True)
        return Response(serializer.data)

    @method_decorator(cache_page(60))
    @action(detail=True, methods=["get"], url_path="analytics")
    def analytics(self, request, pk=None):
        base = self.get_object()
        record_count = base.records.count()
        aggregations = {}
        records = list(base.records.all().only("data"))
        for field in base.fields.all():
            if field.field_type in {FieldTypes.BOOLEAN, FieldTypes.SINGLE_SELECT, FieldTypes.MULTI_SELECT}:
                counter = Counter()
                for record in records:
                    value = record.data.get(field.name)
                    if value is None:
                        continue
                    if isinstance(value, list):
                        counter.update(value)
                    else:
                        counter.update([value])
                aggregations[field.name] = dict(counter)
        serializer = AnalyticsSerializer(
            {"base_id": base.id, "record_count": record_count, "aggregations": aggregations}
        )
        return Response(serializer.data)


class RecordViewSet(viewsets.ModelViewSet):
    serializer_class = RecordSerializer
    permission_classes = [RecordPermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ["data"]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        base = Base.objects.get(pk=self.kwargs.get("base_pk"))
        context.update({"base": base})
        return context

    def get_queryset(self):
        base_id = self.kwargs.get("base_pk")
        queryset = Record.objects.filter(base_id=base_id).select_related("base")
        user = self.request.user
        if user.role in {Roles.MASTER, Roles.MASTER_EDITOR}:
            return queryset
        if user.role == Roles.MASTER_VIEWER:
            return queryset
        return queryset.filter(base__memberships__user=user).distinct()

    def perform_create(self, serializer):
        base = Base.objects.get(pk=self.kwargs.get("base_pk"))
        user = self.request.user
        if user.role == Roles.MASTER_VIEWER:
            raise PermissionDenied("Viewers cannot create records.")
        if user.role not in {Roles.MASTER, Roles.MASTER_EDITOR}:
            membership = base.memberships.filter(user=user).first()
            if not membership or membership.role != membership.MembershipRole.ADMIN:
                raise PermissionDenied("You do not have edit access to this base.")
        serializer.save(base=base, created_by=user)


class GlobalAnalyticsViewSet(viewsets.ViewSet):
    permission_classes = [RecordPermission]

    @method_decorator(cache_page(60))
    def list(self, request):
        user = request.user
        bases = Base.objects.all()
        if user.role not in {Roles.MASTER, Roles.MASTER_EDITOR, Roles.MASTER_VIEWER}:
            bases = bases.filter(memberships__user=user)
        payload = []
        for base in bases.distinct():
            record_count = base.records.count()
            payload.append({"base_id": base.id, "record_count": record_count})
        serializer = AnalyticsSerializer(payload, many=True)
        return Response(serializer.data)
