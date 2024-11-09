from databases import Database
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.config import settings

DATABASE_URL = settings.DATABASE_URL
engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()

from src.company.models import Company  # noqa
from src.account.models import Account  # noqa
from src.user.models import User  # noqa
from src.supplier.models import Supplier  # noqa

async_session = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

database = Database(DATABASE_URL)


async def get_db():
    async with async_session() as session:
        yield session
        await session.close()
