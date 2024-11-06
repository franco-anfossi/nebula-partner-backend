from models import Account
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# CRUDs for Account


async def create_account(
    db: AsyncSession, user_id: str, company_id: int = None, is_active: bool = True
) -> Account:
    """Create a new account and save it to the database."""
    new_account = Account(user_id=user_id, company_id=company_id, is_active=is_active)
    db.add(new_account)
    await db.commit()
    await db.refresh(new_account)
    return new_account


async def get_account_by_user_and_company(
    db: AsyncSession, user_id: str, company_id: int
) -> Account:
    """Retrieve an account by user profile ID and company ID."""
    result = await db.execute(
        select(Account).where(
            Account.user_id == user_id, Account.company_id == company_id
        )
    )
    return result.scalars().first()


async def get_all_accounts_for_user(db: AsyncSession, user_id: str) -> list[Account]:
    """Retrieve all accounts associated with a specific user profile."""
    result = await db.execute(select(Account).where(Account.user_id == user_id))
    return result.scalars().all()


async def update_account_status(
    db: AsyncSession, user_id: str, company_id: int, is_active: bool
) -> Account:
    """Update the active status of an account."""
    account = await get_account_by_user_and_company(db, user_id, company_id)
    if account:
        account.is_active = is_active
        await db.commit()
        await db.refresh(account)
    return account


async def delete_account(db: AsyncSession, user_id: str, company_id: int) -> bool:
    """Delete an account by user profile ID and company ID."""
    account = await get_account_by_user_and_company(db, user_id, company_id)
    if account:
        await db.delete(account)
        await db.commit()
        return True
    return False
