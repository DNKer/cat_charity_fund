import logging
import os
import sys
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseSettings, EmailStr


load_dotenv()


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
    MAX_LENGHT_PASSWORD: int = 3

    logging.basicConfig(
        level=logging.INFO,
        handlers=[
            logging.FileHandler(
                os.path.abspath('cat_charity_fund.log'), mode='a', encoding='UTF-8'),
            logging.StreamHandler(stream=sys.stdout)],
        format='%(asctime)s, %(levelname)s, %(message)s,'
               '%(name)s, %(message)s,', datefmt='%d-%m-%Y %H-%M',
    )

    class Config:
        env_file = '.env'


settings = Settings()
