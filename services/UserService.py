from models.User import UserDocument
from typing import List, Union


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
    entry = UserDocument.objects(resource_code=user_id).first()
    return entry
