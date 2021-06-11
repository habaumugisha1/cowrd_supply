from flask import request, make_response, jsonify
from flask_restful import Resource
from src.db_setup import db
from models import Investment, User, ProductCategory, PurchaseOrder, SupplyStatus
import os
import json
import jwt
from src.schema.supplyStepsSchema import SupplyStepSchema


class SupplyStatusController(Resource):
    def post(self, id):

        body = request.get_json()
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
        schema = SupplyStepSchema()

        errors = schema.validate(body)

        if errors:
            return make_response(jsonify({"status":400, "error": errors}), 400)
        investmentId = id
        step = body["step"]
        description = body["description"]

        # finding exsiting supply status on investment
        supply_status = SupplyStatus.query.filter_by(investmentId = id).all()
        supply_status_list = [i.serialize for i in supply_status]

        supply = SupplyStatus(step=step, description=description, investmentId=investmentId)

        db.session.add(supply)
        db.session.commit()
        results = schema.dumps(body)
        return make_response(jsonify({"status": 201, "message":" supply status created successful!"}),201)
