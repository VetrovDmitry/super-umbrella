from app.database import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class Member(db.Model):
    __tablename__ = 'member'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    memberships = relationship('Membership')
    messages = relationship('Message')


class Membership(db.Model):
    __tablename__ = "membership"
    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey("member.id"))
    room_id = Column(Integer, ForeignKey("room.id"))
    date = Column(DateTime)


class Room(db.Model):
    __tablename__ = "room"
    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey("member.id"))
    title = Column(String(50))
    details = Column(String(150))
    date = Column(DateTime)
    messages = relationship('Message')
    memberships = relationship("Membership")


class Message(db.Model):
    __tablename__ = "message"
    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey("member.id"))
    room_id = Column(Integer, ForeignKey("room.id"))
    content = Column(String)
    date = Column(DateTime)