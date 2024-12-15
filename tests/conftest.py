"""Этот модуль содержит фикстуры для тестов.

Автоматизация подготовки среды для проведения тестов моделей с базой данных.
"""

# STDLIB
from typing import AsyncGenerator

# THIRDPARTY
from httpx import AsyncClient
import pytest
from sqlalchemy.exc import InterfaceError
from sqlalchemy.ext.asyncio import AsyncSession

# FIRSTPARTY
from app.database.models import Base
from app.main import app
from app.routers.dependencies import get_prod_session
from tests.config import settings


@pytest.fixture(scope='package', autouse=False)
async def setup_database() -> None:
    """Фикстура для подготовки тестовой базы данных.

    Создает таблицы для тестов перед началом тестирования и
    удаляет их после завершения.

    Yields:
        None: Возвращает управление после создания таблиц, затем удаляет их.
    """
    test_engine = settings.get_engine(use_null_pool=True)
    async with test_engine.begin() as conn:
        try:
            await conn.run_sync(Base.metadata.create_all)
            print('Таблицы для проведения тестов созданы')
        except InterfaceError as e:
            print(f'{e} - Нет подключения к БД.', exc_info=True)

    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='function')
async def get_session() -> AsyncSession:
    """Фикстура для создания экземпляра сессии базы данных для тестов.

    Yields:
        AsyncSession: Асинхронная сессия SQLAlchemy для проведения тестов.
    """
    test_session = settings.get_sessionmaker()
    async with test_session() as session:
        yield session


async def override_get_session() -> AsyncSession:
    """Override Depends для получения асинхронной сессии из test settings.

    Returns:
        AsyncSession

    """
    yield settings.get_session()


app.dependency_overrides[get_prod_session] = override_get_session


@pytest.fixture(scope='session')
async def get_client() -> AsyncGenerator[AsyncClient, None]:
    """Фикстура для создания асинхронного клиента для тестов API.

    Будет использоваться чтобы вызывать HTTP запросу у ендпоинтов FAST API в
    тестах.

    """
    async with AsyncClient(
        app=app, base_url='http://0.0.0.0:7777'
    ) as async_client:
        yield async_client
