from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import donation_crud
from app.models import User
from app.services.investments import (
    investment_donation_create,
)
from app.schemas import (
    DonationCreate, DonationDBFull, DonationDBShort
)

router = APIRouter()


@router.post(
    '/',
    response_model=DonationDBShort,
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)],
)
async def create_new_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """Только для зарегистрированных пользователей."""

    new_donation = await donation_crud.create(
        donation, session, user
    )
    new_donation_upd = await investment_donation_create(new_donation, session)
    return new_donation_upd


@router.get(
    '/',
    response_model=List[DonationDBFull],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    """Только для суперпользователей."""
    donations_list = await donation_crud.get_multi(session)
    return donations_list


@router.get(
    '/my',
    response_model=List[DonationDBShort],
)
async def get_my_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """Получает список всех пожертвований для текущего пользователя."""
    reservations = await donation_crud.get_by_user(
        session=session, user=user
    )
    return reservations
