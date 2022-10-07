from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import charityproject_crud
from app.models import CharityProject
from app.schemas import CharityProjectUpdate


async def check_charityproject_exists(
        charityproject_id: int,
        session: AsyncSession,
) -> CharityProject:
    charityproject_db = await charityproject_crud.get(
        charityproject_id, session
    )
    if charityproject_db is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден.'
        )
    return charityproject_db


async def check_charityproject_investment_exists(
        charityproject_db: CharityProject,
) -> None:
    if charityproject_db.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!'
        )


async def check_name_duplicate(
        charityproject_name: str,
        session: AsyncSession,
) -> None:
    project_id = await charityproject_crud.get_charityproject_id_by_name(
        charityproject_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!',
        )


async def check_charityproject_not_closed(
    charityproject_db: CharityProject,
) -> None:
    if charityproject_db.close_date is not None:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!'
        )


async def check_full_amount_not_less_than_invested(
    charityproject_db: CharityProject,
    update_info: CharityProjectUpdate,
) -> None:
    db_invested_amount = charityproject_db.invested_amount
    new_full_amount = update_info.full_amount
    if new_full_amount and new_full_amount < db_invested_amount:
        raise HTTPException(
            status_code=422,
            detail='Сумма, требующаяся для проекта, не может стать меньше '
                   'уже вложенной в проект.'
        )
