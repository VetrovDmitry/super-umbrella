from marshmallow import Schema, post_load, fields, validate


class OutputSchema(Schema):
    message = fields.Str()


class NewUserSchema(Schema):
    name = fields.Str()
    username = fields.Str()
    email = fields.Email()
    password = fields.Str()

    @property
    def data(self) -> dict:
        return {
            "name": self.name,
            "username": self.username,
            "email": self.email,
            "password": self.password
        }

    @post_load
    def prepare_username(self, in_data, **kwargs):
        in_data["username"] = in_data["username"].lower().strip().replace(" ", "_")
        return in_data


class PublicUserSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    email = fields.Email()
    date_registered = fields.DateTime()
    username = fields.Str()


class PublicUsersSchema(Schema):
    users = fields.List(fields.Nested(PublicUserSchema))


class LoginSchema(Schema):
    username = fields.Str()
    password = fields.Str()


class TokenSchema(Schema):
    access_token = fields.Str()


class SignupSchema(Schema):
    name = fields.Str()
    username = fields.Str()
    email = fields.Email()
    password = fields.Str()
    birth_date = fields.Date()
    sex = fields.Str(validate=validate.OneOf(['Male', 'Female']))


class NewDeviceSchema(Schema):
    name = fields.Str()
    user_id = fields.Int()


class DeviceSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    key = fields.Str()
    user_id = fields.Int()