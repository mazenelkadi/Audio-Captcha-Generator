from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RegistrationViewSet, UserViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"auth/register", RegistrationViewSet, basename="register")

urlpatterns = [
    path("", include(router.urls)),
]
