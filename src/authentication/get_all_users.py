from marshmallow import (validate, ValidationError)
from flask import request, jsonify, make_response
from flask_restful import Resource

from models import User
from src.db_setup import db, bcrypt
from src.middlewares.isAdmin import isAdmin
import jwt
import os

class GetAllUsers(Resource):
    # @isAdmin
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

        # check if user is admin
        if data["user_role"] != "admin":
            return make_response(jsonify({"status":403, "message":"not allowed"}), 403)

        users = User.query.all()
        users_list = [i.serialize for i in users]

        return make_response(jsonify({
            "status":200,
            "data":users_list
            }), 200)