from configs import is_in_prod
from flask import jsonify, Response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from services.UserService import *


class Users(Resource):

    @jwt_required()
    def get(self, user_id=None):
        if user_id:
            current_user_id = get_jwt_identity()
            if user_id == current_user_id:
                entry = get_user_entry(user_id)
                return jsonify(entry)

            else:
                return Response(response='Unauthorized Request', status=500)

        # Return all user profiles for testing purposes in dev environment.
        if is_in_prod():
            return Response(response='Invalid Request', status=400)
        else:
            entries = get_users_from_db()
            return jsonify(entries)
