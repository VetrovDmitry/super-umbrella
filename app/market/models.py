import datetime
import enum

from app.database import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.utils import get_image


class House(db.Model):
    __tablename__ = "house"
    id = Column(Integer, primary_key=True)
    city = Column(String)
    street = Column(String)
    house_number = Column(String)
    summary = Column(String)
    cost = Column(Float)
    user_id = Column(Integer, ForeignKey("user.id"))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    photos = relationship('Photo', back_populates="house", uselist=True)
    likes = relationship('Like')

    def __init__(self, city: str, street: str, house_number: str, cost: float, summary: str, user_id: int):
        self.city = city
        self.street = street
        self.house_number = house_number
        self.cost = cost
        self.summary = summary
        self.user_id = user_id
        self.date = datetime.datetime.now()

    def update(self):
        db.session.commit()

    def upload(self):
        db.session.add(self)
        self.update()

    def delete(self):
        db.session.delete(self)
        self.update()

    def get_likes_count(self):
        return len(self.likes)

    def get_cost(self):
        if self.cost is None:
            return 0
        return self.cost

    def get_summary(self):
        if self.summary is None:
            return ''
        return self.summary

    @property
    def public_json(self):
        return {
            'id': self.id,
            'city': self.city,
            'street': self.street,
            'house_number': self.house_number,
            'summary': self.get_summary(),
            'cost': self.get_cost(),
            'user_id': self.user_id,
            'time_created': self.time_created.isoformat()
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

    @classmethod
    def find_by_id(cls, _id: int):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_query(cls, city: str, street: str, house_number: str, cost: int):
        return cls.query.filter(
            cls.city.ilike(f"{city}%"),
            cls.street.ilike(f"{street}%"),
            cls.house_number.ilike(f"{house_number}%")
        ).filter_by(cost=cost).all()


class PhotoTypes(enum.Enum):
    PNG = 'png'
    JPG = 'jpg'
    JPEG = 'jpeg'

    @classmethod
    def values(cls) -> list:
        return [cls.PNG.value, cls.JPG.value, cls.JPEG.value]


class Photo(db.Model):
    __tablename__ = 'photo'
    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False, unique=True)
    file_type = Column(Enum(PhotoTypes), nullable=False)
    file_id = Column(String, unique=True, nullable=False)
    url = Column(String, nullable=False)
    house_id = Column(Integer, ForeignKey('house.id'))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    house = relationship("House", back_populates="photos", uselist=False)

    def __init__(self, house_id: int, filename: str, file_type: enumerate, file_id: str, url: str) -> None:
        self.house_id = house_id
        self.filename = filename
        self.file_type = PhotoTypes(file_type)
        self.file_id = file_id
        self.url = url


class Like(db.Model):
    __tablename__ = 'likes'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    house_id = Column(Integer, ForeignKey('house.id'))

    def __init__(self, user_id, house_id):
        self.user_id = user_id
        self.house_id = house_id