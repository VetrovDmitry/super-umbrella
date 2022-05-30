import json
import os
from functools import wraps
from dataclasses import dataclass

STANDART_IMAGES = {
    'house': 'images/standart_photo.png',
    'profile': 'images/profile_photo.png'
}


def get_image(path, mode='house'):
    if path is None or path == '':
        return STANDART_IMAGES.get(mode)

    image = os.path.join('app/static/uploads', path)
    if os.path.isfile(image):
        return 'uploads/' + path


def read_api_config():
    with open('app/api.json', 'r') as json_file:
        data = json.load(json_file)
        return data['API_SPECIFICATIONS']


#  Auth

device_header = {'apiKeyAuth': []}
user_header = {'JWT': []}

api_key_scheme = {
    'type': 'apiKey',
    'in': 'header',
    'name': 'X-API-Key',
    'required': True
}

jwt_scheme = {
    'type': 'apiKey',
    'in': 'header',
    'name': 'JWT',
    'required': True
}


#  Errors

class UserError(Exception):
    def __init__(self, message="problems with user", code=400):
        self.message = message
        self.code = code


@dataclass
class DeviceError(Exception):
    message: str = 'problems with device'
    code: int = 400


#  Handlers

def error_handler(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except UserError as err:
            return {'error': err.message}, err.code
        except DeviceError as err:
            return {'error': err.message}, err.code
        except Exception as error:
            return {'error': error}, 500

    return decorated_view
