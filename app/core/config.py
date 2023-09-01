from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = 'QRKot'
    app_author: str
    database_url: str
    path: str
    secret: str = 'SECRET'
    description: str = 'Приложение благотворительного фонда поддержки котиков.'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    FORMAT_DATE_TIME: str = '%d-%m-%Y %H:%M:%S'

    class Config:
        env_file = '.env'


settings = Settings()
