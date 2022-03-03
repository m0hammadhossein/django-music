from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsUserComment(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS or
               obj.user == request.user)