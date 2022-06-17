from marshmallow import Schema, post_load, fields, validate

from auth.schemas import OutputSchema


class NewHouseSchema(Schema):
    city = fields.Str()
    street = fields.Str()
    house_number = fields.Str()
    summary = fields.Str()
    cost = fields.Float()
    user_id = fields.Int()


class SearchHouseSchema(Schema):
    city = fields.Str()
    street = fields.Str()
    house_number = fields.Str()
    cost = fields.Float()

    @post_load
    def prepare_city(self, in_data, **kwargs):
        if in_data.get('city', '') == '':
            in_data['city'] = ''
        return in_data

    @post_load
    def prepare_street(self, in_data, **kwargs):
        if in_data.get('street', '') == '':
            in_data['street'] = ''
        return in_data

    @post_load
    def prepare_house_number(self, in_data, **kwargs):
        if in_data.get('house_number', '') == '':
            in_data['house_number'] = ''
        return in_data

    @post_load
    def prepare_cost(self, in_data, **kwargs):
        if in_data.get('cost', None) is None:
            in_data['cost'] = None
        return in_data


class HouseSchema(Schema):
    id = fields.Int()
    city = fields.Str()
    street = fields.Str()
    house_number = fields.Str()
    summary = fields.Str()
    cost = fields.Float()
    user_id = fields.Int()
    time_created = fields.DateTime()


class HousesSchema(Schema):
    houses = fields.List(fields.Nested(HouseSchema))


class HouseDetailSchema(Schema):
    city = fields.Str()
    street = fields.Str()
    house_number = fields.Str()
    summary = fields.Str()
    cost = fields.Float()

    @post_load
    def prepare_city(self, in_data, **kwargs):
        if in_data.get('city', 'string') == 'string':
            in_data['city'] = ''
        return in_data

    @post_load
    def prepare_street(self, in_data, **kwargs):
        if in_data.get('street', 'string') == 'string':
            in_data['street'] = ''
        return in_data

    @post_load
    def prepare_house_number(self, in_data, **kwargs):
        if in_data.get('house_number', 'string') == 'string':
            in_data['house_number'] = ''
        return in_data

    @post_load
    def prepare_summary(self, in_data, **kwargs):
        if in_data.get('summary', 'string') == 'string':
            in_data['summary'] = ''
        return in_data

    @post_load
    def prepare_cost(self, in_data, **kwargs):
        if in_data.get('cost', 0) == 0:
            in_data['cost'] = None
        return in_data