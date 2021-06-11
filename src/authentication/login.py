import os
from marshmallow import (validate, ValidationError)
from flask import request, jsonify, make_response,session
from flask_restful import Resource, marshal_with
from flask_restful import Resource, Api
from flask_bcrypt import check_password_hash
from datetime import datetime, timedelta
import jwt
import asyncio

from models import User
from src.schema.users_schema import UserSchema
from src.db_setup import db, bcrypt
from src.schema.user_login_schema import LoginSchema



class Login(Resource):
    def post(self):
        body = request.get_json()
        schema = LoginSchema()

        errors = schema.validate(body)

        if errors:
            return make_response(jsonify({"status": 400, "error": errors}), 400)

        email = body['email']
        password = body['password']

        # check user if is exist in database
        user_exist = User.query.filter_by(email=email).first()

        if not user_exist:
            return make_response(jsonify({"message": "You don't have account with this " + email +", Please create account" }), 404)

        # check user password and stored password
        compare_password = bcrypt.check_password_hash(user_exist.password, password)

        if not compare_password:
            return make_response(jsonify({"message": "Password incorrect" }), 400)
            
        auth_token = jwt.encode({
            "id":str(user_exist.id),
            "username":user_exist.username,
            "email":user_exist.email,
            "user_role":user_exist.userRole,
            "exp":datetime.utcnow() + timedelta(days =  3)
        },
        os.getenv('SECRET_KEY'),
        algorithm="HS256"
        )
        session['auth_token'] = auth_token

        res = make_response(jsonify({"status": 200,"message":"Login successful", "profile":user_exist.serialize, "auth_token": auth_token}),  200)
        
        return res


class Logout(Resource):
    def post(self):
        if not 'auth_token' in session:
            return make_response(jsonify({"status":401, "message":"Please login!"}), 401)

        if 'auth_token' in session:
            session.pop('auth_token', None)
            print(session.get('auth_token'))
            res = make_response(jsonify({"status":200, "message":"successful loged out!"}), 200)

        return res

        