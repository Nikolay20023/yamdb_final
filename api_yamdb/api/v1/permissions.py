from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS


class AdminOrSuperUSerOnly(BasePermission):
    """Пермишоны для админа или суперпользователя."""

    def has_permission(self, request, view):
        """."""
        return request.user.is_admin or request.user.is_superuser


class AuthenticatedOrReadOnly(BasePermission):
    """Пермишоны для Аунтифицированого пользователя."""

    def has_permission(self, request, view):
        """."""
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        """."""
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_superuser
            or request.user.is_admin
            or request.user.is_moderator
        )


class AdminOrReadOnly(BasePermission):
    """Пермишон для админа."""

    def has_permission(self, request, view):
        """."""
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
            or request.user.is_superuser
        )


class CommentRewiewPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
        )
