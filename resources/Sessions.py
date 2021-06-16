from configs import is_in_prod
from flask import Response
from flask_restful import request, Resource, reqparse
from services.UserService import validate_user_login
from app_secrets import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_VERIFY_SERVICE_ID
from twilio.rest import Client


get_parser = reqparse.RequestParser()
get_parser.add_argument('for', type=str)


class Sessions(Resource):

    def __init__(self):
        account_sid = TWILIO_ACCOUNT_SID
        auth_token = TWILIO_AUTH_TOKEN
        verify_service_id = TWILIO_VERIFY_SERVICE_ID
        verify_client = Client(account_sid, auth_token)
        self._verify_service = verify_client.verify.services(verify_service_id)

    def get(self):
        args = get_parser.parse_args()
        phone_number = args.get('for', None)

        if not phone_number:
            return Response(response='Incomplete login request', status=400)

        self._send_otp(phone_number)

        return Response(response='Success', status=200)

    def post(self):
        phone_number = request.json.get('phoneNumber', None)
        otp = request.json.get('otp', None)

        if not phone_number or not otp:
            return Response(response='Incomplete login request', status=400)

        verify_status = self._verify_phone_number(phone_number, otp)

        if verify_status != 'approved':
            return Response(response='Cannot fulfill request', status=400)

        user = validate_user_login(phone_number)

        if not user:
            return Response(
                response='No account found with input credentials',
                status=401
            )

        user_id = str(user.id)
        return {
            'userId': user_id,
        }

    def _send_otp(self, phone_number: str):
        verification = self._verify_service.verifications.create(
            to='+'+phone_number,
            channel='sms'
        )

        if not is_in_prod():
            print(verification.status)

        return verification.status

    def _verify_phone_number(self, phone_number: str, otp: str) -> str:
        check = self._verify_service.verification_checks.create(
            to=phone_number,
            code=otp
        )

        if not is_in_prod():
            print(check.status)

        return check.status
