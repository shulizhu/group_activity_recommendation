from mongoengine import Document, StringField, ListField, IntField

from utils.ActivityTypes import ACTIVITY_TYPES


class UserDocument(Document):
    meta = {'collection': 'Users'}
    display_name = StringField(required=True, db_field='displayName')
    phone_number = StringField(
        required=True,
        db_field='phoneNumber',
        unique=True,
    )
    preferences = ListField(
        db_field='preferences',
        field=IntField(min_value=0, max_value=len(ACTIVITY_TYPES)-1)
    )
