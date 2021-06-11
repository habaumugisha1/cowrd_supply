import os
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# initialize our db
db = SQLAlchemy()

# this is for bcrypting password
bcrypt = Bcrypt()


