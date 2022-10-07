from sqlalchemy import Column, String, Text

from .abstract_common_project_donation import CommonProjectDonation


class CharityProject(CommonProjectDonation):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
