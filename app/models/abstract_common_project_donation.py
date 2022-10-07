from sqlalchemy import Boolean, Column, DateTime, Integer

from app.core.db import Base


class CommonProjectDonation(Base):
    __abstract__ = True
    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime)
    close_date = Column(DateTime)
