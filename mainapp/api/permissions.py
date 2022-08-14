from rest_framework import permissions


class NotAuthenticated(permissions.BasePermission):
    def has_permission(self, request, *_):
        return not request.user.is_authenticated


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, _, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user
