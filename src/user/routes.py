from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth.auth0_helper import delete_user_in_auth0
from ..auth.jwt_handler import get_current_user
from ..database import get_db
from ..exceptions import HTTPException, ResourceNotFound
from .repository import create_user, delete_user, get_user
from .schemas import UserCreate, UserResponse, UserUpdate
from .service import update_user_data

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_new_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Create a new user for the authenticated Auth0 user."""
    auth_id = current_user.get("sub")

    if await get_user(db, auth_id):
        raise ResourceNotFound("User with this Auth0 ID already exists.")

    user_data_with_auth = user_data.model_copy(update={"id_auth0": auth_id})

    user = await create_user(db, user_data_with_auth)
    return user


@router.get("/", response_model=UserResponse)
async def read_user(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Retrieve details of the authenticated user."""
    auth_id = current_user.get("sub")
    user = await get_user(db, auth_id)
    if not user:
        raise ResourceNotFound("User")
    return user


@router.patch("/", response_model=UserResponse)
async def update_existing_user(
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Update the authenticated user's data, including Auth0 data."""
    auth_id = current_user.get("sub")

    try:
        user = await update_user_data(db, auth_id, user_data)
    except ResourceNotFound:
        raise ResourceNotFound("User")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

    return user


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_account(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Delete the authenticated user's account."""
    auth_id = current_user.get("sub")

    success = await delete_user(db, auth_id)
    if not success:
        raise ResourceNotFound("User")

    try:
        await delete_user_in_auth0(auth_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete user in Auth0: {str(e)}",
        )
    return {"message": "User deleted successfully"}
