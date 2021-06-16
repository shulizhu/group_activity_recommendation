from models.User import UserDocument
from typing import List, Union, Optional


def get_users_from_db() -> List[UserDocument]:
    return UserDocument.objects


def populate_user_db_entry(display_name: str, phone_number: str) -> UserDocument:
    entry = UserDocument(
        display_name=display_name,
        phone_number=phone_number,
    )
    entry.save()
    return entry


def get_user_entry(user_id: str) -> Union[type(None), UserDocument]:
    entry = UserDocument.objects(id=user_id).first()
    return entry


def _get_user_by_phone_number(phone_number: str) -> Optional[UserDocument]:
    entry = UserDocument.objects(phone_number=phone_number).first()
    return entry


def validate_user_login(phone_number: str) -> Optional[UserDocument]:
    return _get_user_by_phone_number(phone_number)
