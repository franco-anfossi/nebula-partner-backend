from fastapi import FastAPI

from .auth.routes import router as auth_router
from .middleware.cors import setup_cors
from .supplier.routes import router as supplier_router

app = FastAPI()

setup_cors(app)
app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(supplier_router, prefix="/api/suppliers", tags=["Supplier"])


@app.get("/")
async def read_root():
    return {"message": "Welcome to the API!"}


@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}
