from authentication.jwt import initialize_jwt
from configs import ProductionConfig, DevelopmentConfig, is_in_prod
from database.db import initialize_db
from flask import Flask
from flask_restful import Api
# from flask_cors import *

from resources.Sessions import Sessions
from resources.Users import Users
from resources.UserPreferences import UserPreferences
from resources.Groups import Groups
from utils.JsonEncoder import MongoEngineJsonEncoder


app = Flask(__name__)

config = ProductionConfig if is_in_prod() else DevelopmentConfig
app.config.from_object(config)

initialize_db(app)
initialize_jwt(app)
app.json_encoder = MongoEngineJsonEncoder

api = Api(app)

api.add_resource(Users, '/users', '/users/<string:user_id>')
api.add_resource(
    UserPreferences,
    '/users',
    '/users/<string:user_id>',
    '/users/<string:user_id>/preferences'
)
api.add_resource(Sessions, '/sessions')
api.add_resource(Groups, '/groups', '/groups/<string:group_id>')


# @app.after_request
# def cors(environ):
#     environ.headers['Access-Control-Allow-Origin'] = '*'
#     environ.headers['Access-Control-Allow-Method'] = '*'
#     environ.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
#     return environ


@app.route('/')
def index():
    return 'api'

if __name__ == '__main__':
    app.run()
