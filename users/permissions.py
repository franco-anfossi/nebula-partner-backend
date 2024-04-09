from rest_framework import permissions
from .models import Company

class IsCompanyUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'company')