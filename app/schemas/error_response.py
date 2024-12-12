"""Pydantic схемы для ошибок."""

# THIRDPARTY
from pydantic import BaseModel, ConfigDict, Field


class ErrorResponse(BaseModel):
    """Pydantic модель для ответа во время ошибки."""

    model_config = ConfigDict(
        populate_by_name=True,
    )
    code: int
    type_: str = Field(alias='type')
    message: str
