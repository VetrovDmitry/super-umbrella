import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from flask_login import UserMixin

from utils import get_image
from database import db


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    username = Column(String(30), unique=True)
    email = Column(String(50))
    hash = Column(String(100))
    date_registered = Column(DateTime(timezone=True), server_default=func.now())

    member = relationship('Member', back_populates='user', uselist=False)

    def __init__(self, name: str, username: str, email: str, password: str):
        self.name = name
        self.username = username
        self.email = email
        self.hash = self.create_hash(password)

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

    @staticmethod
    def create_hash(password: str) -> str:
        return generate_password_hash(password, method='sha256')

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.hash, password)

    @property
    def min_info(self):
        return {
            "name": self.name,
            "email": self.email,
            "username": self.username,
            "date": self.date_registered.date(),
            "preview": self.get_preview_avatar()
        }

    @property
    def public_json(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'date_registered': self.date_registered.isoformat(),
            'username': self.username
        }

    @classmethod
    def find_by_username(cls, username: str):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()


class Avatar(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    path = Column(String)
    date_upload = Column(DateTime)

    def __init__(self, user_id, path):
        self.user_id =user_id
        self.path = path
        self.date_upload = datetime.datetime.now()