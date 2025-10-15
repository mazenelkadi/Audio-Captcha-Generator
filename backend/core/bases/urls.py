from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BaseViewSet, GlobalAnalyticsViewSet, RecordViewSet

router = DefaultRouter()
router.register(r"bases", BaseViewSet, basename="base")
router.register(r"analytics/global", GlobalAnalyticsViewSet, basename="global-analytics")

record_list = RecordViewSet.as_view({
    "get": "list",
    "post": "create",
})
record_detail = RecordViewSet.as_view({
    "get": "retrieve",
    "put": "update",
    "patch": "partial_update",
    "delete": "destroy",
})

urlpatterns = [
    path("", include(router.urls)),
    path("bases/<int:base_pk>/records/", record_list, name="record-list"),
    path("bases/<int:base_pk>/records/<int:pk>/", record_detail, name="record-detail"),
]
