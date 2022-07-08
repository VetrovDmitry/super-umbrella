from sqlalchemy import (Column, Integer, String, DateTime, Enum,  ForeignKey, Date)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import datetime
import enum

from app.database import db


class HumanGenders(enum.Enum):
    MALE = 'Male'
    FEMALE = 'Female'


class Member(db.Model):
    __tablename__ = 'member'
    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    birth_date = Column(Date, nullable=False)
    sex = Column(Enum(HumanGenders))

    user = relationship('User', back_populates='member', uselist=False)
    objects = relationship('Object', back_populates='member', uselist=True)

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


class DataTypes(enum.Enum):
    PNG = 'png'
    JPG = 'jpg'
    JPEG = 'jpeg'

    @classmethod
    def get_images_types(cls):
        return [cls.PNG.value, cls.JPG.value, cls.JPEG.value]


class Object(db.Model):
    __tablename__ = 'object'
    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey('member.id'), nullable=False)
    file_name = Column(String, nullable=False, unique=True)
    file_type = Column(Enum(DataTypes), nullable=False)
    file_id = Column(String, unique=True, nullable=False)
    url = Column(String, nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    member = relationship('Member', back_populates='objects', uselist=False)

    def __init__(self, member_id: int, file_type: enumerate, url: str,
                 file_id: str, file_name: str) -> None:
        self.member_id = member_id
        self.file_name = file_name
        self.file_type = DataTypes(file_type)
        self.url = url
        self.file_id = file_id

    def update(self):
        db.session.commit()
        return self

    def upload(self):
        db.session.add(self)
        return self.update()

    def delete(self):
        db.session.delete(self)
        self.upload()
        return
