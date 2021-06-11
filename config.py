import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

# basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    


class ProductionConfig(Config):
    PRODUCTION = True
    DEVELOPMENT = False
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_PRODUCTION_URI')


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    PRODUCTION = False


class TestingConfig(Config):
    TESTING = True


# app_config = {
#     'development': DevelopmentConfig,
#     'testing': TestingConfig,
#     'staging': StagingConfig,
#     'production': ProductionConfig,
# }