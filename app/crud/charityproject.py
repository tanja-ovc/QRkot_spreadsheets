from typing import Optional

from sqlalchemy import extract, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_charityproject_id_by_name(
            self,
            charityproject_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        charityproject_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == charityproject_name
            )
        )
        db_charityproject_id = charityproject_id.scalars().first()
        return db_charityproject_id

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ) -> list[dict[str, str]]:
        projects = await session.execute(
            select(
                [CharityProject.name,
                 CharityProject.close_date,
                 CharityProject.create_date,
                 CharityProject.description]
            ).where(
                CharityProject.fully_invested == 1
            ).order_by(
                extract('year', self.model.close_date) -
                extract('year', self.model.create_date),
                extract('month', self.model.close_date) -
                extract('month', self.model.create_date),
                extract('day', self.model.close_date) -
                extract('day', self.model.create_date),
                extract('hour', self.model.close_date) -
                extract('hour', self.model.create_date),
                extract('minute', self.model.close_date) -
                extract('minute', self.model.create_date),
                extract('second', self.model.close_date) -
                extract('second', self.model.create_date),
            )
        )
        projects = projects.all()
        return projects


charityproject_crud = CRUDCharityProject(CharityProject)
