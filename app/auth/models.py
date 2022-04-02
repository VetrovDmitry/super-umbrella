from app.database import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin


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


class Avatar(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    path = Column(String)
    date_upload = Column(DateTime)