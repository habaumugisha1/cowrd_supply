from models import ProductCategory

from marshmallow import fields, validate, Schema


class PurchaseOrderSchema(Schema):
    class Meta:
        model = ProductCategory

    name = fields.Str(required=True)
    image = fields.Str(required=True)
    duration = fields.Integer(required=True)
    fundingLimit = fields.Integer(required=True)
    ranking = fields.Str(required=True)
    shortDescription = fields.Str(required=True)
    description = fields.Str(required=True)
    testmonialId = fields.Str(required=True)
    interestRate = fields.Integer(required=True)
