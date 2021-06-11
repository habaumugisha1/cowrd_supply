from flask import request, make_response, jsonify, g
from flask_restful import Resource
from functools import wraps
import os
import jwt

def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):

      auth_header = request.headers.get('Authorization')

      if not auth_header:

        return make_response(jsonify({"status":401, "message":"Please log in first!"}), 401)

      token = auth_header.split(" ")[1]

  
      data = jwt.decode(
      token,
      os.getenv('SECRET_KEY'), algorithms=["HS256"]
      )
    

      return f(data, *args, **kwargs)
   return decorator