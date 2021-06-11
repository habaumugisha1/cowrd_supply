from flask import jsonify, make_response, request, g
from flask_restful import Resource
from marshmallow import (validate, ValidationError)
from src.schema.testimonialSchema import TestimonialSchema
from src.db_setup import db
from models import Testimonial
from src.middlewares.isAdmin import isAdmin
from src.middlewares.check_admin import token_required
import os
import jwt

class Testimonials(Resource):
    def get(self):
            
        testimonials = Testimonial.query.all()
        testimonial_list = [i.serialize for i in testimonials]

        return make_response(jsonify({
            "status":200,
            "message":"testimonials retrieved successful!",
            "data":testimonial_list
            }), 200)


    def post(self):
        # token from headers
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return make_response(jsonify({"status":401, "message":"Please log in first!"}), 401)
        
        # getting user token
        token = auth_header.split(" ")[1]

        try:
            data = jwt.decode(
            token,
            os.getenv('SECRET_KEY'), algorithms=["HS256"]
            )
        except jwt.exceptions.ExpiredSignatureError:
            return make_response(jsonify({"status":401,"message":"token expired please log in again"}), 401)

        # check if user is admin
        if data["user_role"] != "admin":
            return make_response(jsonify({"status":403, "message":"not allowed"}), 403)
            
        body = request.get_json()
        schema = TestimonialSchema()

        errors = schema.validate(body)

        if errors:
            return make_response(jsonify({"status":400, "error" : errors}), 400)

        name = body['name']
        image = body['image']
        shortDescription = body['shortDescription']
        description = body['description']

        testimonial_exist = Testimonial.query.filter_by(name=name).first()

        if testimonial_exist:
            return make_response(jsonify({
                "status":409,
                "message": "testimonial with this " + name + " is already exist"}), 409)
        new_testimonial = Testimonial(name=name, image=image, shortDescription=shortDescription, description=description)

        result = schema.dump(new_testimonial)
        db.session.add(new_testimonial)
        db.session.commit()

        return make_response(jsonify({"status":201, "message":"Testimonial created successful!", "testimonial":result}), 201)

class UpdateTestimonial(Resource):        
    def patch(self, id):
    
        # token from headers
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return make_response(jsonify({"status":401, "message":"Please log in first!"}), 401)
        
        # getting user token
        token = auth_header.split(" ")[1]

        try:
            data = jwt.decode(
            token,
            os.getenv('SECRET_KEY'), algorithms=["HS256"]
            )
        except jwt.exceptions.ExpiredSignatureError:
            return make_response(jsonify({"status":401,"message":"token expired please log in again"}), 401)

        # check if user is admin
        if data["user_role"] != "admin":
            return make_response(jsonify({"status":403, "message":"not allowed"}), 403)

        body = request.get_json()
        testimonial = Testimonial.query.filter_by(id=id).first()

        if not testimonial:
            return make_response(jsonify({"status":404, "message":"No results found! related to " + id }), 404)

        name=body['name']
        image = body['image']
        shortDescription = body['shortDescription']
        description = body['description']

        testimonial.name = name
        testimonial.image = image
        testimonial.shortDescription = shortDescription
        testimonial.description = description

        db.session.commit()

        return make_response(jsonify({"status": 200, "message": "testimonial successful updated!", "testimonial": testimonial.serialize}), 200)

    def delete(self, id):
        # token from headers
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return make_response(jsonify({"status":401, "message":"Please log in first!"}), 401)
        
        # getting user token
        token = auth_header.split(" ")[1]

        try:
            data = jwt.decode(
            token,
            os.getenv('SECRET_KEY'), algorithms=["HS256"]
            )
        except jwt.exceptions.ExpiredSignatureError:
            return make_response(jsonify({"status":401,"message":"token expired please log in again"}), 401)

        # check if user is admin
        if data["user_role"] != "admin":
            return make_response(jsonify({"status":403, "message":"not allowed"}), 403)

        testimonial = Testimonial.query.filter_by(id=id).first()

        if not testimonial:
            return make_response(jsonify({"status":404, "message":"No results found related to " + id }), 404)

        
        db.session.delete(testimonial)
        db.session.commit()

        serialized_testimonial = testimonial.serialize

        return make_response(jsonify({"status": 200, "message": "testimonial successful deleted!", "testimonial": serialized_testimonial}), 200)

