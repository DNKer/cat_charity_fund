from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt

from app.core.config import settings


class CharityProjectBase(BaseModel):
    """
    Схема, от которой наследуем все остальные.
    Дополнительные поля и использование пустой модели запрещено
    через подкласс Config (параметры, неописанные в схеме,
    не принимаются).
    """

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    """
    Схема `Проект` (создание).
    Параметры:
    name — уникальное название проекта
    description — описание
    full_amount — требуемая сумма
    """

    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):
    """
    Схема `Проект` (обновление).
    """

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str]
    full_amount: Optional[PositiveInt]


class CharityProjectDB(CharityProjectCreate):
    """
    Схема, описывающая объект `Проект`,
    полученный из БД. Cхема может принимать
    на вход объект базы данных, а не только
    Python-словарь или JSON-объект.
    Параметры:
    id — первичный ключ
    invested_amount — внесённая сумма
    fully_invested — значение, указывающее
                    на то, собрана ли нужная
                    сумма для проекта (закрыт
                    ли проект)
    create_date — дата создания проекта
    close_date — дата закрытия проекта
    """

    id: int
    invested_amount: int = 0
    fully_invested: bool = False
    create_date: datetime = datetime.now().strftime(settings.FORMAT_DATE_TIME)
    close_date: Optional[datetime.replace(microsecond=0)]

    class Config:
        orm_mode = True
