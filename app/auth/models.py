from datetime import datetime, timedelta, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from flask_login import UserMixin
from uuid import uuid4

from utils import get_image
from database import db


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    username = Column(String(30), unique=True)
    email = Column(String(50))
    hash = Column(String(100))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    member = relationship('Member', back_populates='user', uselist=False)
    device = relationship("Device", back_populates='user', uselist=True)
    tokens = relationship('Token', back_populates='user', uselist=False)

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
            "date": self.time_created.date(),
            "preview": self.get_preview_avatar()
        }

    @property
    def public_json(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'date_registered': self.time_created.isoformat(),
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


class Device(db.Model):
    __tablename__ = "device"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False, unique=True)
    key = Column(String(80), unique=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    requests = Column(Integer, default=0)

    user = relationship("User", back_populates='device', uselist=False)

    def __init__(self, name: str, user_id: int):
        self.name = name
        self.user_id = user_id
        self.key = uuid4().hex

    def update(self):
        db.session.commit()

    def upload(self):
        db.session.add(self)
        self.update()

    def delete(self):
        db.session.delete(self)
        self.update()

    def add_request(self):
        self.requests += 1
        self.update()

    @property
    def info(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "user_id": self.user_id,
            "key": self.key
        }

    @classmethod
    def find_by_name(cls, name: str):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_key(cls, key: str):
        return cls.query.filter_by(key=key).first()

    @classmethod
    def find_by_id(cls, _id: int):
        return cls.query.filter_by(id=_id).first()


class Token(db.Model):
    __tablename__ = 'token'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    access_token = Column(String, unique=True)
    expires = Column(DateTime(timezone=True))

    user = relationship("User", back_populates='tokens', uselist=False)

    def __init__(self, user_id: int, token: str, expires: datetime):
        self.user_id = user_id
        self.access_token = token
        self.expires = expires

    def update(self):
        db.session.commit()
        return self

    def upload(self):
        db.session.add(self)
        return self.update()

    def delete(self):
        db.session.delete(self)
        self.update()
        return

    def update_data(self, token: str, expires: datetime):
        self.access_token = token
        self.expires = expires
        return self.update()

    @classmethod
    def find_by_token(cls, token: str):
        return cls.query.filter_by(access_token=token).first()

    @classmethod
    def find_by_user_id(cls, user_id: int):
        return cls.query.filter_by(user_id=user_id).first()