from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    """
    Настройки проекта.
    """

    app_title: str = 'QRKot'
    app_author: str = 'DNK'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    description: str = 'Приложение благотворительного фонда поддержки котиков.'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    TOKKEN_URL: str = 'auth/jwt/login'
    TOKKEN_LIFETIME_SEC: int = 3600
    BACKEND_NAME_UNIC: str = 'jwt'

    class Config:
        env_file = '.env'


settings = Settings()
