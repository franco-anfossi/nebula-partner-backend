from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .models import Supplier


async def create_supplier(
    db: AsyncSession,
    company_id: int,
    description: str = None,
    keywords: str = None,
    category: str = None,
) -> Supplier:
    """Create a new supplier profile and save it to the database."""
    new_supplier = Supplier(
        company_id=company_id,
        description=description,
        keywords=keywords,
        category=category,
    )
    db.add(new_supplier)
    await db.commit()
    await db.refresh(new_supplier)
    return new_supplier


async def get_supplier_by_company_id(db: AsyncSession, company_id: int) -> Supplier:
    """Retrieve a supplier profile by its associated company ID."""
    result = await db.execute(select(Supplier).where(Supplier.company_id == company_id))
    return result.scalars().first()


async def get_all_suppliers(db: AsyncSession) -> list[Supplier]:
    """Retrieve all registered suppliers."""
    result = await db.execute(select(Supplier))
    return result.scalars().all()


async def update_supplier(
    db: AsyncSession,
    company_id: int,
    description: str = None,
    keywords: str = None,
    category: str = None,
) -> Supplier:
    """Update the details of an existing supplier profile."""
    supplier = await get_supplier_by_company_id(db, company_id)
    if supplier:
        if description is not None:
            supplier.description = description
        if keywords is not None:
            supplier.keywords = keywords
        if category is not None:
            supplier.category = category
        await db.commit()
        await db.refresh(supplier)
    return supplier


async def delete_supplier(db: AsyncSession, company_id: int) -> bool:
    """Delete a supplier profile by its associated company ID."""
    supplier = await get_supplier_by_company_id(db, company_id)
    if supplier:
        await db.delete(supplier)
        await db.commit()
        return True
    return False


async def count_suppliers(db: AsyncSession) -> int:
    """Return the total number of suppliers."""
    result = await db.execute(select(Supplier))
    return len(result.scalars().all())


async def supplier_exists(db: AsyncSession, company_id: int) -> bool:
    """Check if a supplier exists by their company ID."""
    result = await db.execute(select(Supplier).where(Supplier.company_id == company_id))
    return result.scalars().first() is not None
