from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta, datetime, timezone
import datetime, time
from functools import wraps
from flask import request

from . import models

from main.models import Member
from database import db
from utils import DeviceError



UPLOAD_DIR = 'app/static/uploads/'
SECOND_PATH = 'static/uploads/'


class UserController:
    def __init__(self):
        self.model = models.User

    def check_username_exists(self, username: str) -> dict:
        if self.model.find_by_username(username):
            return {'status': True, 'output': 'username: %s exists' % username}
        else:
            return {'status': False, 'output': 'username: %s does not exist' % username}

    def check_email_exists(self, email: str) -> dict:
        if self.model.find_by_email(email):
            return {'status': True, 'output': 'email: %s exists' % email}
        else:
            return {'status': False, 'output': 'email: %s does not exist' % email}

    def check_user_exists(self, user_id: int) -> dict:
        if self.model.find_by_id(user_id):
            return {'status': True, 'output': 'user_id: %s exists' % user_id}
        else:
            return {'status': False, 'output': 'user_id: %s does not exist' % user_id}

    def check_user_login(self, username: str, password: str) -> dict:
        username_checking = self.check_username_exists(username)
        if not username_checking['status']:
            return {'status': False, 'output': username_checking['output']}

        user = self.model.find_by_username(username)
        if not user.check_password(password):
            return {'status': False, 'output': 'wrong password'}

        return {'status': True, 'output': 'everything is right'}

    def __new_user(self, name: str, username: str, email: str, password: str) -> int:
        new_user = self.model(name=name,
                              username=username,
                              email=email,
                              password=password)
        db.session.add(new_user)
        db.session.commit()
        return new_user.id

    def __new_member(self, user_id: int, sex: str, birth_date: datetime.date) -> int:
        new_member = Member(user_id, birth_date, sex)
        db.session.add(new_member)
        db.session.commit()
        return new_member.id

    def create_user(self, user_data: dict) -> dict:
        new_user_id = self.__new_user(
            name=user_data['name'],
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password']
        )
        return {'message': 'user %s was created' % new_user_id}

    def signup(self, user_data: dict) -> dict:
        new_user_id = self.__new_user(
            name=user_data['name'],
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password']
        )

        new_member_id = self.__new_member(
            user_id=new_user_id,
            sex=user_data['sex'],
            birth_date=user_data['birth_date']
        )

        return {'message': 'member %s signed up' % new_member_id}

    def get_user_public_info(self, user_id: int) -> dict:
        return self.model.find_by_id(user_id).public_json

    def get_users_public_info(self) -> dict:
        users_info = list()
        users = self.model.find_all()
        for user in users:
            users_info.append(user.public_json)
        return {'users': users_info}

    @staticmethod
    def create_token(username: str, expires=30) -> dict:
        token = create_access_token(identity=username, expires_delta=timedelta(minutes=expires))
        return {'access_token': token}


class OAuthController(UserController):
    models = {
        "device": models.Device,
        "token": models.Token
    }
    tz = timezone(timedelta(0))

    #  Checks

    @classmethod
    def check_device_key(cls, key: str) -> dict:
        if cls.models['device'].find_by_key(key):
            return {'status': True, 'output': f'api_key: {key[:10]}... exists'}
        return {'status': False, 'output': f'api_key: {key[:10]}... does not exist'}

    @classmethod
    def check_device_name_exists(cls, name: str) -> dict:
        if cls.models['device'].find_by_name(name):
            return {'status': True, 'output': f'device_name: {name} exists'}
        return {'status': False, 'output': f'device_name: {name} does not exist'}

    @classmethod
    def check_user_token_exists(cls, user_id: int) -> dict:
        if cls.models['token'].find_by_user_id(user_id):
            return {'status': True, 'output': f'user_id: {user_id} already has token'}
        return {'status': False, 'output': f'user_id: {user_id} does not have a token'}

    #  Create

    @classmethod
    def create_device(cls, user_id: int, name: str) -> dict:
        device = cls.models['device'](
            name=name,
            user_id=user_id
        )
        device.upload()
        return device.info

    @classmethod
    def add_device_request(cls, device_key: str):
        device = cls.models['device'].find_by_key(device_key)
        device.add_request()

    @classmethod
    def api_required(cls, func):
        @wraps(func)
        def decorator(*args, **kwargs):
            headers = request.headers
            if not headers:
                raise DeviceError('there is no headers', 400)

            api_key = headers.get('X-Api-key', None)
            if not api_key:
                raise DeviceError('there is no api-key', 400)

            key_checking = cls.check_device_key(api_key)
            if not key_checking['status']:
                raise DeviceError(key_checking['output'], 401)

            cls.add_device_request(api_key)

            return func(*args, **kwargs)

        return decorator