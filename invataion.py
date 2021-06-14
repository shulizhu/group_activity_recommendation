import uuid
import datetime
import pymongo

class User(object):

    def __init__(self, user_name, phone_number, invitation_code_client):
        self.user_name = user_name
        self.phone_number = phone_number
        uid = str(uuid.uuid4())
        self.userID = ''.join(uid.split('-'))
        self.invitation_code_client = invitation_code_client

    def enter_invitation_code(self, invitation_code):
        if invitation_code is None or len(invitation_code) < 4:
            return "Invalid input"
        self.invitation_code_client.group_user(invitation_code, self)


class Group(object):
    def __init__(self, group_name, user):
        self.group_name = group_name
        uid = str(uuid.uuid4())
        self.groupId = ''.join(uid.split('-'))
        self.creator_name = user.user_name
        self.create_timestamp = datetime.datetime.now().timestamp()
        self.last_modified_timestamp = self.create_timestamp
        self.user_list = []
        self.invitationCode = self.groupId[:-4]


class InvitationCodeClient(object):

    relationshipMap = {}

    def __init__(self, relationship_map):
        self.relationship_map = relationship_map

    def group_user(self, invitation_code, user):
        if invitation_code not in self.relationshipMap.keys():
            return "Cannot find group via invitation code."
        temp_group = self.relationshipMap.get(invitation_code)
        temp_group.userList.append(user)
        user.currentGroupName = temp_group.groupName
        temp_group.lastModifiedTimestamp = datetime.datetime.now().timestamp()
        self.relationshipMap[invitation_code] = temp_group


