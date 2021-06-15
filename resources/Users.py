from configs import is_in_prod
from flask_restful import Resource
from flask import jsonify
from services.UserService import *


class Users(Resource):

    def get(self, user_id=None):
        if is_in_prod():
            return 404

        if user_id:
            entry = get_user_entry(user_id)
            return jsonify(entry)

        entries = get_users_from_db()
        return jsonify(entries)
