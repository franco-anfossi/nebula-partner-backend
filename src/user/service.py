from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth.auth0_helper import change_user_password_in_auth0, update_user_in_auth0
from ..exceptions import ResourceNotFound
from .repository import update_user
from .schemas import UserUpdate


async def update_user_data(db: AsyncSession, auth_id: str, user_data: UserUpdate):
    """Update user data in the local database and Auth0 if needed."""
    # Actualizar datos locales
    local_update_data = _prepare_local_update_data(user_data)
    if local_update_data:
        user = await update_user(db, auth_id, user_data)
        if not user:
            raise ResourceNotFound("User")
    else:
        user = None

    # Actualizar datos en Auth0
    auth0_update_data = _prepare_auth0_update_data(user_data)
    if auth0_update_data:
        try:
            await update_user_in_auth0(auth_id, auth0_update_data)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update user in Auth0: {str(e)}",
            )

    # Cambiar la contraseña en Auth0
    if user_data.password:
        try:
            await change_user_password_in_auth0(auth_id, user_data.password)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to change user password in Auth0: {str(e)}",
            )

    return user or {"message": "User updated successfully"}


def _prepare_local_update_data(user_data: UserUpdate):
    """Prepare data to update in the local database."""
    local_update_data = {
        "first_name": user_data.first_name,
        "last_name": user_data.last_name,
        "phone": user_data.phone,
    }
    return {k: v for k, v in local_update_data.items() if v is not None}


def _prepare_auth0_update_data(user_data: UserUpdate):
    """Prepare data to update in Auth0."""
    auth0_update_data = {}
    if user_data.nickname:
        auth0_update_data["nickname"] = user_data.nickname
    if user_data.email:
        auth0_update_data["email"] = user_data.email
    return auth0_update_data
