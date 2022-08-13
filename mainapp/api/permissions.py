from rest_framework.permissions import BasePermission


class NotAuthenticated(BasePermission):
    def has_permission(self, request, *_):
        return not request.user.is_authenticated
