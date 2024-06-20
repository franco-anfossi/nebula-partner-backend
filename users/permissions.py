from rest_framework import permissions


class IsCompanyUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, "company")
