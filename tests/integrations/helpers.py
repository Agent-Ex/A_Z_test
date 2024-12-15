"""Модуль для вспомогательных методов."""

# FIRSTPARTY
from app.database.models import ResultModel, TerritoryModel


def create_valid_territory() -> TerritoryModel:
    """Данные для создания валидной сущности Territory.

    Returns:
        TerritoryModel: Экземпляр валидной сущности
    """
    return TerritoryModel(
        cadastral_number='11:11:111111:12',
        latitude=66.6666,
        longtitude=66.6666,
    )


def create_invalid_territory() -> TerritoryModel:
    """Данные для создания валидной сущности Territory.

    Returns:
        TerritoryModel: Экземпляр невалидной сущности.
    """
    return TerritoryModel(
        cadastral_number='11:11:111111:11',
        latitude=5.1,
        longtitude=True,
    )


def create_valid_result() -> ResultModel:
    """Данные для создания валидной сущности Result.

    Returns:
        ResultModel: Экземпляр валидной сущности
    """
    return ResultModel(
        cadastral_number='11:11:111111:11',
        score=66.666666,
    )


def create_invalid_result() -> ResultModel:
    """Данные для создания валидной сущности Result.

    Returns:
        ResultModel: Экземпляр невалидной сущности.
    """
    return ResultModel(
        cadastral_number='11:1',
        score=66.666666,
    )
