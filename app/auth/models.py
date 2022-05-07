import datetime

from app.database import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from flask_login import UserMixin
from app.utils import get_image


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    username = Column(String(30), unique=True)
    email = Column(String(50))
    hash = Column(String(100))
    date_registered = Column(DateTime(timezone=True), server_default=func.now())
    avatars = relationship('Avatar')
    likes = relationship('Like')

    def __init__(self, name: str, username: str, email: str, hash: str):
        self.name = name
        self.username = username
        self.email = email
        self.hash = hash

    def get_photos(self):
        photos = list()
        for photo in self.avatars:
            photos.append(photo.path)
        return photos

    def get_preview_avatar(self):
        if len(self.avatars) == 0:
            return get_image(None, 'profile')
        else:
            return get_image(self.get_photos()[-1], 'profile')

    @property
    def min_info(self):
        return {
            "name": self.name,
            "email": self.email,
            "username": self.username,
            "date": self.date_registered.date(),
            "preview": self.get_preview_avatar()
        }

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def check_exists_by_username(cls, username) -> bool:
        if cls.find_by_username(username):
            return True
        else:
            return False

    @classmethod
    def check_exists_by_email(cls, email) -> bool:
        if cls.find_by_email(email):
            return True
        else:
            return False


class Avatar(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    path = Column(String)
    date_upload = Column(DateTime)

    def __init__(self, user_id, path):
        self.user_id =user_id
        self.path = path
        self.date_upload = datetime.datetime.now()