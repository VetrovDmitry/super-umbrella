from marshmallow import Schema, post_load, fields, validate

from auth.schemas import OutputSchema

class NewHouseSchema(Schema):
    city = fields.Str()
    street = fields.Str()
    house_number = fields.Str()
    summary = fields.Str()
    cost = fields.Float()
    user_id = fields.Int()


class HouseSchema(Schema):
    id = fields.Int()
    city = fields.Str()
    street = fields.Str()
    house_number = fields.Str()
    summary = fields.Str()
    cost = fields.Float()
    user_id = fields.Int()
    time_created = fields.DateTime()