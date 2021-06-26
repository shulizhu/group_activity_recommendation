from mongoengine import Document, EmbeddedDocument, IntField, EmbeddedDocumentField, StringField, ListField, LazyReferenceField, FloatField, DateTimeField

from models.User import UserDocument
from utils.ActivityTypes import ACTIVITY_TYPES


class GroupActivityEntryDocument(EmbeddedDocument):
    activity_type = IntField(
        db_field='activityType',
        required=True,
        min_value=0,
        max_value=len(ACTIVITY_TYPES)-1
    )
    activity_score = FloatField(
        db_field='activityScore',
        required=True,
        min_value=0
    )

class GroupDocument(Document):
    meta = {'collection': 'Groups'}
    display_name = StringField(required=True, db_field='displayName')
    invite_code = StringField(required=True, db_field='inviteCode')
    creator_id = LazyReferenceField(
        UserDocument,
        required=True,
        db_field='creatorId'
    )
    password_hash = StringField(required=True, db_field='passwordHash')
    created_time = DateTimeField(db_field='createdTime', required=True)
    expiry_time = DateTimeField(db_field='expiryTime', required=True)
    # Group preferences is a map where <key: activity enum, value: score>
    preferences = ListField(
        db_field='preferences',
        required=True,
        field=EmbeddedDocumentField(GroupActivityEntryDocument)
    )
    members = ListField(
        db_field='members',
        required=True,
        field=LazyReferenceField(UserDocument)
    )
