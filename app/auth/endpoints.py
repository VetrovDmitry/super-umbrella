from flask_restful import Resource
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource
from flask_login import current_user

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