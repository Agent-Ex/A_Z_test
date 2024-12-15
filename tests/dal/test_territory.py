"""Тест для CRUD операций DAL класса Terrirory."""

# STDLIB
from dataclasses import dataclass

# THIRDPARTY
from hamcrest import assert_that, is_not
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

# FIRSTPARTY
from app.dal.territory import Territory
from app.schemas.territory import CalcRequestSchema
from tests.config import settings


@dataclass
class TerritoryData:
    """Dataclass для тестов сущности Territory."""

    cadastral_number: str = '66:66:666666:66'
    latitude: float = -30.2125
    longtitude: float = 70.1578


@pytest.mark.usefixtures('setup_database')
@pytest.mark.integtest
class TestTerritory:
    """Класс методов с тестами сущности Territory."""

    dal = Territory(session=settings.get_session())

    async def test_create(self, get_session: AsyncSession) -> None:
        """Тест на функцию create класса Territory.

        Args:
            get_session: get_session: фикстура с AsyncSession.
        """
        response = await self.dal.create(
            data=CalcRequestSchema(
                cadastral_number=TerritoryData.cadastral_number,
                latitude=TerritoryData.latitude,
                longtitude=TerritoryData.longtitude,
            )
        )
        assert_that(actual_or_assertion=response, matcher=is_not(None))
