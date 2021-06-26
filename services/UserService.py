from models.User import UserDocument
from mongoengine import ValidationError
from typing import List, Union, Optional
import random
import string

from utils.ActivityTypes import ACTIVITY_TYPES


def get_users_from_db() -> List[UserDocument]:
    return UserDocument.objects


def populate_user_db_entry(
    phone_number: str,
    display_name: Optional[str] = None
) -> UserDocument:
    if not display_name:
        letters = string.ascii_lowercase
        display_name = ''.join(random.choice(letters) for i in range(10))

    try:
        entry = UserDocument(
            display_name=display_name,
            phone_number=phone_number,
        )
        entry.save()
        return entry
    except ValidationError as e:
        raise e


def get_user_entry(user_id: str) -> Union[type(None), UserDocument]:
    entry = UserDocument.objects(id=user_id).first()
    return entry


def _get_user_by_phone_number(phone_number: str) -> Optional[UserDocument]:
    entry = UserDocument.objects(phone_number=phone_number).first()
    return entry


def validate_user_login(phone_number: str) -> Optional[UserDocument]:
    return _get_user_by_phone_number(phone_number)


def update_user_display_name(user_id: str, display_name: str):
    user = get_user_entry(user_id)
    user.update(set__display_name=display_name)


def update_user_preferences(user_id: str, preferences: List[int] = []) -> bool:
    user = get_user_entry(user_id)

    # Validate preferences
    preference_set = set(preferences)
    if len(preference_set) != len(preferences):
        return False

    for preference in preferences:
        if isinstance(preference, int) and 0 < preference < len(ACTIVITY_TYPES):
            pass
        else:
            return False

    user.update(set__preferences=preferences)
    return True