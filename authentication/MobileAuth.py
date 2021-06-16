from app_secrets import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_VERIFY_SERVICE_ID
from configs import is_in_prod
from twilio.rest import Client


verify_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
_verify_service = verify_client.verify.services(TWILIO_VERIFY_SERVICE_ID)


def send_otp(phone_number: str):
    verification = _verify_service.verifications.create(
        to=phone_number,
        channel='sms'
    )

    if not is_in_prod():
        print(verification.status)

    return verification.status


def verify_phone_number(phone_number: str, otp: str) -> str:
    check = _verify_service.verification_checks.create(
        to=phone_number,
        code=otp
    )

    if not is_in_prod():
        print(check.status)

    return check.status