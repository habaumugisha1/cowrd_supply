from models import Testimonial

from marshmallow import fields, validate, Schema


class TestimonialSchema(Schema):
    class Meta:
        model = Testimonial

    name = fields.Str(required=True)
    image = fields.Str(required=True)
    shortDescription = fields.Str(required=True)
    description = fields.Str(required=True)