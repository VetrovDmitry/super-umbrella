from flask_restful import Resource
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource

from . import controllers
from . import schemas
from utils import UserError, error_handler

USER = 'User operations'


class UserApi(MethodResource, Resource):
    __controller = controllers.UserController()
    __schemas = {
        'request': schemas.NewUserSchema,
        'output': schemas.OutputSchema
    }
    decorators = []

    @doc(tags=[USER],
         summary='uploads new User',
         description='Receives minimal personal User info')
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


class UserSettingsApi(MethodResource, Resource):
    __controller = controllers.UserController()
    __schemas = {
        'response': schemas.PublicUserSchema,
        'output': schemas.OutputSchema
    }
    decorators = []

    @doc(tags=[USER],
         summary='returns User entity by id',
         desription='Receives user id')
    @marshal_with(__schemas['response'])
    def get(self, user_id: int) -> tuple:
        user_checking = self.__controller.check_user_exists(user_id)
        if not user_checking['status']:
            raise UserError(user_checking['output'], 404)

        result = self.__controller.get_user_public_info(user_id)
        response = self.__schemas['response']().load(data=result)
        return response


class UsersApi(MethodResource, Resource):
    __controller = controllers.UserController()
    __schemas = {
        'response': schemas.PublicUsersSchema
    }

    @doc(tags=[USER],
         summary='returns list of User entities',
         desription='...')
    @marshal_with(__schemas['response'])
    def get(self):
        result = self.__controller.get_users_public_info()
        response = self.__schemas['response']().load(data=result)
        return response


AUTH = 'Authentication operations'


class SignupApi(MethodResource, Resource):
    __controller = controllers.UserController()
    __schemas = {
        'request': schemas.SignupSchema,
        'output': schemas.OutputSchema
    }
    decorators = [error_handler]

    @doc(tags=[AUTH],
         summary='uploads new User with Member',
         description='Receives full User information')
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


class TokenApi(MethodResource, Resource):
    __controller = controllers.UserController()
    __schemas = {
        'request': schemas.LoginSchema,
        'output': schemas.TokenSchema
    }
    decorators = [error_handler]

    @doc(tags=[AUTH],
         summary='creates authorization token',
         description='Receives user login information')
    @use_kwargs(__schemas['request'])
    @marshal_with(__schemas['output'])
    def post(self, **user_data):

        login_checking = self.__controller.check_user_login(user_data['username'], user_data['password'])
        if not login_checking['status']:
            raise UserError(login_checking['output'], 401)

        result = self.__controller.create_token(user_data['username'])
        output = self.__schemas['output']().load(data=result)
        return output