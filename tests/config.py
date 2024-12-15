"""В этом модулле определлен класс настроек подключения к тестовой базе данных.

Он включает настройку подключения к базе данных на основе переменных окружения.

В нем переопределен метод генерации сессии с использованием NullPool.
"""

# THIRDPARTY
from pydantic import ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

# FIRSTPARTY
from app.database.db_base_config import Settings as PostgresSettings

ENV_FILENAME = '.test.env'


class SettingsTestPostgresEnvironment(PostgresSettings):
    """Класс для настройки подключения к тестовой базе данных.

    Этот класс переопределяет переменные окружения, необходимые для
    подключения к тестовой базе данных.
    """

    model_config = ConfigDict(env_file=ENV_FILENAME)

    def get_sessionmaker(self) -> async_sessionmaker:
        """Создает и возвращает асинхронную сессию с использованием NullPool.

        Returns:
            session(AsyncSession).
        """
        return async_sessionmaker(
            self.get_engine(use_null_pool=True),
            expire_on_commit=False,
            class_=AsyncSession,
        )


settings = SettingsTestPostgresEnvironment()
