from models import Investment

from marshmallow import fields, validate, Schema

class InvestmentSchema(Schema):
    class Meta:
        model = Investment

    productCategoryId = fields.Str(required=True)
    productCategory = fields.Boolean(required=True)
    purchase_order = fields.Boolean(required=True)
    amount = fields.Integer(required=True)
    interestRate = fields.Integer(required=True)