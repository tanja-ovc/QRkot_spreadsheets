from datetime import datetime
from pydantic import BaseModel, Extra, Field, PositiveInt, validator
from typing import Optional


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt
    create_date: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        schema_extra = {
            'example': {
                'name': 'Сбор на стерилизацию бездомных кошек',
                'description': 'В рамках кампании по стерилизации кошек Кошачьего района.',
                'full_amount': 34000
            }
        }


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class CharityProjectUpdate(CharityProjectBase):

    @validator('name')
    def name_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Имя проекта не может быть пустым.')
        return value
