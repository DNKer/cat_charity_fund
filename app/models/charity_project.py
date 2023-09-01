from sqlalchemy import Column, String, Text

from app.core.db import Base


class CharityProject(Base):
    """Модель `Благотворительный проект`."""

    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return (
            f'{self.name}. Собрано: {self.invested_amount}/{self.full_amount}'
        )
