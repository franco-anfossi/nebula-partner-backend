from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .models import User
from .schemas import UserCreate, UserResponse


async def get_user(db: AsyncSession, user_id: str) -> UserResponse:
    """Fetches a user by their Auth0 ID."""
    result = await db.execute(select(User).filter(User.id_auth0 == user_id))
    user = result.scalars().first()
    return user


async def create_user(db: AsyncSession, user_data: UserCreate) -> UserResponse:
    """Creates a new user."""
    user = User(**user_data.model_dump())
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def update_user(
    db: AsyncSession, user_id: str, user_data: UserCreate
) -> UserResponse:
    """Updates an existing user."""
    result = await db.execute(select(User).filter(User.id_auth0 == user_id))
    user = result.scalars().first()

    if user:
        for key, value in user_data.model_dump(exclude_unset=True).items():
            setattr(user, key, value)
        await db.commit()
        await db.refresh(user)
    return user


async def delete_user(db: AsyncSession, user_id: str) -> bool:
    """Deletes a user by their Auth0 ID."""
    result = await db.execute(select(User).filter(User.id_auth0 == user_id))
    user = result.scalars().first()

    if user:
        await db.delete(user)
        await db.commit()
        return True
    return False
