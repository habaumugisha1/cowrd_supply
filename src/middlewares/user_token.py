from flask import request, make_response, jsonify, g
import os
import jwt



def userToken():
    auth_header = request.headers.get('Authorization')
    print(auth_header)
    if not auth_header:
        return make_response(jsonify({"status":401, "message":"Please log in first!"}), 401)
    

    token = auth_header.split(" ")[1]

    data = jwt.decode(
        token,
        os.getenv('SECRET_KEY'), algorithms=["HS256"]
        )
    return (data, auth_header)