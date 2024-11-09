import httpx
from fastapi import HTTPException

from ..config import settings


async def _get_management_api_token() -> str:
    """Función auxiliar para obtener un token de acceso de Auth0 Management API."""
    url = f"https://{settings.AUTH0_DOMAIN}/oauth/token"
    payload = {
        "client_id": settings.AUTH0_MANAGEMENT_CLIENT_ID,
        "client_secret": settings.AUTH0_MANAGEMENT_CLIENT_SECRET,
        "audience": settings.AUTH0_MANAGEMENT_AUDIENCE,
        "grant_type": "client_credentials",
        "scope": "update:users read:users",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Failed to obtain Auth0 Management API token: {
                    response.json().get('error_description', 'Unknown error')
                }",
            )

        return response.json()["access_token"]


async def delete_user_in_auth0(user_id: str):
    """Delete a user in Auth0 given their user ID."""
    token = await _get_management_api_token()
    url = f"{settings.AUTH0_MANAGEMENT_AUDIENCE}users/{user_id}"

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    async with httpx.AsyncClient() as client:
        response = await client.delete(url, headers=headers)
        if response.status_code != 204:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Failed to delete user in Auth0: {
                    response.json().get('message', 'Unknown error')
                }",
            )
    return {"message": "User deleted successfully"}


async def update_user_in_auth0(user_id: str, update_data: dict):
    """Actualiza los datos de un usuario en Auth0."""
    token = await _get_management_api_token()
    url = f"{settings.AUTH0_MANAGEMENT_AUDIENCE}users/{user_id}"

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, json=update_data, headers=headers)
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Failed to update user in Auth0: {
                    response.json().get('message', 'Unknown error')
                }",
            )
    return {"message": "User updated successfully"}


async def change_user_password_in_auth0(user_id: str, new_password: str):
    """Cambia la contraseña de un usuario en Auth0."""
    token = await _get_management_api_token()
    url = f"{settings.AUTH0_MANAGEMENT_AUDIENCE}users/{user_id}"

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    payload = {
        "password": new_password,
        "connection": "Username-Password-Authentication",
    }

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, json=payload, headers=headers)
        if response.status_code != 200:
            error_message = response.json().get("message", "Unknown error")
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Failed to change password in Auth0: {error_message}",
            )
    return {"message": "Password changed successfully"}
