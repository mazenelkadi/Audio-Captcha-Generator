from rest_framework.permissions import BasePermission

from .models import Roles


class IsMasterUser(BasePermission):
    """Allow access only to master level users."""

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.role in {
            Roles.MASTER,
            Roles.MASTER_EDITOR,
            Roles.MASTER_VIEWER,
        })
