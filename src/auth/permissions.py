from ..exceptions import PermissionDenied


def check_user_permission(auth_id: str, user_id: str):
    """Checks if the authenticated user has permission to access the resource."""
    if auth_id != user_id:
        raise PermissionDenied("You do not have permission to access this resource.")
