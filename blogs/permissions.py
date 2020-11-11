from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Only authors update or delete their blogs"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user
