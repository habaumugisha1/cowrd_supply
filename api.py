import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from flask_migrate import Migrate
from dotenv import load_dotenv, find_dotenv
from flask_cors import CORS
import config
from src.routes import initialize_routes


load_dotenv(find_dotenv())

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_pyfile('config.py')

CORS(app)
api = Api(app)
db = SQLAlchemy()


# initialize routes file
initialize_routes(api)


db.init_app(app)

if __name__ == '__main__':
    app.run()
