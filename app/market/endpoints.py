from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource

from . import controllers
from . import schemas
from auth import controllers as auth_controllers
from utils import UserError, DeviceError, HouseError, error_handler, device_header, user_header

api_required = auth_controllers.OAuthController.api_required
user_required = auth_controllers.OAuthController.user_required

MARKET = 'Market operations'


class CreateHouseApi(MethodResource):
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


class HousesApi(MethodResource):
    __controller = controllers.HouseController()
    __schemas = {
        "response": schemas.HousesSchema,
        "output": schemas.OutputSchema
    }
    decorators = [
        user_required,
        api_required,
        error_handler
    ]

    @doc(tags=[MARKET],
         summary='returns info about every house',
         description="Returns Houses info",
         security=[device_header, user_header])
    @marshal_with(__schemas['response'], code=200)
    def get(self, **kwargs):
        result = self.__controller.get_houses_public_info()
        response = self.__schemas['response']().load(data=result)
        return response, 200


class HouseApi(MethodResource):
    __controller = controllers.HouseController()
    __schemas = {
        "response": schemas.HouseSchema,
        "output": schemas.OutputSchema
    }
    decorators = [
        user_required,
        api_required,
        error_handler
    ]

    @doc(tags=[MARKET],
         summary="return House info by id",
         description="Receives house_id",
         security=[device_header, user_header])
    @marshal_with(__schemas['response'], code=200)
    def get(self, house_id, **kwargs):
        house_checking = self.__controller.check_house_exists(house_id)
        if not house_checking['status']:
            raise HouseError(house_checking['output'], 404)
        result = self.__controller.get_house_public_info(house_id)
        response = self.__schemas['response']().load(data=result)
        return response, 200
