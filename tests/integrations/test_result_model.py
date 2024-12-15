"""Модуль с тестами сущности Result."""

# THIRDPARTY
from hamcrest import assert_that, has_properties, none, not_none
import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# FIRSTPARTY
from app.database.models import ResultModel, TerritoryModel
from tests.integrations.helpers import (
    create_invalid_result,
    create_valid_result,
)


@pytest.mark.usefixtures('setup_database')
@pytest.mark.integtest
class TestResultModel:
    """Класс для тестирования модели Result.

    Методы проверяют работу CRUD операций для модели и
    проверку на некоректные данные.
    """

    async def test_create_result(self, get_session: AsyncSession) -> None:
        """Тест на создание записи в бд.

        Args:
            get_session (AsyncSession): Асинхронная сессия.
        """
        async with get_session as connection:
            async with connection.begin():
                connection.add(
                    TerritoryModel(
                        cadastral_number='11:11:111111:11',
                        latitude=55.5555,
                        longtitude=55.5555,
                    )
                )
                connection.add(create_valid_result())
                result = await connection.execute(
                    select(ResultModel).filter_by(
                        cadastral_number='11:11:111111:11'
                    )
                )
                result = result.scalars().first()
                assert_that(actual_or_assertion=result, matcher=not_none())
                assert_that(
                    actual_or_assertion=result,
                    matcher=has_properties(
                        {
                            'cadastral_number': '11:11:111111:11',
                            'score': 66.666666,
                        }
                    ),
                )
            async with connection.begin():
                await connection.delete(result)
                await connection.commit()

    async def test_create_invalid_result(
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
                    connection.add(create_invalid_result())

                    await connection.commit()

    async def test_get_result(self, get_session: AsyncSession) -> None:
        """Тест на получение записи в бд.

        Args:
            get_session (AsyncSession): Асинхронная сессия.
        """
        async with get_session as connection:
            async with connection.begin():
                connection.add(create_valid_result())
                result = await connection.execute(
                    select(ResultModel).filter_by(
                        cadastral_number='11:11:111111:11'
                    )
                )
                result = result.scalars().first()
                assert_that(actual_or_assertion=result, matcher=not_none())
                assert_that(
                    actual_or_assertion=result,
                    matcher=has_properties(
                        {
                            'cadastral_number': '11:11:111111:11',
                        }
                    ),
                )
            async with connection.begin():
                await connection.delete(result)
                await connection.commit()

    async def test_get_invalid_result(self, get_session: AsyncSession) -> None:
        """Тест на получение неправильной записи в бд.

        Args:
            get_session (AsyncSession): Асинхронная сессия.
        """
        async with get_session as connection:
            async with connection.begin():
                result = await connection.execute(
                    select(ResultModel).filter_by(score=99.999999)
                )
                result = result.scalars().first()
                assert_that(actual_or_assertion=result, matcher=none())

    async def test_update_result(self, get_session: AsyncSession) -> None:
        """Тест на обновление записи в бд.

        Args:
            get_session (AsyncSession): Асинхронная сессия.
        """
        async with get_session as connection:
            async with connection.begin():
                connection.add(create_valid_result())
                await connection.commit()

            async with connection.begin():
                result = await connection.execute(
                    select(ResultModel).filter_by(score=66.666666)
                )
                result = result.scalars().first()
                assert_that(actual_or_assertion=result, matcher=not_none())

            async with connection.begin():
                to_update = result
                to_update.score = 99.999999
                await connection.merge(to_update)
                await connection.commit()

            async with connection.begin():
                result = await connection.execute(
                    select(ResultModel).filter_by(score=99.999999)
                )
                updated_result = result.scalars().first()
                assert_that(
                    actual_or_assertion=updated_result, matcher=not_none()
                )
                assert_that(
                    actual_or_assertion=updated_result,
                    matcher=has_properties(
                        {
                            'cadastral_number': '11:11:111111:11',
                            'score': 99.999999,
                        }
                    ),
                )
            async with connection.begin():
                await connection.delete(updated_result)
                await connection.commit()

    async def test_delete_result(self, get_session: AsyncSession) -> None:
        """Тест на удаление записи в бд.

        Args:
            get_session (AsyncSession): Асинхронная сессия.
        """
        async with get_session as connection:
            async with connection.begin():
                connection.add(create_valid_result())
                await connection.commit()
            async with connection.begin():
                result = await connection.execute(
                    select(ResultModel).filter_by(score=66.666666)
                )
                result = result.scalars().first()
                assert_that(actual_or_assertion=result, matcher=not_none())
            async with connection.begin():
                await connection.delete(result)
                await connection.commit()
            async with connection.begin():
                result = await connection.execute(
                    select(ResultModel).filter_by(score=66.666666)
                )
                result = result.scalars().first()
                assert_that(actual_or_assertion=result, matcher=none())
