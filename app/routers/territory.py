"""Модуль с ендпоинтами."""

# STDLIB
import asyncio
import random

# THIRDPARTY
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

# FIRSTPARTY
from app.dal.result import Result
from app.dal.territory import Territory
from app.routers.dependencies import get_prod_session
from app.schemas.territory import CalcRequestSchema

router = APIRouter()


async def remote_calculation(
    data: CalcRequestSchema, session: AsyncSession
) -> None:
    """Имитация сервиса вычислений.

    Args:
        data (CalcRequestSchema): Инофрмация для вычислений.
        session (AsyncSession): Асинхронная сессия для подключения к бд.
    """
    await asyncio.sleep(random.randint(10, 20))
    score = round(random.uniform(-100, 100), 6)
    result = Result(session=session)
    await result.update(cadastral_number=data.cadastral_number, score=score)


@router.post('/calc/')
async def post_to_result(
    body: CalcRequestSchema, session: AsyncSession = Depends(get_prod_session)
) -> int:
    """Функция получает тело запроса и возвращает ID из бд.

    Args:
        body (CalcRequestSchema): Тело запроса для вычислений.
        session (AsyncSession): Асинхронная сессия для подключения к бд.

    Returns:
        ID записи в бд.
    """
    territory = Territory(session=session)
    id_ = await territory.create(data=body)
    await remote_calculation(data=body, session=session)
    return id_


@router.get('/result/')
async def get_result(
    result_id: int,
    session: AsyncSession = Depends(get_prod_session),
) -> JSONResponse:
    """Функция берет на вход ID и возвращает результат расчетов.

    Args:
        result_id (int): ID записи в бд для получения информации score.
        session (AsyncSession): Асинхронная сессия для подключения к бд.

    Returns:
        JSONResponse: JSON формата {'score': -45.123125}.
    """
    result = Result(session=session)
    result = await result.get(id_=result_id)
    return {'score': result}
