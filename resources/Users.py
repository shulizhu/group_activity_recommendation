from authentication.MobileAuth import verify_phone_number
from configs import is_in_prod
from flask import jsonify, Response, request
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, set_access_cookies
from flask_restful import Resource
from flask import jsonify
from services.UserService import *


class Users(Resource):

    @jwt_required()
    def get(self, user_id=None):
        """
        :param user_id: user id
        :return: a JSON object representing a particular user
        """
        if user_id:
            # Verify that the logged-in user id matches the one the user is
            # is requesting.
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

    def post(self):
        phone_number = request.json.get('phoneNumber', None)
        otp = request.json.get('otp', None)

        if not phone_number or not otp:
            return Response(response='Incomplete sign-up request', status=400)

        verify_status = verify_phone_number(phone_number, otp)

        if verify_status != 'approved':
            return Response(response='Cannot fulfill request', status=400)

        user = validate_user_login(phone_number)

        if user:
            return Response(
                response='User with phone number exists. Please log in instead',
                status=401
            )

        user = populate_user_db_entry(phone_number=phone_number)

        user_id = str(user.id)
        access_token = create_access_token(identity=user_id)

        response = jsonify({'userId': user_id})
        set_access_cookies(response, access_token)

        return response
