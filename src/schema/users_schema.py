from models import User

from marshmallow import fields, validate, Schema


class UserSchema(Schema):

    class Meta:
        model = User

    username= fields.Str(required=True, validate=[validate.Length(min=4, max=250)])
    email = fields.Str(required=True, validate=validate.Email())
    password = fields.Str(required=True)
    firstName = fields.Str(required=True, validate=[validate.Length(min=4, max=250)])
    phone = fields.Str(required=True)
    lastName = fields.Str(required=True, validate=[validate.Length(min=4, max=250)])
    addressLine1 = fields.Str(required=True, validate=[validate.Length(min=5, max=250)])
    addressLine2 = fields.Str(required=False, validate=[validate.Length(max=250)])
    country = fields.Str(required=False, validate=[validate.Length(max=250)])
    city = fields.Str(required=True, validate=[validate.Length(min=5, max=100)])
    zipCode = fields.Str(required=True, validate=[validate.Length(min=5, max=250)])

