import datetime

from database import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship

from utils import get_image


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
    likes = relationship('Like')

    def __init__(self, city, street, house_number, user_id):
        self.city = city
        self.street = street
        self.house_number = house_number
        self.user_id = user_id
        self.date = datetime.datetime.now()

    def get_likes_count(self):
        return len(self.likes)

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
            'cost': self.get_cost(),
            'preview': self.get_preview_photo(),
            'likes_count': self.get_likes_count()
        }

    def get_max_info(self):
        return {
            'id': self.id,
            'cost': self.cost,
            "summary": self.summary,
            "city": self.city,
            "street": self.street,
            "house_number": self.house_number,
            'photos': self.get_photos()
        }

    def get_photos(self):
        photos = list()
        for photo in self.photos:
            photos.append(photo.path)
        return photos

    def get_preview_photo(self):
        if len(self.photos) == 0:
            return get_image(None, 'house')
        else:
            return get_image(self.get_photos()[-1], 'house')


class Photo(db.Model):
    __tablename__ = 'photo'
    id = Column(Integer, primary_key=True)
    path = Column(String)
    house_id = Column(Integer, ForeignKey('house.id'))
    date = Column(DateTime)

    def __init__(self, path, house_id):
        self.path = path
        self.house_id = house_id
        self.date = datetime.datetime.now()


class Like(db.Model):
    __tablename__ = 'likes'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    house_id = Column(Integer, ForeignKey('house.id'))

    def __init__(self, user_id, house_id):
        self.user_id = user_id
        self.house_id = house_id