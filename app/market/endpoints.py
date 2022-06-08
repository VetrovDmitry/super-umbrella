from flask_restful import Resource
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource

from . import controllers
from . import schemas
from auth import controllers as auth_controllers
from utils import UserError, DeviceError, error_handler, device_header, user_header

api_required = auth_controllers.OAuthController.api_required
user_required = auth_controllers.OAuthController.user_required

MARKET = 'Market operations'


class CreateHouseApi(MethodResource, Resource):
    __controller = controllers.HouseController()
    __schemas = {
        'request': schemas.NewHouseSchema,
        'output': schemas.OutputSchema
    }
    decorators = [
        user_required,
        api_required,
        error_handler]

    @doc(tags=[MARKET],
         summary='uploads new House to market',
         descirption='Receives House info',
         security=[device_header, user_header])
    @use_kwargs(__schemas['request'])
    @marshal_with(__schemas['output'], code=201)
    def post(self, **house_data):
        result = self.__controller.create_house(house_data)
        output = self.__schemas['output']().load(result)
        return output, 201