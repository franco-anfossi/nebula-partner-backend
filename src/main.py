from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .auth.routes import router as auth_router
from .config import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS.split(","),
    allow_credentials=settings.ALLOW_CREDENTIALS,
    allow_methods=settings.ALLOWED_METHODS.split(","),
    allow_headers=settings.ALLOWED_HEADERS.split(","),
)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])

# Ruta de bienvenida
@app.get("/")
async def read_root():
    return {"message": "Welcome to the API!"}


# Ruta de salud para verificar si la API está funcionando
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
