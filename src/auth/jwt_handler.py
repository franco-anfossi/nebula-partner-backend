import os
from typing import Dict

import requests
from fastapi import HTTPException
from fastapi.security import HTTPBearer
from jose import JWTError, jwt

# Variables de entorno cargadas desde el .env
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
API_AUDIENCE = os.getenv("AUTH0_AUDIENCE")
ALGORITHMS = os.getenv("ALGORITHMS", "RS256").split(",")

auth_scheme = HTTPBearer()


def get_rsa_key(token_header: Dict) -> Dict:
    """Obtener la clave pública RSA desde Auth0"""
    jwks_url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
    jwks = requests.get(jwks_url).json()

    for key in jwks["keys"]:
        if key["kid"] == token_header["kid"]:
            return {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }
    raise HTTPException(status_code=401, detail="No se encontró una clave válida")


def verify_jwt(token: str) -> Dict:
    """Verifica y decodifica el JWT"""
    try:
        token_header = jwt.get_unverified_header(token)
        rsa_key = get_rsa_key(token_header)

        if rsa_key:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer=f"https://{AUTH0_DOMAIN}/",
            )
            return payload
    except JWTError as e:
        raise HTTPException(
            status_code=401, detail=f"Token inválido o expirado: {str(e)}"
        )

    raise HTTPException(status_code=401, detail="No se pudo validar el token")
