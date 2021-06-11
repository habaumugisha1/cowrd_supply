from models import User

from marshmallow import fields, validate, Schema


class LoginSchema(Schema):
    class Meta:
        model = User

    email = fields.Str(required=True, validate=validate.Email())
    password = fields.Str(required=True)