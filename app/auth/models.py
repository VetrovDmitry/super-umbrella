import datetime

from app.database import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from app.utils import get_image


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    username = Column(String(30), unique=True)
    email = Column(String(50))
    hash = Column(String(100))
    date_registered = Column(DateTime)
    avatars = relationship('Avatar')
    likes = relationship('Like')

    def __init__(self, worksheet):
        self.name = worksheet['name']
        self.username = worksheet['username']
        self.email = worksheet['email']
        self.hash = worksheet['hash']
        self.date_registered = worksheet['date']

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


class Avatar(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    path = Column(String)
    date_upload = Column(DateTime)

    def __init__(self, user_id, path):
        self.user_id =user_id
        self.path = path
        self.date_upload = datetime.datetime.now()