from flask import request, jsonify, make_response
from flask_restful import Resource
from src.db_setup import db, bcrypt
from models import User
import os
class AdminUser(Resource):
    def post(self):
        username = os.getenv('ADMIN_USERNAME')
        email = os.getenv('ADMIN_EMAIL')
        password = bcrypt.generate_password_hash(os.getenv("ADMIN_PASSWORD")).decode('utf-8')
        firstName = "ami des jeunes"
        lastName = "habumugisha"
        phone = "+250784696314"
        country = "Rwanda"
        city = "Kigali"
        zipCode = "34525"
        addressLine1 = "Kicukiro"
        userRole="admin"
            
        
        exist_user = User.query.filter_by(email=email).first()
        exist_username = User.query.filter_by(username=username).first()
        
        if exist_username:
                return make_response(jsonify({"status":409,
                    "message": "user with this " + username + " is already exist in database"}), 409)

        if exist_user:
            return make_response(jsonify({
                "status":409,
                "message": "user with this " + email + " is already exist"}), 409)

        user = User(username=username, password=password, email=email, firstName=firstName,lastName=lastName, phone=phone, country=country, city=city, zipCode=zipCode, addressLine1=addressLine1, userRole=userRole)


        db.session.add(user)
        db.session.commit()

        return make_response(jsonify({
            "status":201,
            "message": "Admin user with username of " + username + " created successfully",
        }), 201)