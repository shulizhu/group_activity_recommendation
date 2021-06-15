from mongoengine import Document, StringField


class UserDocument(Document):
    meta = {'collection': 'Users'}
    display_name = StringField(required=True, db_field='displayName')
    phone_number = StringField(
        required=True,
        db_field='phoneNumber',
        unique=True,
    )
