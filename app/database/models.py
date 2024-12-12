"""Модуль с моделями сущностей."""

# STDLIB
from typing import List

# THIRDPARTY
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Базовый класс."""

    pass


class TerritoryModel(Base):
    """Класс, определяющий кадастровый номер с координатами объекта.

    Args:
        cadastral_number (str): Кадастровый номер объекта.
        latitude (float): Широта.
        longtitude (float): Долгота.
    """

    __tablename__ = 'territory'

    cadastral_number: Mapped[str] = mapped_column(primary_key=True)
    latitude: Mapped[float] = mapped_column(nullable=False)
    longtitude: Mapped[float] = mapped_column(nullable=False)

    result: Mapped[List['ResultModel']] = relationship(
        back_populates='territory'
    )


class ResultModel(Base):
    """Класс, определяющий вычисления по кадастровому номеру.

    Args:
        id_ (int): id записи.
        cadastral_number (str): Кадастровый номер, по которому ведется расчет.
        score (float): результат расчетов.
    """

    __tablename__ = 'result'

    id_: Mapped[int] = mapped_column(name='id', primary_key=True)
    cadastral_number: Mapped[str] = mapped_column(
        ForeignKey('territory.cadastral_number', ondelete='CASCADE')
    )
    score: Mapped[float] = mapped_column(nullable=True)

    territory: Mapped[List['TerritoryModel']] = relationship(
        back_populates='result'
    )
