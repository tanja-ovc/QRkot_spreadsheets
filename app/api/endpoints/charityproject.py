from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charityproject_not_closed,
    check_charityproject_exists,
    check_charityproject_investment_exists,
    check_full_amount_not_less_than_invested,
    check_name_duplicate
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import charityproject_crud
from app.services.investments import investment_project_create
from app.schemas import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
)

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charityproject(
        charityproject: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    await check_name_duplicate(charityproject.name, session)
    new_charityproject = await charityproject_crud.create(charityproject, session)
    new_charityproject_upd = await investment_project_create(
        new_charityproject, session
    )
    return new_charityproject_upd


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charityprojects(
    session: AsyncSession = Depends(get_async_session)
):
    charityprojects_list = await charityproject_crud.get_multi(session)
    return charityprojects_list


@router.delete(
    '/{charityproject_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_charityproject(
        charityproject_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    charityproject_db = await check_charityproject_exists(
        charityproject_id, session
    )
    await check_charityproject_investment_exists(charityproject_db)
    await check_charityproject_not_closed(charityproject_db)
    charityproject = await charityproject_crud.remove(
        charityproject_db, session
    )
    return charityproject


@router.patch(
    '/{charityproject_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charityproject(
        charityproject_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    charityproject_db = await check_charityproject_exists(
        charityproject_id, session
    )
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    await check_charityproject_not_closed(charityproject_db)
    await check_full_amount_not_less_than_invested(charityproject_db, obj_in)
    charityproject = await charityproject_crud.update(
        charityproject_db, obj_in, session
    )
    return charityproject
