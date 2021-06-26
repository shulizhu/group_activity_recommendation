from configs import is_in_prod
from flask import jsonify, Response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from services.GroupService import *


class Groups(Resource):

    @jwt_required()
    def get(self, group_id=None):
        """
        :param group_id: group id
        :return: a JSON object representing a particular group
        """

        if group_id:
            group = get_group_entry(group_id)

            if not group:
                return Response(response='Invalid Request', status=400)

            current_user_id = get_jwt_identity()

            if not is_user_in_group(current_user_id, group):
                return Response(response='Unauthorized Request', status=500)

            return jsonify(group)

        if is_in_prod():
            return Response(response='Invalid Request', status=400)
        else:
            entries = get_groups_from_db()
            return jsonify(entries)

    @jwt_required()
    def post(self):
        creator_id = get_jwt_identity()
        display_name = request.json.get('displayName', None)
        password = request.json.get('password', '')
        entry = populate_group_db_entry(creator_id, display_name, password)

        return jsonify(entry)

    @jwt_required()
    def patch(self):
        creator_id = get_jwt_identity()
        invite_code = request.json.get('inviteCode', '')
        password = request.json.get('password', '')
        entry = get_group_entry_by_invite_code(invite_code, password)
        if entry and join_group(creator_id, entry):
            return jsonify(entry)
        else:
            return Response(response='Unauthorized Request', status=500)

