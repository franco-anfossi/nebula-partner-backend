from models import Company
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# CRUDs for Company


async def create_company(
    db: AsyncSession, legal_name: str, tax_id: str, is_active: bool = True
) -> Company:
    """Create a new company and save it to the database."""
    new_company = Company(legal_name=legal_name, tax_id=tax_id, is_active=is_active)
    db.add(new_company)
    await db.commit()
    await db.refresh(new_company)
    return new_company


async def get_company_by_tax_id(db: AsyncSession, tax_id: str) -> Company:
    """Retrieve a company by its tax ID."""
    result = await db.execute(select(Company).where(Company.tax_id == tax_id))
    return result.scalars().first()


async def get_all_companies(db: AsyncSession) -> list[Company]:
    """Retrieve all registered companies."""
    result = await db.execute(select(Company))
    return result.scalars().all()


async def update_company_status(
    db: AsyncSession, tax_id: str, is_active: bool
) -> Company:
    """Update the active status of a company."""
    company = await get_company_by_tax_id(db, tax_id)
    if company:
        company.is_active = is_active
        await db.commit()
        await db.refresh(company)
    return company


async def delete_company(db: AsyncSession, tax_id: str) -> bool:
    """Delete a company by its tax ID."""
    company = await get_company_by_tax_id(db, tax_id)
    if company:
        await db.delete(company)
        await db.commit()
        return True
    return False
