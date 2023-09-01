"""Импорты класса Base и всех последующих моделей Alembic."""
from app.core.db import Base # noqa
from app.models import CharityProject # noqa
from app.models.donation import Donation # noqa
from app.models.user import User # noqa
