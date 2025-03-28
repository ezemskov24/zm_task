from typing import AsyncGenerator

import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.auth.verify import verify_token
from app.main import app
from app.core.database import Base, get_db
from app.schemas.token_schemas import TokenData


DATABASE_URL_TEST = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(DATABASE_URL_TEST, echo=True)
TestingSessionLocal = sessionmaker(
    bind=test_engine, expire_on_commit=False, class_=AsyncSession
)


@pytest_asyncio.fixture(scope="function")
async def db() -> AsyncGenerator:
    """
    Фикстура для подготовки и очистки базы данных перед и после каждого теста

    :yield: Управление временем жизни базы данных
    """
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session(db) -> AsyncSession:
    """
    Фикстура для создания сессии базы данных для каждого теста

    :param db: Фикстура базы данных
    :yield: Асинхронная сессия базы данных
    """
    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture(scope="function")
async def client(db_session) -> AsyncGenerator:
    """
    Фикстура для создания клиента FastAPI для каждого теста

    :param db_session: Фикстура сессии базы данных
    :yield: Экземпляр клиента для отправки запросов на сервер
    """
    def mock_verify_token():
        return TokenData(sub="testuser")

    app.dependency_overrides[verify_token] = mock_verify_token
    app.dependency_overrides[get_db] = lambda: db_session

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
