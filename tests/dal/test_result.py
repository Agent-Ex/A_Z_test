"""Тест для CRUD операций DAL класса Result."""

# STDLIB
from dataclasses import dataclass

# THIRDPARTY
from hamcrest import assert_that, equal_to
import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# FIRSTPARTY
from app.dal.result import Result
from app.dal.territory import Territory
from app.database.models import ResultModel
from app.schemas.territory import CalcRequestSchema
from tests.config import settings


@dataclass
class ResultData:
    """Dataclass для теста сущности Result."""

    cadastral_number: str = '66:66:666666:65'
    score: float = 55.532757
    latitude: float = -30.2155
    longtitude: float = 70.1558


@pytest.mark.usefixtures('setup_database')
@pytest.mark.integtest
class TestResult:
    """Класс методов с тестами сущности Result."""

    dal_result = Result(session=settings.get_session())
    dal_territory = Territory(session=settings.get_session())

    async def test_update(self, get_session: AsyncSession) -> None:
        """Тест на функцию update класса Result.

        Args:
            get_session: get_session: фикстура с AsyncSession.
        """
        await self.dal_territory.create(
            data=CalcRequestSchema(
                cadastral_number=ResultData.cadastral_number,
                latitude=ResultData.latitude,
                longtitude=ResultData.longtitude,
            )
        )
        await self.dal_result.update(
            cadastral_number=ResultData.cadastral_number,
            score=ResultData.score,
        )
        async with get_session as connection:
            result = select(ResultModel.score).filter(ResultModel.id_ == 1)
            result = (await connection.execute(result)).first()

        assert_that(
            actual_or_assertion=result.score,
            matcher=equal_to(ResultData.score),
        )

    async def test_get(self, get_session: AsyncSession) -> None:
        """Тест на функцию get класса Result.

        Args:
            get_session: get_session: фикстура с AsyncSession.
        """
        result = await self.dal_result.get(id_=1)
        assert_that(
            actual_or_assertion=result, matcher=equal_to(ResultData.score)
        )
