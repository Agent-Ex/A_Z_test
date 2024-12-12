"""Модуль со схемами для запросов."""

# STDLIB
import re

# THIRDPARTY
from pydantic import BaseModel, Field, field_validator


class CalcRequestSchema(BaseModel):
    """Схема для POST запроса на расчет.

    Args:
        cadastral_number (str): Кадастровый номер.
        latitude (float): Широта.
        longtitude (float): Долгота.
    """

    cadastral_number: str = Field(..., description='Кадастровый номер')
    latitude: float = Field(..., description='latitude', ge=-90, le=90)
    longtitude: float = Field(..., description='longtitude', ge=-180, le=180)

    @field_validator('cadastral_number')
    def validate_cadastral_number(cls, value: str) -> str:
        """Валидация кадастрового номера.

        Args:
            value (str): Кадастровый номер.

        Returns:
            value: Возвращает кадастровый номер, если данные верного формата.

        Raises:
            ValueError: Если данные неправилные.
        """
        pattern = re.compile(r'^\d{2}:\d{2}:\d{6}:\d{2}$')
        if not pattern.match(value):
            raise ValueError(
                'Кадастровый номер должен быть формата' ' NN:NN:NNNNNN:NN'
            )
        return value
