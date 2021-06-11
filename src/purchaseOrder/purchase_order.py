from flask import request, jsonify, make_response
from flask_restful import Resource
from src.db_setup import db
from src.schema.purchaseOrder import PurchaseOrderSchema
from models import PurchaseOrder, Testimonial
from src.middlewares.isAdmin import isAdmin
import os
import jwt

class PurchaseOrderController(Resource):
    def get(self):
        purchase_order = PurchaseOrder.query.all()

        purchase_order_list = [i.serialize for i in purchase_order]

        return make_response(jsonify({"status": 200, "message":"purchase order retrieved successful", "data": purchase_order_list}), 200)

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
        schema = PurchaseOrderSchema()

        errors = schema.validate(body)

        if errors:
            return make_response(jsonify({"status":400, "error": errors}), 400)

        name = body["name"]
        image = body["image"]
        duration = body["duration"]
        fundingLimit = body["fundingLimit"]
        interestRate = body["interestRate"]
        ranking = body["ranking"]
        shortDescription = body["shortDescription"]
        description = body["description"]
        testmonialId = body["testmonialId"]


        # finding existing of purchase order category

        purchase_order = PurchaseOrder.query.filter_by(name=name).first()

        if purchase_order:
            return make_response(jsonify({"status":409, "message": "The purchase order with this name " + name + " is already exist in database"}), 409)

        new_purchase_order = PurchaseOrder(name=name, image=image, duration=duration, interestRate=interestRate, fundingLimit=fundingLimit, ranking=ranking, shortDescription=shortDescription, description=description, testmonialId=testmonialId)

        results = schema.dump(new_purchase_order)

        db.session.add(new_purchase_order)
        db.session.commit()

        return make_response(jsonify({"status":201, "message":"Purchase order successful created!", "data":results}), 201)

class PurchaseOrderControllerModify(Resource):
    def get(self, id):
        
        #finding a purchase order
        single_purchase_order = PurchaseOrder.query.filter_by(id=id).first()

        if not single_purchase_order:
            return make_response(jsonify({"status":404, "message":"No result found"}), 404)
        
        serialize_purchase_order = single_purchase_order.serialize

        #finding testimonial related to purchase order

        purchase_order_testimonial = Testimonial.query.filter_by(id=serialize_purchase_order["testmonialId"]).first()

        # serializing purchase order
        serialized_order_testimonial = purchase_order_testimonial.serialize

        return make_response(jsonify({
            "status":200,
            "message":"purchase order retrieved successful!",
            "data": serialize_purchase_order,
            "testimonial": serialized_order_testimonial}), 200)

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

        # check if purchase order exist in database
        purchase_order_exist = PurchaseOrder.query.filter_by(id=id).first()

        if not purchase_order_exist:
            return make_response(jsonify({"status":404, "message":"You can't update none existing data"}))
            
        # serializing existing purchase order 
        serialized_purchase_order = purchase_order_exist.serialize

        body = request.get_json()

        purchase_order_exist.name = body["name"]
        purchase_order_exist.image = body["image"]
        purchase_order_exist.duration = body["duration"]
        purchase_order_exist.fundingLimit = body["fundingLimit"]
        purchase_order_exist.interestRate = body["interestRate"]
        purchase_order_exist.ranking = body["ranking"]
        purchase_order_exist.shortDescription = body["shortDescription"]
        purchase_order_exist.description = body["description"]
        purchase_order_exist.testmonialId = body["testmonialId"]

        db.session.add(purchase_order_exist)
        db.session.commit()

        return make_response(jsonify({
            "status":200,
            "message":"purchase order updated successful!",
            }), 200)


    def delete(selef, id):
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
        purchase_order_exist = PurchaseOrder.query.filter_by(id=id).first()

        if not purchase_order_exist:
             return make_response(jsonify({"status":404, "message":"No result fuond, You can't delete none existing data"}), 404)

        db.session.delete(purchase_order_exist)
        db.session.commit()

        return make_response(jsonify({"status":200, "message":"purchase order  successful deleted!"}), 200)