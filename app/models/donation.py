from sqlalchemy import Column, ForeignKey, Integer, Text

from .abstract_common_project_donation import CommonProjectDonation


class Donation(CommonProjectDonation):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
