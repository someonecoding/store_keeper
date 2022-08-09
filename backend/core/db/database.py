from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from core.config import settings

Base = declarative_base()

engine = create_async_engine(settings.DATABASE_URL, echo=True)

session_local = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)


async def get_db() -> AsyncSession:

    async with session_local() as session:
        yield session
