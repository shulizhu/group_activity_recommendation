from mongoengine import ValidationError
from typing import List, Union, Optional
import random
import string
import datetime
from random import choices as random_choices
from bson import ObjectId

from models.Group import GroupDocument, GroupActivityEntryDocument
from utils.PasswordValidator import *
from services.UserService import get_user_entry
from utils.ActivityTypes import ACTIVITY_TYPES


def get_groups_from_db() -> List[GroupDocument]:
    return GroupDocument.objects


def populate_group_db_entry(
    creator_id: str,
    display_name: Optional[str] = None,
    password: Optional[str] = '',
) -> GroupDocument:
    if not display_name:
        letters = string.ascii_lowercase
        display_name = ''.join(random.choice(letters) for i in range(10))

    try:
        password_hash = get_password_hash(password)
        created_time = datetime.datetime.utcnow()
        expiry_time = created_time + datetime.timedelta(hours=1)
        user = get_user_entry(creator_id)
        group_preferences = _merge_group_preferences(user.preferences, [])
        entry = GroupDocument(
            display_name=display_name,
            invite_code=generate_invite_code(),
            creator_id=ObjectId(creator_id),
            password_hash=password_hash,
            created_time=created_time,
            expiry_time=expiry_time,
            preferences=group_preferences,
            members=[ObjectId(creator_id)],
        )
        entry.save()
        return entry
    except ValidationError as e:
        raise e
    except ValueError as e:
        raise e


def get_group_entry(group_id: str) -> Union[type(None), GroupDocument]:
    entry = GroupDocument.objects(id=group_id).first()
    return entry


def get_group_entry_by_invite_code(
    invite_code: str,
    password: Optional[str] = ''
) -> Union[type(None), GroupDocument]:
    entry = GroupDocument.objects(invite_code=invite_code).first()
    if validate_password(password, entry):
        return entry
    else:
        return None


def is_user_in_group(user_id: str, group: GroupDocument) -> bool:
    return ObjectId(user_id) in group.members


def get_random_code(code_length):
    num_set = [chr(i) for i in range(48, 58)]
    char_set = [chr(i) for i in range(97, 123)]
    choices = num_set + char_set
    code = "".join(random_choices(choices, k=code_length))
    return code


def generate_invite_code():
    code = get_random_code(4)
    while get_group_entry_by_invite_code(code):
        code = get_random_code(4)
    return code


def join_group(user_id: str, group: GroupDocument) -> bool:
    user = get_user_entry(user_id)
    if not user:
        return False

    if is_user_in_group(user):
        return True
    else:
        new_group_preferences = _merge_group_preferences(
            user.preferences, group.preferences)
        group.update(push__members=ObjectId(user_id))
        group.update(set__preferences=new_group_preferences)
        return True


# TODO add group preferences merging logic.
def _merge_group_preferences(
    user_preferences: List[int],
    group_preferences: List[GroupActivityEntryDocument]
):
    return []