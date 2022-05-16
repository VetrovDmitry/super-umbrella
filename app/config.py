from dotenv import load_dotenv
from os import environ


load_dotenv()


class Config:
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = environ['SECRET_KEY']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = environ['JWT_SECRET_KEY']


class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = environ['DB_DEV']
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = environ['DB_TEST']
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(Config):
    ENV = 'production'
    SQLALCHEMY_DATABASE_URI = environ['DB_PROD']
