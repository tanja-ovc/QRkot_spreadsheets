from datetime import datetime

import sqlalchemy as sa
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.models import CharityProject, Donation
from app.schemas import (
    CharityProjectCreate, DonationCreate,
)


async def investment_donation_create(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
):
    projects_from_oldest = await session.execute(
        select(CharityProject).where(
            CharityProject.close_date == sa.null()).order_by('create_date')
    )
    projects_from_oldest = projects_from_oldest.scalars().all()

    if not projects_from_oldest:
        return donation

    donation_full_amount = True
    for project in projects_from_oldest:

        money_needed = project.full_amount - project.invested_amount

        if donation_full_amount:
            money_received = donation.full_amount

        if money_received < money_needed:
            project.invested_amount += money_received
            donation.invested_amount += money_received
            donation.fully_invested = True
            donation.close_date = datetime.utcnow()
            break

        elif money_received == money_needed:
            project.invested_amount += money_needed
            project.fully_invested = True
            project.close_date = datetime.utcnow()
            donation.invested_amount += money_needed
            donation.fully_invested = True
            donation.close_date = datetime.utcnow()
            break

        elif money_received > money_needed:
            project.invested_amount += money_needed
            project.fully_invested = True
            project.close_date = datetime.utcnow()
            donation.invested_amount += money_needed
            money_received -= money_needed
            donation_full_amount = False

    session.add(project)
    session.add(donation)
    await session.commit()
    await session.refresh(project)
    await session.refresh(donation)

    return donation


async def investment_project_create(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    unused_donations = await session.execute(
        select(Donation).where(
            Donation.close_date == sa.null()).order_by('create_date')
    )
    unused_donations = unused_donations.scalars().all()

    if not unused_donations:
        return project

    zero_money_in_project = True
    for donation in unused_donations:

        unused_leftover = donation.full_amount - donation.invested_amount

        if zero_money_in_project:
            money_needed = project.full_amount - project.invested_amount

        if unused_leftover < money_needed:
            project.invested_amount += unused_leftover
            donation.invested_amount += unused_leftover
            donation.fully_invested = True
            donation.close_date = datetime.utcnow()
            money_needed -= unused_leftover
            zero_money_in_project = False

        elif unused_leftover == money_needed:
            project.invested_amount += unused_leftover
            project.fully_invested = True
            project.close_date = datetime.utcnow()
            donation.invested_amount += unused_leftover
            donation.fully_invested = True
            donation.close_date = datetime.utcnow()
            break

        elif unused_leftover > money_needed:
            project.invested_amount += money_needed
            project.fully_invested = True
            project.close_date = datetime.utcnow()
            donation.invested_amount += money_needed
            break

    session.add(project)
    session.add(donation)
    await session.commit()
    await session.refresh(project)
    await session.refresh(donation)

    return project
