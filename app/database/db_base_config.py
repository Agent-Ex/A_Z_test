"""Этот модуль содержит базовый класс настроек сессии.

Класс Settings определяет методы генерации URL(get_db_url), engine(get_engine)
и session(get_session).

Он включает настройку подключения к базе данных на основе переменных окружения.

Пример использования методов класса:
    settings = Settings().
    db_url = settings.get_db_url().
    engine = settings.get_engine(use_null_pool=True).
    async_session = settings.get_session().

"""

# THIRDPARTY
from pydantic import ConfigDict
from pydantic_settings import BaseSettings
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

ASYNC_DRIVER = 'postgresql+asyncpg'


class Settings(BaseSettings):
    """Класс для настройки переменных окружения для подключения к базе данных.

    Этот класс загружает переменные окружения, используемые для формирования
    URL подключения к базе данных.

    Атрибуты:
        postgres_host (str): Адрес хоста базы данных
        postgres_port (int): Порт для подключения к базе данных
        postgres_db_name (str): Имя базы данных
        postgres_user (str): Имя пользователя базы данных
        postgres_password (str): Пароль для подключения к базе данных

    Параметры загружаются из .env файла


    Исключения:
        KeyError: Если переменные окружения для подключения не определены.

    """

    postgres_host: str
    postgres_port: int
    postgres_db_name: str
    postgres_user: str
    postgres_password: str
    model_config = ConfigDict(extra='ignore')

    def get_db_url(self) -> URL:
        """Формирует URL подключения к базе данных.

        Создает строку подключения к базе данных,
        используя переменные окружения.

        Returns:
            str: URL для подключения к базе данных в формате SQLAlchemy.

        """
        return URL.create(
            drivername=ASYNC_DRIVER,
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_host,
            port=self.postgres_port,
            database=self.postgres_db_name,
        )

    def get_engine(self, use_null_pool: bool = False) -> AsyncEngine:
        """Создает движок асинхронной сессии с выбором типа пула.

        Args:
            use_null_pool(bool): Выбор NullPool для сессии SQLAlchemy.

        """
        pool_class = NullPool if use_null_pool else None
        return create_async_engine(self.get_db_url(), poolclass=pool_class)

    def get_sessionmaker(self) -> async_sessionmaker:
        """Создает и возвращает асинхронную сессию.

        Returns:
            session(AsyncSession).

        """
        return async_sessionmaker(
            self.get_engine(), expire_on_commit=False, class_=AsyncSession
        )

    def get_session(self) -> AsyncSession:
        """Возвращает сессию подключения к БД.

        Returns: AsyncSession

        """
        return self.get_sessionmaker()()
