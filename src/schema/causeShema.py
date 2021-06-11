from models import Cause

from marshmallow import fields, validate, Schema


class CauseSchema(Schema):
    class Meta:
        model = Cause

    name = fields.Str(required=True)
    image = fields.Str(required=True)
    shortDescription = fields.Str(required=True)
    description = fields.Str(required=True)
    testmonialId = fields.Str(required=True)
