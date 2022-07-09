from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource
from flask import current_app, request
from . import controllers
from . import schemas
from app.auth import controllers as auth_controllers
from app.utils import UserError, DeviceError, FileError, HouseError, error_handler, device_header, user_header

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
        "request": schemas.HouseDetailSchema,
        "response": schemas.HouseSchema,
        "output": schemas.OutputSchema
    }
    decorators = [
        user_required,
        api_required,
        error_handler
    ]

    @doc(tags=[MARKET],
         summary="returns House info by id",
         description="Receives house_id",
         security=[device_header, user_header])
    @marshal_with(__schemas['response'], code=200)
    def get(self, house_id, **kwargs):

        current_user = kwargs['current_user']

        house_checking = self.__controller.check_house_exists(house_id)
        if not house_checking['status']:
            raise HouseError(house_checking['output'], 404)

        result = self.__controller.get_house_public_info(house_id)
        response = self.__schemas['response']().load(data=result)

        current_app.logger.info(f"server sends to user: {current_user.id} public info of house: {house_id}")

        return response, 200

    @doc(tags=[MARKET],
         summary="updates House info by id",
         description="Receives house_id",
         security=[device_header, user_header],
         consumes='multipart/form-data')
    @use_kwargs(__schemas["request"], location='form')
    @marshal_with(__schemas["output"], code=204)
    def put(self, house_id, **house_data):

        current_user = house_data["current_user"]

        house_checking = self.__controller.check_house_exists(house_id)
        if not house_checking['status']:
            raise HouseError(house_checking['output'], 404)

        owner_checking = self.__controller.check_house_owner(house_id, current_user.id)
        if not owner_checking['status']:
            raise HouseError(owner_checking['output'], 403)

        file = request.files.get('photo')
        if file:
            type_checking = self.__controller.check_photo_type(file.content_type)
            if type_checking['status']:
                raise FileError(type_checking['output'])

        house_data['photo'] = file
        result = self.__controller.change_house_details(house_id, house_data)
        output = self.__schemas['output']().load(data=result)

        return output, 204

    @doc(tags=[MARKET],
         summary="delete House by id",
         descirptions="Receives house_id",
         security=[device_header, user_header])
    @marshal_with(__schemas['output'], code=204)
    def delete(self, house_id, **kwargs):

        current_user = kwargs['current_user']

        house_checking = self.__controller.check_house_exists(house_id)
        if not house_checking['status']:
            raise HouseError(house_checking['output'], 404)

        owner_checking = self.__controller.check_house_owner(house_id, current_user.id)
        if not owner_checking['status']:
            raise HouseError(owner_checking['output'], 403)

        result = self.__controller.delete_house_by_id(house_id)
        output = self.__schemas['output']().load(data=result)

        return output, 204


class SearchHouseApi(MethodResource):
    __controller = controllers.HouseController()
    __schemas = {
        'response': schemas.HousesSchema,
        'query': schemas.SearchHouseSchema
    }
    decorators = [
        user_required,
        api_required,
        # error_handler
    ]

    @doc(tags=[MARKET],
         summary="returns houses by search",
         description="Receives house query",
         security=[device_header, user_header])
    @use_kwargs(__schemas['query'], location='query')
    @marshal_with(__schemas['response'], code=200)
    def get(self, **house_data):
        result = self.__controller.search_house(house_data)
        response = self.__schemas['response']().load(data=result)
        return response, 200
