from typing import List

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import (
    current_superuser,
    current_user
)
from app.crud.chartity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import User
from app.services.investment import investment
from app.schemas.donation import (
    DonationCreate,
    DonationDB,
    DonationView
)

router = APIRouter()


@router.post(
    '/',
    response_model=DonationView,
    response_model_exclude_none=True,
    description='Создание `пожертвования.`',
)
async def create_donation(
        reservation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """Создание `пожертвования`. Текущий пользователь."""
    new_donation = await donation_crud.create(
        reservation, session, user
    )
    await investment(new_donation, charity_project_crud, session)
    return new_donation


@router.get(
    '/',
    response_model=List[DonationDB],
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,
    description='Получить список всех `пожертвований`.'
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """Получить список всех `пожертвований`. Только для суперпользователей."""
    return await donation_crud.get_multi(session)


@router.get(
    '/my',
    response_model=List[DonationView],
    response_model_exclude_none=True,
    description='Получить список всех моих `пожертвований`.'
)
async def get_my_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """Получить список `пожертвований`. Текущий пользователь."""
    return await donation_crud.get_user_donations(
        session=session, user=user
    )
