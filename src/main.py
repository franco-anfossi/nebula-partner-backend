from fastapi import FastAPI

from .auth.routes import router as auth_router
from .middleware.cors import setup_cors
from .user.routes import router as user_router

app = FastAPI()

setup_cors(app)
app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(user_router, prefix="/api/users", tags=["User"])


@app.get("/")
async def read_root():
    return {"message": "Welcome to the API!"}


@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}
