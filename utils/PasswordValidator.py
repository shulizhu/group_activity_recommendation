import re
import bcrypt
from typing import Optional, Tuple
from models.Group import GroupDocument


PASSWORD_PATTERN = re.compile('^[\S]{0,64}$', flags=re.ASCII)


def get_password_hash(password: str):
    is_password_valid = PASSWORD_PATTERN.match(password)
    if not is_password_valid:
        raise ValueError('Password is invalid, please re-enter.')
    password_hash = bcrypt.hashpw(password.encode('ascii'), bcrypt.gensalt(16))
    return password_hash


def validate_password(
    password: str,
    entry: Optional[GroupDocument] = None,
) -> Tuple[bool, Optional[GroupDocument]]:
    if not entry:
        return False, None

    password_checked = bcrypt.checkpw(
        password.encode('utf8'), entry.password_hash.encode('utf8'))

    return password_checked, entry if password_checked else None