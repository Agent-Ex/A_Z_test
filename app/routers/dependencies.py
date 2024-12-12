"""Общие зависимости для роутеров."""

# THIRDPARTY
from sqlalchemy.ext.asyncio import AsyncSession

# FIRSTPARTY
from app.database.db_prod_config import settings


async def get_prod_session() -> AsyncSession:
    """Depends для получения асинхронной сессии из prod settings.

    Returns:
        AsyncSession: сессия для подключения к основной БД.

    """
    async with settings.get_session() as session:
        yield session
