from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_meeting_room_exists, check_name_duplicate
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.meeting_room import meeting_room_crud
from app.crud.reservation import reservation_crud
# Импортируем модель, чтобы указать её в аннотации.
from app.schemas.meeting_room import (
    MeetingRoomCreate, MeetingRoomDB, MeetingRoomUpdate
)
from app.schemas.reservation import ReservationDB


router = APIRouter()


@router.post(
    '/',
    # Указываем схему ответа.
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    description='Создание новой `переговорки.`',
)
async def create_new_meeting_room(
        meeting_room: MeetingRoomCreate,
        # Указываем зависимость, предоставляющую объект сессии,
        # как параметр функции.
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    # Выносим проверку дубликата имени в отдельную корутину.
    # Если такое имя уже существует, то будет вызвана ошибка HTTPException
    # и обработка запроса остановится.
    await check_name_duplicate(meeting_room.name, session)
    new_room = await meeting_room_crud.create(meeting_room, session)
    return new_room


@router.get(
    '/',
    response_model=list[MeetingRoomDB],
    response_model_exclude_none=True,
    description='Получить список всех `переговорок.`'
)
async def get_all_meeting_rooms(
    session: AsyncSession = Depends(get_async_session),
):
    all_rooms = await meeting_room_crud.get_multi(session)
    return all_rooms


@router.patch(
    # ID обновляемого объекта будет передаваться path-параметром.
    '/{meeting_room_id}',
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    description='Изменить `переговороку`'
)
async def partially_update_meeting_room(
        # ID обновляемого объекта.
        meeting_room_id: int,
        # JSON-данные, отправленные пользователем.
        obj_in: MeetingRoomUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    # Выносим повторяющийся код в отдельную корутину.
    meeting_room = await check_meeting_room_exists(
        meeting_room_id, session
    )

    if obj_in.name is not None:
        # Если в запросе получено поле name — проверяем его на уникальность.
        await check_name_duplicate(obj_in.name, session)

    # Передаём в корутину все необходимые для обновления данные.
    meeting_room = await meeting_room_crud.update(
        meeting_room, obj_in, session
    )
    return meeting_room


@router.delete(
    '/{meeting_room_id}',
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    description='Удалить `переговороку.`'
)
async def remove_meeting_room(
        meeting_room_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    # Выносим повторяющийся код в отдельную корутину.
    meeting_room = await check_meeting_room_exists(
        meeting_room_id, session
    )
    meeting_room = await meeting_room_crud.remove(meeting_room, session)
    return meeting_room


@router.delete(
    '/{meeting_room_id}/reservations',
    response_model=ReservationDB,
    # Добавляем множество с полями, которые надо исключить из ответа.
    response_model_exclude={'user_id'},
    description='Удалить бронь `переговороки.`'
)
async def get_reservations_for_room(
        meeting_room_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    await check_meeting_room_exists(meeting_room_id, session)
    reservations = await reservation_crud.get_future_reservations_for_room(
        room_id=meeting_room_id, session=session
    )
    return reservations