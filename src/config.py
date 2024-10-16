from typing import Optional

from dotenv import load_dotenv
from pydantic import AnyHttpUrl, ConfigDict
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """
    Configuración de la aplicación utilizando Pydantic
    para validar y cargar variables de entorno.
    """

    # Configuración general de entorno
    ENV: str
    DEBUG: bool

    # Configuración de la base de datos
    DATABASE_URL: str

    # Configuración de Auth0
    AUTH0_DOMAIN: str
    AUTH0_CLIENT_ID: str
    AUTH0_CLIENT_SECRET: str
    AUTH0_AUDIENCE: Optional[str]
    AUTH0_CALLBACK_URL: Optional[AnyHttpUrl]

    # Configuración de JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

    # Configuración de CORS
    ALLOWED_ORIGINS: str = ["*"]
    ALLOWED_METHODS: str = ["*"]
    ALLOWED_HEADERS: str = ["*"]
    ALLOW_CREDENTIALS: bool = True

    model_config = ConfigDict(case_sensitive=True)


# Crear una instancia de configuración que puedas utilizar en toda la app.
settings = Settings()
