from sqlalchemy import Column, Integer, ForeignKey, Text

from .base import Base


class Donation(Base):
    """Модель `Пожертвование`."""

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    comment = Column(Text, nullable=True)

    def __repr__(self):
        return (
            f'№{self.id}. Вложено: {self.invested_amount}/{self.full_amount}'
        )
