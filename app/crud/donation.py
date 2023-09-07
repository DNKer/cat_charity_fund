from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):

    async def get_user_donations(
            self, session: AsyncSession, user: User
    ) -> Optional[Donation]:
        """Получение всех пожертвований пользователя."""
        select_user = select(Donation).where(
            Donation.user_id == user.id,
        )
        donations = await session.execute(select_user)
        result = donations.scalars().all()
        return result


donation_crud = CRUDDonation(Donation)
