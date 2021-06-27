from app_secrets import DATABASE_USERNAME, DATABASE_PASSWORD, DATABASE_GROUP_ACT_HOSTNAME_PROD, DATABASE_GROUP_ACT_HOSTNAME_DEV, FLASK_APP_SECRET_KEY, JWT_SECRET_KEY
import datetime
import os


class Config(object):
    JWT_SECRET_KEY = JWT_SECRET_KEY
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=1)
    # Always send cookie over https.
    JWT_COOKIE_SECURE = True
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_CSRF_CHECK_FORM = True

    SECRET_KEY = FLASK_APP_SECRET_KEY
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    MONGODB_SETTINGS = {
        'db': 'group-act',
        'username': DATABASE_USERNAME,
        'password': DATABASE_PASSWORD,
        'host': DATABASE_GROUP_ACT_HOSTNAME_PROD
    }


class DevelopmentConfig(Config):
    # Turn off this flag so that cookies can be sent through http in dev
    # environment
    JWT_COOKIE_SECURE = False

    MONGODB_SETTINGS = {
        'db': 'group-act',
        'host': DATABASE_GROUP_ACT_HOSTNAME_DEV
    }

def is_in_prod():
    return os.getenv('FLASK_ENV', 'production') == 'production'
