import os
from flask_script import Manager # class for handling a set of commands
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from api import app
from src.db_setup import db

from models import User


app.config.from_object(os.environ['APP_SETTINGS'])
# env_name = os.getenv('FLASK_ENV')

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)



db.init_app(app)
migrate.init_app(app, db)
if __name__ == '__main__':
    manager.run()