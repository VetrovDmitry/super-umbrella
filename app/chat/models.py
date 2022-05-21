import datetime

from database import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class Membership(db.Model):
    __tablename__ = "membership"
    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey("member.id"))
    room_id = Column(Integer, ForeignKey("room.id"))
    date = Column(DateTime)

    def __init__(self, member_id, room_id):
        self.room_id= room_id
        self.member_id = member_id
        self.date = datetime.datetime.now()


class Room(db.Model):
    __tablename__ = "room"
    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey("member.id"))
    title = Column(String(50))
    details = Column(String(150))
    date = Column(DateTime)
    messages = relationship('Message')
    memberships = relationship("Membership")

    def __init__(self, member_id, title, details):
        self.member_id = member_id
        self.title = title
        self.details = details
        self.date = datetime.datetime.now()

    def get_min_info(self):
        return {
            'id': self.id,
            'title': self.title,
            'details': self.details,
            'date': self.date
        }


class Message(db.Model):
    __tablename__ = "message"
    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey("member.id"))
    room_id = Column(Integer, ForeignKey("room.id"))
    content = Column(String)
    date = Column(DateTime)

    def __init__(self, member_id, content, room_id):
        self.member_id = member_id
        self.content = content
        self.room_id = room_id
        self.date = datetime.datetime.now()