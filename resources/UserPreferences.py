from flask_restful import Resource
from flask import Response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.UserService import *

class UserPreferences(Resource):

    @jwt_required
    def put(self, user_id=None):
        """
        :param user_id: user id
        :return: a JSON object representing a particular user
        """
        if not user_id:
            return Response(response='Invalid Request', status=400)

        # Verify that the logged-in user id matches the one the user is
        # is requesting.
        current_user_id = get_jwt_identity()
        if user_id == current_user_id:
            preferences = request.json.get('preferences', None)
            valid = update_user_preferences(user_id, preferences)
            if valid:
                return Response(response='OK', status=200)
            else:
                return Response(response='Invalid Request', status=400)
        else:
            return Response(response='Unauthorized Request', status=500)