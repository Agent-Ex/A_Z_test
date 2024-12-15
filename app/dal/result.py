"""DAL CRUD операции для сущности Result."""

# STDLIB
from socket import gaierror

# THIRDPARTY
from sqlalchemy import select, update
from sqlalchemy.exc import InterfaceError
from sqlalchemy.ext.asyncio import AsyncSession

# FIRSTPARTY
from app.dal.base_dal import Base
from app.database.models import ResultModel
from app.routers.common_http_exceptions import exception_500_db_connection


class Result(Base):
    """Класс с DAL CRUD операциями для сущности Result."""

    def __init__(self, session: AsyncSession) -> None:
        """Инициализация сессии.

        Args:
            session (AsyncSession): асинхронная сессия.

        """
        super().__init__(session=session)

    async def update(self, cadastral_number: str, score: float) -> None:
        """SQL Alchemy запрос на запись счета.

        Args:
            id_ (int): Данные для нахождения сущности, которую надо обновить.

        Raises:
            InterfaceError: при работе вне развернутого окружения, когда нет
                подключения к БД.
            gaierror: когда нет подrлючения к контейнеру БД в развернутом
                Docker Compose.
        """
        try:
            await self.session.execute(
                update(ResultModel)
                .filter(ResultModel.cadastral_number == cadastral_number)
                .values(score=score)
            )
            await self.session.commit()
        except InterfaceError:
            await self.session.rollback()
        except gaierror:
            raise exception_500_db_connection

    async def get(self, id_: int) -> float:
        """SQL Alchemy запрос на получение счета по ID записи.

        Args:
            id_ (int): Данные для получения сущности.

        Returns:
            score: Возвращение score из таблицы с счетом.

        Raises:
            InterfaceError: при работе вне развернутого окружения, когда нет
                подключения к БД.
            gaierror: когда нет подrлючения к контейнеру БД в развернутом
                Docker Compose.

        """
        try:
            result = await self.session.execute(
                select(ResultModel.score).filter(ResultModel.id_ == id_)
            )
        except InterfaceError:
            await self.session.rollback()
        except gaierror:
            raise exception_500_db_connection
        record = result.all()[0].score
        if record:
            return record
        elif result:
            return 'Расчет еще не выполнен'
