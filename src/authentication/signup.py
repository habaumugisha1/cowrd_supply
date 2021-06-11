from marshmallow import (validate, ValidationError)
from flask import request, jsonify, make_response
from flask_restful import Resource, marshal_with

from models import User
from src.schema.users_schema import UserSchema
from src.db_setup import db, bcrypt


class Signup(Resource):
    def post(self):
        data = request.get_json()

        schema = UserSchema()

        errors = schema.validate(data)

        if errors:
            return make_response(jsonify({"status": 400, "error": errors}), 400)

        username = data['username']
        password = data['password']
        email = data['email']
        firstName= data['firstName']
        lastName= data['lastName']
        phone= data['phone']
        country= data['country']
        city= data['city']
        zipCode= data['zipCode']
        addressLine1= data['addressLine1']

        # bcrypting password for user secrit
        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        
        exist_user = User.query.filter_by(email=email).first()
        exist_username = User.query.filter_by(username=username).first()
        
        if exist_username:
                return make_response(jsonify({"status":409,
                    "message": "user with this " + username + " is already exist in database"}), 409)

        if exist_user:
            return make_response(jsonify({
                "status":409,
                "message": "user with this " + email + " is already exist"}), 409)


        user = User(username=username, password=pw_hash, email=email, firstName=firstName,lastName=lastName, phone=phone, country=country, city=city, zipCode=zipCode, addressLine1=addressLine1)

        result = schema.dump(user)

        db.session.add(user)
        db.session.commit()

        return make_response(jsonify({
            "status":201,
            "message": "User " + username + " created successfully",
            "data": [result]
        }), 201)