from app_secrets import DATABASE_USERNAME, DATABASE_PASSWORD, DATABASE_GROUP_ACT_HOSTNAME, FLASK_APP_SECRET_KEY
import os


class Config(object):
    SECRET_KEY = FLASK_APP_SECRET_KEY
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    MONGODB_SETTINGS = {
        'db': 'group-act',
        'username': DATABASE_USERNAME,
        'password': DATABASE_PASSWORD,
        'host': DATABASE_GROUP_ACT_HOSTNAME
    }


class DevelopmentConfig(Config):
    MONGODB_SETTINGS = {
        'db': 'group-act',
        'host': 'mongodb://localhost:27017/group-act?retryWrites=true&w=majority'
    }

def is_in_prod():
    return os.getenv('FLASK_ENV', 'production') == 'production'
