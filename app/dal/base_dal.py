"""Модуль с абстрактным и базовым классами с DAL CRUD операциями."""

# STDLIB
from abc import ABC, abstractmethod

# THIRDPARTY
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractDAL(ABC):
    """Абстрактный класс с DAL CRUD операциями."""

    @abstractmethod
    async def create(self, *args, **kwargs) -> None:
        """Create операция должна быть реализована при наследовании."""
        pass

    @abstractmethod
    async def get(self, *args, **kwargs) -> None:
        """Get операция должна быть реализована при наследовании."""
        pass

    @abstractmethod
    async def update(self, *args, **kwargs) -> None:
        """Update операция должна быть реализована при наследовании."""
        pass


class Base(AbstractDAL):
    """Базовый DAL класс."""

    def __init__(self, session: AsyncSession):
        """Инициализация сессии бд.

        Args:
            session: AsyncSession
        """
        self.__session = session

    @property
    def session(self) -> AsyncSession:
        """Возвращает объект сессии.

        Returns: AsyncSession

        """
        return self.__session

    async def create(self, *args, **kwargs) -> None:
        """Create operation for Instance."""
        # SQL Alchemy create for Instance
        raise NotImplementedError('This should never happen')

    async def get(self, *args, **kwargs) -> None:
        """Get operation for Instance."""
        # SQL Alchemy get for Instance
        raise NotImplementedError('This should never happen')

    async def update(self, *args, **kwargs) -> None:
        """Update operation for Instance."""
        # SQL Alchemy update for Instance
        raise NotImplementedError('This should never happen')
