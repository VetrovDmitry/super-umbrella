from flask_restful import Resource
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource

from . import controllers
from . import schemas
from utils import UserError, DeviceError, error_handler, device_header


api_required = controllers.OAuthController.api_required


ADMIN = 'Admin operations'


class CreateDeviceApi(MethodResource):
    __controller = controllers.OAuthController()
    __schemas = {
        'request': schemas.NewDeviceSchema,
        'output': schemas.DeviceSchema
    }

    @doc(tags=[ADMIN],
         summary='uploads new Device entity',
         description='Receives Device info')
    @use_kwargs(__schemas['request'])
    @marshal_with(__schemas['output'], code=201)
    def post(self, **device_data):

        name_checking = self.__controller.check_device_name_exists(device_data['name'])
        if name_checking['status']:
            raise DeviceError(name_checking['output'], 409)

        result = self.__controller.create_device(device_data['user_id'], device_data['name'])
        output = self.__schemas['output']().load(result)

        return output, 201


USER = 'User operations'


class UserApi(MethodResource):
    __controller = controllers.UserController()
    __schemas = {
        'request': schemas.NewUserSchema,
        'output': schemas.OutputSchema
    }
    decorators = [api_required,
                  error_handler]

    @doc(tags=[USER],
         summary='uploads new User',
         description='Receives minimal personal User info',
         security=[device_header])
    @use_kwargs(__schemas['request'])
    @marshal_with(__schemas['output'])
    def post(self, **user_data):

        username_checking = self.__controller.check_username_exists(user_data['username'])
        if username_checking['status']:
            raise UserError(username_checking['output'], 409)

        email_checking = self.__controller.check_email_exists(user_data['email'])
        if email_checking['status']:
            raise UserError(email_checking['output'], 409)

        result = self.__controller.create_user(user_data)
        output = self.__schemas['output']().load(result)
        return output, 201


class UserSettingsApi(MethodResource):
    __controller = controllers.UserController()
    __schemas = {
        'response': schemas.PublicUserSchema,
        'output': schemas.OutputSchema
    }
    decorators = [
        api_required,
        error_handler
    ]

    @doc(tags=[USER],
         summary='returns User entity by id',
         desription='Receives user id',
         security=[device_header])
    @marshal_with(__schemas['response'])
    def get(self, user_id: int) -> tuple:
        user_checking = self.__controller.check_user_exists(user_id)
        if not user_checking['status']:
            raise UserError(user_checking['output'], 404)

        result = self.__controller.get_user_public_info(user_id)
        response = self.__schemas['response']().load(data=result)
        return response


class UsersApi(MethodResource):
    __controller = controllers.UserController()
    __schemas = {
        'response': schemas.PublicUsersSchema
    }
    decorators = [
        api_required,
        error_handler
    ]

    @doc(tags=[USER],
         summary='returns list of User entities',
         desription='...',
         security=[device_header])
    @marshal_with(__schemas['response'])
    def get(self):
        result = self.__controller.get_users_public_info()
        response = self.__schemas['response']().load(data=result)
        return response


AUTH = 'Authentication operations'


class SignupApi(MethodResource):
    __controller = controllers.UserController()
    __schemas = {
        'request': schemas.SignupSchema,
        'output': schemas.OutputSchema
    }
    decorators = [api_required,
                  error_handler]

    @doc(tags=[AUTH],
         summary='uploads new User with Member',
         description='Receives full User information',
         security=[device_header])
    @use_kwargs(__schemas['request'])
    @marshal_with(__schemas['output'])
    def post(self, **user_data):
        username_checking = self.__controller.check_username_exists(user_data['username'])
        if username_checking['status']:
            raise UserError(username_checking['output'], 409)

        email_checking = self.__controller.check_email_exists(user_data['email'])
        if email_checking['status']:
            raise UserError(email_checking['output'], 409)

        result = self.__controller.signup(user_data)
        output = self.__schemas['output']().load(data=result)
        return output, 201


class TokenApi(MethodResource):
    __controller = controllers.UserController()
    __schemas = {
        'request': schemas.LoginSchema,
        'output': schemas.TokenSchema
    }
    decorators = [api_required,
                  error_handler]

    @doc(tags=[AUTH],
         summary='creates authorization token',
         description='Receives user login information',
         security=[device_header])
    @use_kwargs(__schemas['request'])
    @marshal_with(__schemas['output'])
    def post(self, **user_data):

        login_checking = self.__controller.check_user_login(user_data['username'], user_data['password'])
        if not login_checking['status']:
            raise UserError(login_checking['output'], 401)

        result = self.__controller.create_token(user_data['username'])
        output = self.__schemas['output']().load(data=result)
        return output