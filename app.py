from authentication.jwt import initialize_jwt
from configs import ProductionConfig, DevelopmentConfig, is_in_prod
from database.db import initialize_db
from flask import Flask, render_template, jsonify
from flask_restful import Api
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from resources.Sessions import Sessions
from resources.Users import Users
from resources.UserPreferences import UserPreferences
from resources.Groups import Groups
from utils.JsonEncoder import MongoEngineJsonEncoder
from services.UserService import get_user_entry


app = Flask(
    __name__,
    static_url_path='/static',
    static_folder='build/static',
    template_folder='build'
)

config = ProductionConfig if is_in_prod() else DevelopmentConfig
app.config.from_object(config)

initialize_db(app)
initialize_jwt(app)
app.json_encoder = MongoEngineJsonEncoder

api = Api(app)

api.add_resource(Users, '/api/users', '/api/users/<string:user_id>')
api.add_resource(
    UserPreferences,
    '/api/users',
    '/api/users/<string:user_id>',
    '/api/users/<string:user_id>/preferences'
)
api.add_resource(Sessions, '/api/sessions')
api.add_resource(Groups, '/api/groups', '/api/groups/<string:group_id>')


@app.route('/')
@app.route('/user')
@app.route('/group')
def index():
    user = None
    if verify_jwt_in_request(optional=True):
        user_id = get_jwt_identity()
        if user_id:
            user = get_user_entry(user_id)
    user = jsonify(user).get_json()
    return render_template('index.html', user=user)

if __name__ == '__main__':
    app.run()
