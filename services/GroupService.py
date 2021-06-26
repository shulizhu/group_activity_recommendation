from mongoengine import ValidationError
from typing import List, Union, Optional
import random
import string
import datetime
from random import choices as random_choices

from models.Group import GroupDocument
from utils.PasswordValidator import *
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
        entry = GroupDocument(
            display_name=display_name,
            invite_code=generate_invite_code(),
            creator_id=creator_id,
            password_hash=password_hash,
            created_time=created_time,
            expiry_time=expiry_time,
            # TODO add preferences insertion logic.
            preferences=[],
            members=[creator_id],
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
    invite_code: str) -> Union[type(None), GroupDocument]:
    entry = GroupDocument.objects(invite_code=invite_code).first()
    return entry


def is_user_in_group(user_id: str, group_id: str) -> bool:
    group = get_group_entry(group_id)

    if not group:
        return False
    return user_id in group.members


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
