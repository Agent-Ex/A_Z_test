"""DAL CRUD операции для сущности Territory."""

# STDLIB
from socket import gaierror

# THIRDPARTY
from pydantic import validate_call
from sqlalchemy.exc import InterfaceError
from sqlalchemy.ext.asyncio import AsyncSession

# FIRSTPARTY
from app.dal.base_dal import Base
from app.database.models import ResultModel, TerritoryModel
from app.routers.common_http_exceptions import exception_500_db_connection
from app.schemas.territory import CalcRequestSchema


class Territory(Base):
    """Класс с DAL CRUD операциями для сущности Territory."""

    def __init__(self, session: AsyncSession) -> None:
        """Инициализация сессии.

        Args:
            session (AsyncSession): асинхронная сессия.

        """
        super().__init__(session=session)

    @validate_call
    async def create(self, data: CalcRequestSchema) -> int | None:
        """SQL Alchemy запрос на создание записей по территории.

        Args:
            data (CalcRequestSchema): Данные для создания сущности.

        Returns:
            ResultModel.id_: Возвращение ID из таблицы с счетом.

        Raises:
            ValidationError: Если Pydantic обнаружит неправильные данные.
            InterfaceError: при работе вне развернутого окружения, когда нет
                подключения к БД.
            gaierror: когда нет подrлючения к контейнеру БД в развернутом
                Docker Compose.

        """
        record_territory = TerritoryModel(
            cadastral_number=data.cadastral_number,
            latitude=data.latitude,
            longtitude=data.longtitude,
        )
        record_result = ResultModel(cadastral_number=data.cadastral_number)
        try:
            self.session.add(instance=record_territory)
            self.session.add(instance=record_result)
            await self.session.commit()
        except InterfaceError:
            await self.session.rollback()
        except gaierror:
            raise exception_500_db_connection

        return record_result.id_
