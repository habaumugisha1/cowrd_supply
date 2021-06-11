from flask import jsonify, make_response, request, g
from flask_restful import Resource
from marshmallow import (validate, ValidationError)
from src.schema.causeShema import CauseSchema
from src.db_setup import db
from models import Cause, ProductCategory, Testimonial
from src.middlewares.isAdmin import isAdmin
import os
import jwt

class Causes(Resource):

    def get(self):
        causes = Cause.query.all()
        cause_list = [i.serialize for i in causes]

        return make_response(jsonify({
            "status":200,
            "message":"causes retrieved successful!",
            "data":cause_list
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
        schema = CauseSchema()

        # initializing validation error
        errors = schema.validate(body)
        if errors:
            return make_response(jsonify({"status":400, "error" : errors}), 400)
        
        name = body['name']
        image = body['image']
        shortDescription = body['shortDescription']
        description = body['description']
        testmonialId = body['testmonialId']

        # check if cause already exist in database
        cause_exist = Cause.query.filter_by(name=name).first()

        if cause_exist:
            return make_response(jsonify({
                "status":409,
                "message": "cause with this " + name + " is already exist"}), 409)
        # asigining cause dictionally to cause model
        new_cause = Cause(name=name, image=image, shortDescription=shortDescription, description=description, testmonialId=testmonialId)

        result = schema.dump(new_cause)
        db.session.add(new_cause)
        db.session.commit()

        return make_response(jsonify({"status":201, "message":"Cause created successful!", "testimonial":result}), 201)


class ModifyCause(Resource):
    def get(self, id):
        single_cause = Cause.query.filter_by(id=id).first()

        if not single_cause:
            return make_response(jsonify({"status":404, "message":"No results found! related to " + id }), 404)

        # serializing single cause
        serialized_cause = single_cause.serialize
        
        # finding testimonial releted to this cause
        testimonial = Testimonial.query.filter_by(id=serialized_cause['testmonialId']).first()
        serialized_testimonial = testimonial.serialize

        # find all products category related to this cause
        product_category = ProductCategory.query.filter_by(causeId=id).all()
        serialized_categories = [i.serialize for i in product_category]
      

        return make_response(jsonify(
            {
            "status": 200,
            "message": "cause successful retrieved!",
            "cause": serialized_cause,
            "product_category": serialized_categories,
            "testimonial": serialized_testimonial
            }
         ), 200)

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

        # declaring user data input
        body = request.get_json()
        single_cause = Cause.query.filter_by(id=id).first()

        if not single_cause:
            return make_response(jsonify({"status":404, "message":"No results found! related to " + id }), 404)

        single_cause.name = body['name']
        single_cause.image = body['image']
        single_cause.shortDescription = body['shortDescription']
        single_cause.description = body['description']

        db.session.add(single_cause)
        db.session.commit()

        return make_response(jsonify({"status": 200, "message": "cause successful updated!", "testimonial": single_cause.serialize}), 200)

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

        # check if cause is exist in database
        single_cause = Cause.query.filter_by(id=id).first()

        if not single_cause:
            return make_response(jsonify({"status":404, "message":"No results found! related to " + id }), 404)

        db.session.delete(single_cause)
        db.session.commit()

        return make_response(jsonify({"status":200, "message":"cause successful deleted!"}), 200)
