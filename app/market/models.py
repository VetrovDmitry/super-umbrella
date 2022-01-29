import datetime

from app.database import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship


class House(db.Model):
    __tablename__ = "house"
    id = Column(Integer, primary_key=True)
    city = Column(String)
    street = Column(String)
    house_number = Column(String)
    summary = Column(String)
    cost = Column(Float)
    user_id = Column(Integer, ForeignKey("user.id"))
    date = Column(DateTime)

    def __init__(self, city, street, house_number, cost, summary):
        self.city = city
        self.street = street
        self.house_number = house_number
        self.cost = cost
        self.summary = summary
        self.date = datetime.datetime.now()


class Photo(db.Model):
    __tablename__ = 'photo'
    id = Column(Integer, primary_key=True)
    path = Column(String)
    house_id = Column(Integer, ForeignKey('house.id'))
    date = Column(DateTime)

    def __init__(self, path, house_id):
        self.path = path
        self.house_id = house_id