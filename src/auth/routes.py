from fastapi import APIRouter, Depends

from src.auth.jwt_handler import auth_scheme, verify_jwt

router = APIRouter()


@router.get("/private")
async def private_route(token: str = Depends(auth_scheme)):
    """Ruta privada que requiere autenticación con JWT."""
    payload = verify_jwt(token.credentials)
    return {"message": "Ruta privada", "user": payload}
