from fastapi import HTTPException, status


def has_permission(user: dict, permission: str) -> bool:
    """Verifica si el usuario tiene el permiso necesario."""
    if permission not in user.get("permissions", []):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para realizar esta acción.",
        )
    return True
