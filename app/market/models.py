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
    photos = relationship('Photo')

    def __init__(self, city, street, house_number, user_id):
        self.city = city
        self.street = street
        self.house_number = house_number
        self.user_id = user_id
        self.date = datetime.datetime.now()

    def get_cost(self):
        if self.cost is None:
            return 'Cost'
        return str(self.cost)

    def get_summary(self):
        if self.summary is None:
            return 'Summary'
        return self.summary

    def get_min_info(self):
        return {
            'id': self.id,
            'city': self.city,
            'street': self.street,
            'house_number': self.house_number,
            'summary': self.get_summary(),
            'cost': self.get_cost()
        }

    def get_max_info(self):
        return {
            'id': self.id,
            'cost': self.cost,
            "summary": self.summary,
            "city": self.city,
            "street": self.street,
            "house_number": self.house_number,
            'photos': self.photos
        }


class Photo(db.Model):
    __tablename__ = 'photo'
    id = Column(Integer, primary_key=True)
    path = Column(String)
    house_id = Column(Integer, ForeignKey('house.id'))
    date = Column(DateTime)

    def __init__(self, path, house_id):
        self.path = path
        self.house_id = house_id