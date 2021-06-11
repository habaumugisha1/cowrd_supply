import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from flask_migrate import Migrate
from dotenv import load_dotenv, find_dotenv
from config import app_config

load_dotenv(find_dotenv())

# migrate = Migrate()

app = Flask(__name__)
# app.config.from_object(os.environ.get('APP_SETTINGS'))
app.config.from_object(app_config['development'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)


api = Api(app)

@app.route('/api/v1')
def hello():
    return {'data': 'this is the db set up'}

db.init_app(app)
# migrate.init_app(app, db)

if __name__ == '__main__':
    app.run()
