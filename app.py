from configs import ProductionConfig, DevelopmentConfig, is_in_prod
from database.db import initialize_db
from flask import Flask
from flask_restful import Api
from resources.Users import Users
from utils.JsonEncoder import MongoEngineJsonEncoder


app = Flask(__name__)
config = ProductionConfig if is_in_prod() else DevelopmentConfig
app.config.from_object(config)
initialize_db(app)
app.json_encoder = MongoEngineJsonEncoder

api = Api(app)

api.add_resource(Users, '/users', '/users/<string:user_id>')


if __name__ == '__main__':
    app.run()
