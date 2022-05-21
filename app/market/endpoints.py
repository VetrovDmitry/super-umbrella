from flask_restful import Resource
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource

from . import controllers
from . import schemas


MARKET = 'Market operations'


class CreateHouseApi(MethodResource, Resource):
    __controller = controllers.HouseController()
    __schemas = {
        'request': schemas.NewHouseSchema,
        'output': schemas.OutputSchema
    }

    @doc(tags=[MARKET],
         summary='uploads new House to market',
         descirption='Receives House info')
    @use_kwargs(__schemas['request'])
    @marshal_with(__schemas['output'])
    def post(self, **house_data):
        result = self.__controller.create_house(house_data)
        output = self.__schemas['output']().load(result)
        return output, 201