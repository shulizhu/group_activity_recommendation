from flask_jwt_extended import JWTManager

def initialize_jwt(app):
    jwt = JWTManager(app)
    return jwt