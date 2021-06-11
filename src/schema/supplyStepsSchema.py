from models import SupplyStatus

from marshmallow import fields, validate, Schema


class SupplyStepSchema(Schema):
    class Meta:
        model = SupplyStatus

    step = fields.Str(required=True)
    investmentId = fields.Str()
    description = fields.Str(required=True)
    value = fields.Str()