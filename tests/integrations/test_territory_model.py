"""Модуль с тестами сущности Territory."""

# THIRDPARTY
from hamcrest import assert_that, has_properties, none, not_none
import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# FIRSTPARTY
from app.database.models import TerritoryModel
from tests.integrations.helpers import (
    create_invalid_territory,
    create_valid_territory,
)


@pytest.mark.usefixtures('setup_database')
@pytest.mark.integtest
class TestTerritoryModel:
    """Класс для тестирования модели Territory.

    Методы проверяют работу CRUD операций для модели и
    проверку на некоректные данные.
    """

    async def test_create_territory(self, get_session: AsyncSession) -> None:
        """Тест на создание записи в бд.

        Args:
            get_session (AsyncSession): Асинхронная сессия.
        """
        async with get_session as connection:
            async with connection.begin():
                connection.add(create_valid_territory())
                result = await connection.execute(
                    select(TerritoryModel).filter_by(
                        cadastral_number='11:11:111111:12'
                    )
                )
                result = result.scalars().first()
                assert_that(actual_or_assertion=result, matcher=not_none())
                assert_that(
                    actual_or_assertion=result,
                    matcher=has_properties(
                        {
                            'cadastral_number': '11:11:111111:12',
                            'latitude': 66.6666,
                            'longtitude': 66.6666,
                        }
                    ),
                )
            async with connection.begin():
                await connection.delete(result)
                await connection.commit()

    async def test_create_invalid_territory(
        self, get_session: AsyncSession
    ) -> None:
        """Тест на создание неправильной записи в бд.

        Проверка на ошибку IntegrityError

        Args:
            get_session (AsyncSession): Асинхронная сессия.
        """
        async with get_session as connection:
            async with connection.begin():
                with pytest.raises(IntegrityError):
                    connection.add(create_invalid_territory())

                    await connection.commit()

    async def test_get_territory(self, get_session: AsyncSession) -> None:
        """Тест на получение записи в бд.

        Args:
            get_session (AsyncSession): Асинхронная сессия.
        """
        async with get_session as connection:
            async with connection.begin():
                connection.add(create_valid_territory())
                result = await connection.execute(
                    select(TerritoryModel).filter_by(
                        cadastral_number='11:11:111111:12'
                    )
                )
                result = result.scalars().first()
                assert_that(actual_or_assertion=result, matcher=not_none())
                assert_that(
                    actual_or_assertion=result,
                    matcher=has_properties(
                        {
                            'cadastral_number': '11:11:111111:12',
                        }
                    ),
                )
            async with connection.begin():
                await connection.delete(result)
                await connection.commit()

    async def test_get_invalid_territory(
        self,
        get_session: AsyncSession,
    ) -> None:
        """Тест на получение неправильной записи в бд.

        Args:
            get_session (AsyncSession): Асинхронная сессия.
        """
        async with get_session as connection:
            async with connection.begin():
                result = await connection.execute(
                    select(TerritoryModel).filter_by(latitude=99.6666)
                )
                result = result.scalars().first()
                assert_that(actual_or_assertion=result, matcher=none())

    async def test_update_territory(self, get_session: AsyncSession) -> None:
        """Тест на обновление записи в бд.

        Args:
            get_session (AsyncSession): Асинхронная сессия.
        """
        async with get_session as connection:
            async with connection.begin():
                connection.add(create_valid_territory())
                await connection.commit()

            async with connection.begin():
                result = await connection.execute(
                    select(TerritoryModel).filter_by(
                        cadastral_number='11:11:111111:12'
                    )
                )
                result = result.scalars().first()
                assert_that(actual_or_assertion=result, matcher=not_none())

            async with connection.begin():
                to_update = result
                to_update.latitude = 99.9999
                await connection.merge(to_update)
                await connection.commit()

            async with connection.begin():
                result = await connection.execute(
                    select(TerritoryModel).filter_by(latitude=99.9999)
                )
                updated_result = result.scalars().first()
                assert_that(
                    actual_or_assertion=updated_result, matcher=not_none()
                )
                assert_that(
                    actual_or_assertion=updated_result,
                    matcher=has_properties(
                        {
                            'cadastral_number': '11:11:111111:12',
                            'latitude': 99.9999,
                        }
                    ),
                )
            async with connection.begin():
                await connection.delete(updated_result)
                await connection.commit()

    async def test_delete_territory(self, get_session: AsyncSession) -> None:
        """Тест на удаление записи в бд.

        Args:
            get_session (AsyncSession): Асинхронная сессия.
        """
        async with get_session as connection:
            async with connection.begin():
                connection.add(create_valid_territory())
                await connection.commit()
            async with connection.begin():
                result = await connection.execute(
                    select(TerritoryModel).filter_by(
                        cadastral_number='11:11:111111:12'
                    )
                )
                result = result.scalars().first()
                assert_that(actual_or_assertion=result, matcher=not_none())
            async with connection.begin():
                await connection.delete(result)
                await connection.commit()
            async with connection.begin():
                result = await connection.execute(
                    select(TerritoryModel).filter_by(
                        cadastral_number='11:11:111111:12'
                    )
                )
                result = result.scalars().first()
                assert_that(actual_or_assertion=result, matcher=none())
