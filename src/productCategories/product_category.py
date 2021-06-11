from flask import request, jsonify, make_response
from flask_restful import Resource
from src.db_setup import db
from src.schema.productCategorySchema import ProductCategorySchema
from models import ProductCategory, Testimonial
from src.middlewares.isAdmin import isAdmin
import os
import jwt

class ProductCategoryController(Resource):
    def get(self):
        product_category = ProductCategory.query.all()

        product_category_list = [i.serialize for i in product_category]

        return make_response(jsonify({"status": 200, "message":"product category retrieved successful", "data": product_category_list}), 200)

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
        schema = ProductCategorySchema()

        errors = schema.validate(body)

        if errors:
            return make_response(jsonify({"status":400, "error": errors}), 400)

        name = body["name"]
        image = body["image"]
        duration = body["duration"]
        fundingLimit = body["fundingLimit"]
        interestRate = body["interestRate"]
        ranking = body["ranking"]
        causeId = body["causeId"]
        shortDescription = body["shortDescription"]
        description = body["description"]
        testmonialId = body["testmonialId"]

        # finding existing of product category

        category = ProductCategory.query.filter_by(name=name, causeId=causeId).first()

        if category:
            return make_response(jsonify({"status":409, "message": "The product category with this name " + name + " is already exist in database"}), 409)

        new_product_category = ProductCategory(name=name, image=image, duration=duration, interestRate=interestRate, fundingLimit=fundingLimit, ranking=ranking, causeId=causeId, shortDescription=shortDescription, description=description, testmonialId=testmonialId)

        results = schema.dump(new_product_category)

        db.session.add(new_product_category)
        db.session.commit()

        return make_response(jsonify({"status":201, "message":"Product category successful created!", "data":results}), 201)

class productCategoryModify(Resource):
    def get(self, id):
        single_category = ProductCategory.query.filter_by(id=id).first()

        if not single_category:
            return make_response(jsonify({"status":404, "message":"No result found"}), 404)

        serialized_category = single_category.serialize
        category_testimonial = Testimonial.query.filter_by(id=serialized_category["testmonialId"]).first()
        serialized_testimonial = category_testimonial.serialize

        return make_response(jsonify({
            "status":200,
            "message":"product category retrieved successful!",
            "data":serialized_category,
            "testimonial":serialized_testimonial}), 200)

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

        # check if product category exist in database
        product_exist = ProductCategory.query.filter_by(id=id).first()

        if not product_exist:
            return make_response(jsonify({"status":404, "message":"You can't update none existing data"}))
            
        # serializing existing product category
        serialized_product = product_exist.serialize

        body = request.get_json()

        product_exist.name = body["name"]
        product_exist.image = body["image"]
        product_exist.duration = body["duration"]
        product_exist.fundingLimit = body["fundingLimit"]
        product_exist.interestRate = body["interestRate"]
        product_exist.ranking = body["ranking"]
        product_exist.causeId = body["causeId"]
        product_exist.shortDescription = body["shortDescription"]
        product_exist.description = body["description"]
        product_exist.testmonialId = body["testmonialId"]

        db.session.add(product_exist)
        db.session.commit()

        return make_response(jsonify({
            "status":200,
            "message":"product category updated successful!"
            }), 200)

    
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

        # check if product category exist in database
        product_exist = ProductCategory.query.filter_by(id=id).first()

        if not product_exist:
            return make_response(jsonify({"status":404, "message":"No result fuond, You can't delete none existing data"}), 404)

        db.session.delete(product_exist)
        db.session.commit()

        return make_response(jsonify({"status":200, "message":"product category successful deleted!"}), 200)