from sqlalchemy import (Column, Integer, String, DateTime, Enum,  ForeignKey, Date)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import datetime
import enum

from database import db


class HumanGenders(enum.Enum):
    MALE = 'Male'
    FEMALE = 'Female'


class Member(db.Model):
    __tablename__ = 'member'
    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    birth_date = Column(Date, nullable=False)
    sex = Column(Enum(HumanGenders))

    user = relationship('User', back_populates='member', uselist=False)

    def __init__(self, user_id: int, birth_date: datetime.date, sex: HumanGenders):
        self.id = user_id
        self.birth_date = birth_date
        self.sex = HumanGenders(sex)

    @property
    def username(self) -> str:
        return self.user.username

    @property
    def name(self) -> str:
        return self.user.name

    @property
    def email(self) -> str:
        return self.user.email

    @property
    def json(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'email': self.email,
            'sex': self.sex.value,
            'birth_date': self.birth_date.isoformat()
        }