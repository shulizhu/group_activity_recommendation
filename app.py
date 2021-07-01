from authentication.jwt import initialize_jwt
from configs import ProductionConfig, DevelopmentConfig, is_in_prod
from database.db import initialize_db
from flask import Flask, render_template, jsonify, make_response
from flask_restful import Api
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request, unset_jwt_cookies
from jwt import ExpiredSignatureError

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
jwt = initialize_jwt(app)
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


@jwt.expired_token_loader
def expired_token_callback():
    response = redirect('/', code=302)
    unset_jwt_cookies(response)
    return response

@jwt.revoked_token_loader
def revoked_token_callback():
    response = redirect('/', code=302)
    unset_jwt_cookies(response)
    return response

@jwt.invalid_token_loader
def invalid_token_callback():
    response = redirect('/', code=302)
    unset_jwt_cookies(response)
    return response

@app.route('/')
@app.route('/user')
@app.route('/group')
def index():
    user = None
    try:
        verified = verify_jwt_in_request(optional=True)
        if verified:
            user_id = get_jwt_identity()
            if user_id:
                user = get_user_entry(user_id)
        user = jsonify(user).get_json()
        return render_template('index.html', user=user)
    except ExpiredSignatureError:
        response = make_response(render_template('index.html'), 200)
        response.headers['Content-Type'] = 'text/html'
        unset_jwt_cookies(response)
        return response

if __name__ == '__main__':
    app.run()
