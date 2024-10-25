from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth.jwt_handler import get_current_user
from ..database import get_db
from .repository import (
    create_supplier,
    delete_supplier,
    get_supplier_by_auth_id,
    update_supplier_description,
)

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_new_supplier(
    description: str = None,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """Create a new supplier for the authenticated user."""
    auth_id = user.get("sub")

    if await get_supplier_by_auth_id(db, auth_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Supplier with this Auth0 ID already exists.",
        )

    supplier = await create_supplier(db, auth_id, description)
    return supplier


@router.get("/", status_code=status.HTTP_200_OK)
async def get_my_supplier(
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """Retrieve the authenticated user's supplier."""
    auth_id = user.get("sub")
    supplier = await get_supplier_by_auth_id(db, auth_id)

    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found."
        )
    return supplier


@router.put("/description", status_code=status.HTTP_200_OK)
async def update_my_supplier_description(
    new_description: str,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """Update the description of the authenticated user's supplier."""
    auth_id = user.get("sub")
    supplier = await update_supplier_description(db, auth_id, new_description)

    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found."
        )
    return {"message": "Description updated successfully"}


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def remove_my_supplier(
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """Delete the authenticated user's supplier."""
    auth_id = user.get("sub")
    if not await delete_supplier(db, auth_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found."
        )
    return {"message": "Supplier deleted successfully"}
