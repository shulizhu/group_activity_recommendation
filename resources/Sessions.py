from flask import Response
from flask_restful import request, Resource, reqparse
from flask_jwt_extended import create_access_token
from services.UserService import validate_user_login
from authentication.MobileAuth import send_otp, verify_phone_number


get_parser = reqparse.RequestParser()
get_parser.add_argument('for', type=str)


class Sessions(Resource):

    def get(self):
        args = get_parser.parse_args()
        phone_number = args.get('for', None)

        if not phone_number:
            return Response(response='Incomplete login request', status=400)

        send_otp(phone_number if phone_number[0] == '+' else '+' + phone_number)

        return Response(response='Success', status=200)

    def post(self):
        phone_number = request.json.get('phoneNumber', None)
        otp = request.json.get('otp', None)

        if not phone_number or not otp:
            return Response(response='Incomplete login request', status=400)

        verify_status = verify_phone_number(phone_number, otp)

        if verify_status != 'approved':
            return Response(response='Cannot fulfill request', status=400)

        user = validate_user_login(phone_number)

        if not user:
            return Response(
                response='No account found with input credentials',
                status=401
            )

        user_id = str(user.id)
        access_token = str(create_access_token(identity=user_id))

        return {
            'accessToken': access_token,
            'userId': user_id,
        }
