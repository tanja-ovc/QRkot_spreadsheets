from datetime import datetime
from pydantic import BaseModel, Field, PositiveInt
from typing import Optional


class DonationCreate(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]
    create_date: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        schema_extra = {
            'example': {
                'full_amount': 14300,
                'comment': 'От Васи Пупкина.'
            }
        }


class DonationDBShort(DonationCreate):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDBFull(DonationDBShort):
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
