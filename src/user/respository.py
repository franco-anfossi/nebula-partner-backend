from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import User

# CRUDs for User

async def create_user(
    db: AsyncSession, user_id: str, first_name: str, last_name: str, phone: str = None
) -> User:
    """Create a new user profile and save it to the database."""
    new_user = User(id=user_id, first_name=first_name, last_name=last_name, phone=phone)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def get_user_by_id(db: AsyncSession, user_id: str) -> User:
    """Retrieve a user profile by their ID."""
    result = await db.execute(select(User).where(User.id_auth0 == user_id))
    return result.scalars().first()

async def update_user(
    db: AsyncSession, user_id: str, first_name: str = None, last_name: str = None, phone: str = None
) -> User:
    """Update the details of an existing user profile."""
    user = await get_user_by_id(db, user_id)
    if user:
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        if phone is not None:
            user.phone = phone
        await db.commit()
        await db.refresh(user)
    return user

async def delete_user(db: AsyncSession, user_id: str) -> bool:
    """Delete a user profile by their ID."""
    user = await get_user_by_id(db, user_id)
    if user:
        await db.delete(user)
        await db.commit()
        return True
    return False
