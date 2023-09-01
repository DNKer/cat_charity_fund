from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt


class DonationCreate(BaseModel):
    """
    Схема для создания пожертвования.
    Дополнительные поля и использование пустой
    модели запрещены (параметры, неописанные
    в схеме, не принимаются).
    """

    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationView(DonationCreate):
    """
    Схема для просмотра ответа объекта
    пожертвования. Cхема может принимать
    на вход объект базы данных,а не только
    Python-словарь или JSON-объект.
    """

    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDB(DonationView):
    """
    Схема со всеми данными объекта пожертвования.
    """

    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
