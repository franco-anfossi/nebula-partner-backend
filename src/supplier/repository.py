from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .models import Supplier


async def create_supplier(
    db: AsyncSession, auth_id: str, description: str = None
) -> Supplier:
    """Create a new supplier and save it to the database."""
    new_supplier = Supplier(auth_id=auth_id, description=description)
    db.add(new_supplier)
    await db.commit()
    await db.refresh(new_supplier)
    return new_supplier


async def get_supplier_by_auth_id(db: AsyncSession, auth_id: str) -> Supplier:
    """Retrieve a supplier by their Auth0 ID."""
    result = await db.execute(select(Supplier).where(Supplier.auth_id == auth_id))
    return result.scalars().first()


async def get_all_suppliers(db: AsyncSession) -> list[Supplier]:
    """Retrieve all registered suppliers."""
    result = await db.execute(select(Supplier))
    return result.scalars().all()


async def update_supplier_description(
    db: AsyncSession, auth_id: str, new_description: str
) -> Supplier:
    """Update the description of an existing supplier."""
    supplier = await get_supplier_by_auth_id(db, auth_id)
    if supplier:
        supplier.description = new_description
        await db.commit()
        await db.refresh(supplier)
    return supplier


async def delete_supplier(db: AsyncSession, auth_id: str) -> bool:
    """Delete a supplier by their Auth0 ID."""
    supplier = await get_supplier_by_auth_id(db, auth_id)
    if supplier:
        await db.delete(supplier)
        await db.commit()
        return True
    return False


async def count_suppliers(db: AsyncSession) -> int:
    """Return the total number of suppliers."""
    result = await db.execute(select(Supplier))
    return len(result.scalars().all())


async def supplier_exists(db: AsyncSession, auth_id: str) -> bool:
    """Check if a supplier exists by their Auth0 ID."""
    result = await db.execute(select(Supplier).where(Supplier.auth_id == auth_id))
    return result.scalars().first() is not None
