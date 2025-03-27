from typing import AsyncIterator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

from app.core.config import settings

Base = declarative_base()

def get_engine(database_url: str):
    """Создает асинхронный движок SQLAlchemy."""
    return create_async_engine(database_url, echo=True, future=True)

engine = get_engine(settings.DATABASE_URL)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, expire_on_commit=False
)

async def get_db() -> AsyncIterator[AsyncSession]:
    """Асинхронный генератор для получения сессии базы данных."""
    async with AsyncSessionLocal() as session:
        yield session
