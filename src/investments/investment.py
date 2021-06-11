from flask import request, make_response, jsonify
from flask_restful import Resource
from src.db_setup import db
from models import Investment, User, ProductCategory, PurchaseOrder, SupplyStatus
import os
import json
import jwt
from src.schema.investmentSchema import InvestmentSchema

from ..middlewares.user_token import userToken



class InvestmentController(Resource):

    def get(self):
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

        if data["user_role"] != "admin":
            return make_response(jsonify({"status":403, "message":"access dinied!"}), 403)

        investment = Investment.query.all()
        investment_list = [i.serialize for i in investment
        ]
        return make_response(jsonify({"status": 200, "message":"Investment retrieved successful", "data": investment_list}), 200)


    def post(self):
        invested_on = {}
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

        # finding invested user
        user = User.query.filter_by(id=data["id"]).first()
        serialized_user = user.serialize

        # initializing request body
        body = request.get_json()
        schema = InvestmentSchema()
        errors = schema.validate(body)

        if errors:
            return make_response(jsonify({"status":400, "error": errors}), 400)

        productCategoryId = body["productCategoryId"]
        productCategory = body["productCategory"]
        purchase_order = body["purchase_order"]
        amount = body["amount"]
        interestRate = body["interestRate"]
        
        

        # finding product category or purchase order details
        if productCategory == True:
            product_category = ProductCategory.query.filter_by(id=productCategoryId).first()

            if product_category:
                product_category_serialized = product_category.serialize
                invested_on.update(product_category_serialized)

        if purchase_order == True:
            purchaseOrders = PurchaseOrder.query.filter_by(id=productCategoryId).first()

            if purchaseOrders:
                purchaseOrders_serialized = purchaseOrders.serialize
                invested_on.update(purchaseOrders_serialized)
        
        new_investment = Investment(userId=serialized_user["id"], productCategoryId=invested_on["id"], amount=amount, name=invested_on["name"], interestRate=interestRate, productCategory=productCategory, purchase_order=purchase_order)

        db.session.add(new_investment)
        db.session.commit()

        return make_response(jsonify({"status":201,
            "message":"create investments successful!",
         "invester_details": serialized_user, "invested_on":invested_on}), 201)

class InvestmentAdmin(Resource):
    def get(self, id):
        invested_on = {}
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

        #check in user is admin
        if data["user_role"] != "admin":
            return make_response(jsonify({"status":403, "message":"access dinied!"}), 403)
        investment_exist = Investment.query.filter_by(id=id).first()
        serialized_investment = investment_exist.serialize

        if not investment_exist:
            return make_response(jsonify({"status":404, "message":"No results found! related to this " + id + " ID"}), 404)
        # finding invested user
        user = User.query.filter_by(id=serialized_investment["userId"]).first()
        serialized_user = user.serialize

        # finding product category or purchase order
        if serialized_investment["productCategory"] == True:
            product_category = ProductCategory.query.filter_by(id=serialized_investment["productCategoryId"]).first()

            if product_category:
                product_category_serialized = product_category.serialize
                invested_on.update(product_category_serialized)

        if serialized_investment["purchase_order"] == True:
            purchaseOrders = PurchaseOrder.query.filter_by(id=serialized_investment["productCategoryId"]).first()

            if purchaseOrders:
                purchaseOrders_serialized = purchaseOrders.serialize
                invested_on.update(purchaseOrders_serialized)

        # finding exsiting supply status on investment
        supply_status = SupplyStatus.query.filter_by(investmentId=id).all()
        supply_status_list = [i.serialize for i in supply_status]

        return make_response(jsonify({
            "status":200,
             "investment":serialized_investment,
              "investor": serialized_user,
              "invested_on":invested_on,
              "supply_status":supply_status_list
              }), 200)

    def patch(self, id):
        auth_header = request.headers.get('Authorization')
        body = request.get_json()
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
            return make_response(jsonify({"status":403, "message":"This is for only company"}), 403)

        investment_exist = Investment.query.filter_by(id=id).first()

        if not investment_exist:
            return make_response(jsonify({"status":404, "message":"No result found"}), 404)
        investment_exist.InvestmentStatus = body["InvestmentStatus"]

        db.session.commit()

        return make_response(jsonify({"status":200, "message":"Investment " + body["InvestmentStatus"]+ " successful"}), 200)

class MyInvestments(Resource):
    def get(self):
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

        # check if investment is exist in database
        investment_exist = Investment.query.filter_by(userId=data["id"]).all()
        if not investment_exist:
            return make_response(jsonify({"status":404, "message":"No investment you made yet!"}), 404)

        serialized_investment = [i.serialize for i in investment_exist]

        return make_response(jsonify({
            "status":200,
            "message":"My investments",
             "investment":serialized_investment
              }), 200)

class MyInvestment(Resource):
    def get(self, id):
        invested_on = {}
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

        investment_exist = Investment.query.filter_by(id=id).first()

        if not investment_exist:
            return make_response(jsonify({"status":404, "message":"No result found!"}), 404)

        serialized_investment = investment_exist.serialize 

        # finding product category or purchase order
        if serialized_investment["productCategory"] == True:
            product_category = ProductCategory.query.filter_by(id=serialized_investment["productCategoryId"]).first()

            if product_category:
                product_category_serialized = product_category.serialize
                invested_on.update(product_category_serialized)

        if serialized_investment["purchase_order"] == True:
            purchaseOrders = PurchaseOrder.query.filter_by(id=serialized_investment["productCategoryId"]).first()

            if purchaseOrders:
                purchaseOrders_serialized = purchaseOrders.serialize
                invested_on.update(purchaseOrders_serialized)
         # finding exsiting supply status on investment
        supply_status = SupplyStatus.query.filter_by(investmentId=id).all()
        supply_status_list = [i.serialize for i in supply_status]

        return make_response(jsonify({
            "status":200,
            "message":"My investment",
             "investment":serialized_investment,
             "invested_on": invested_on,
             "supply_status":supply_status_list
              }), 200)

    def patch(self, id):
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

        # check if investment is exist in database
        investment_exist = Investment.query.filter_by(id=id).first()

        if not investment_exist:
            return make_response(jsonify({"status":404, "message":"No result found!"}), 404)

        serialized_investment = investment_exist.serialize

        #check if user is owner
        if str(data["id"]) != str(serialized_investment["userId"]):
            return make_response(jsonify({"status":403, "message":" Only investment owner can cancel it!"}), 403)

        # check if investment is already approved
        if serialized_investment["InvestmentStatus"] == "approved" or serialized_investment["InvestmentStatus"] == "rejected":
            return make_response(jsonify({"status":403, "message":" You can't cancel an approved or rejected investment!"}), 403)

        investment_exist.InvestmentStatus = "canceled"

        db.session.commit()

        return make_response(jsonify({"status":200, "message":"Investment canceled successful"}), 200)

