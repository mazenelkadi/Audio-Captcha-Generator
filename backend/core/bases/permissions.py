from rest_framework.permissions import BasePermission, SAFE_METHODS

from core.accounts.models import Roles


class BaseObjectPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user.is_authenticated:
            return False
        if user.role in {Roles.MASTER, Roles.MASTER_EDITOR}:
            return True
        if request.method in SAFE_METHODS and user.role == Roles.MASTER_VIEWER:
            return True
        if hasattr(obj, "created_by") and obj.created_by_id == user.id:
            return True
        memberships = obj.memberships.filter(user=user)
        if memberships.exists():
            membership = memberships.first()
            if request.method in SAFE_METHODS:
                return True
            return membership.role == obj.memberships.model.MembershipRole.ADMIN
        return False


class RecordPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user.is_authenticated:
            return False
        if user.role in {Roles.MASTER, Roles.MASTER_EDITOR}:
            return True
        if user.role == Roles.MASTER_VIEWER:
            return request.method in SAFE_METHODS
        membership = obj.base.memberships.filter(user=user).first()
        if not membership:
            return False
        if membership.role == membership.MembershipRole.ADMIN:
            return True
        return request.method in SAFE_METHODS

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
