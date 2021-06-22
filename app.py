import os
import json
import time
import pymongo
from bson.objectid import ObjectId
from authentication.jwt import initialize_jwt
from configs import ProductionConfig, DevelopmentConfig, is_in_prod
from database.db import initialize_db
from flask import request, Flask, jsonify
from flask_restful import Api
from resources.Sessions import Sessions
from resources.Users import Users
from utils.JsonEncoder import MongoEngineJsonEncoder
from flask_cors import *

import hashlib
import random

app = Flask(__name__)

config = ProductionConfig if is_in_prod() else DevelopmentConfig
app.config.from_object(config)

initialize_db(app)
initialize_jwt(app)
app.json_encoder = MongoEngineJsonEncoder

api = Api(app)

api.add_resource(Users, '/users', '/users/<string:user_id>')
api.add_resource(Sessions, '/sessions')


dbname = "data"
tbUser = "users"
tbGroup = "groups"

mydb = myclient[dbname]

userCol = mydb[tbUser]
groupCol = mydb[tbGroup]

tbname = ""
mycol = {}

def dbCol():
    global myclient, dbname, tbname
    mydb = myclient[dbname]
    return mydb[tbname]


def dbGetOne(param):
    global mycol
    mlist = mycol.find(param).limit(1)
    data = {}
    for r in mlist:
        data = r
        break
    return data


def dbGetList(param, num=0):
    global mycol
    if num > 0:
        return mycol.find(param).limit(num)
    else:
        return mycol.find(param)


def dbAdd(data):
    global mycol
    mycol.insert_one(data)


def dbUpdate(myquery, data):
    global mycol
    # myquery = { "url": url,"page": page }
    # newvalues = { "$set": { "isGet": val } }
    newvalues = {"$set": data}
    x = mycol.update_many(myquery, newvalues)
    return x.modified_count


def getRandomSet(bits):
    num_set = [chr(i) for i in range(48, 58)]
    char_set = [chr(i) for i in range(97, 123)]
    total_set = num_set + char_set
    value_set = str("".join(random.sample(total_set, bits)))
    return value_set


def getTime():
    return int(time.time())


def md5(data):
    return hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()


@app.after_request
def cors(environ):
    environ.headers['Access-Control-Allow-Origin'] = '*'
    environ.headers['Access-Control-Allow-Method'] = '*'
    environ.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return environ


@app.route('/')
def index():
    return 'api'


# Users


'''
PUT /users/:userId/preferences
Update the user’s activity preferences with a new set.

[
{activityType: x},
… ]
'''


@app.route('/users/<userId>/preferences', methods=['PUT'])
def setUsers(userId):
    global tbname, mycol
    res = "set user:" + str(userId)

    data = request.data
    arr = json.loads(data)

    print(arr)

    groupArr = []

    for r in arr:
        groupArr.append(r['activityType'])

    groupStr = "|".join(groupArr)

    tbname = "users"
    mycol = dbCol()
    param = {
        "_id": ObjectId(userId)
    }

    data = {
        "preference": groupStr
    }
    res = dbUpdate(param, data)


    if res:
        result = 'ok'
    else:
        result = 'no'

    return result


# Group
'''
Id
Invite Code
Display Name
Creator
Password hash
Password salt
Aggregate Preferences
Members


Id
Invite Code
Creator
(Password hash)
(Password salt)
Aggregate Preferences
Members
Timestamp
Expiry Time

'''

'''
    GET /group/:groupId
    Get the profile of a particular group.
'''


@app.route('/groups/<groupId>')
def getGroup(groupId):
    global tbname, mycol

    # print(groupId)

    try:
        id = ObjectId(groupId)
    except:
        id = ""

    tbname = "groups"
    mycol = dbCol()
    param = {
        "_id": id
    }

    # print(param)
    row = dbGetOne(param)
    # print(row)

    result = {}
    if len(row) > 0:
        result['id'] = str(row['_id'])
        result['displayName'] = row['displayName']

        result['password'] = row['password']
        result['passwordSalt'] = row['passwordSalt']

        result['inviteCode'] = row['inviteCode']
        result['creator'] = row['creator']

        result['timestamp'] = row['timestamp']
        result['expirytime'] = row['expirytime']

        result['members'] = row['members']
        result['preferences'] = row['preferences']

    return jsonify(result)


'''
    GET /groups?code=:inviteCode&pwd=:password
    Join a group with invite code and optional password and get the profile of the group.
'''


@app.route('/groups')
def joinGroups():
    global tbname, mycol

    code = str(request.args.get('code')).strip()
    pwd = str(request.args.get('pwd')).strip()

    uid = str(request.args.get('uid')).strip()

    print(code)
    print(pwd)

    tbname = "groups"
    mycol = dbCol()
    param = {
        "inviteCode": code
    }

    row = dbGetOne(param)
    print(row)

    if len(row) > 0:

        password = md5(pwd + row['passwordSalt'])
        print(password)

        if row['password'] == password:
            res = "inviteCode:" + code + " pass:" + pwd + " joinGroups  ok"

            if len(str(row['members'])) > 0:
                memberArr = str(row['members']).split("|")
            else:
                memberArr = []
            print(memberArr)
            if uid not in memberArr:
                memberArr.append(uid)

            members = "|".join(memberArr)

            data = {
                "members": members
            }
            dbUpdate(param, data)



        else:
            res = "Group password is wrong"
    else:
        res = "Group does not exist"
    return res


'''
PUT /groups
Create a group.

{ password: x }
'''


@app.route('/groups', methods=['POST'])
def group():
    global tbname, mycol

    data = request.data
    arr = json.loads(data)

    print(arr)

    tbname = "groups"
    mycol = dbCol()

    run = 1
    i = 0
    while run == 1:
        i += 1
        print("get inviteCode times:" + str(i))
        code = getRandomSet(4)

        param = {
            "inviteCode": code
        }
        res = dbGetOne(param)
        if len(res) == 0:
            run = 0
            break

    salt = getRandomSet(6)

    row = {}
    row['displayName'] = arr['displayName']
    row['password'] = md5(arr['password'] + salt)
    row['passwordSalt'] = salt

    row['inviteCode'] = code
    row['creator'] = arr['creator']

    row['timestamp'] = getTime()
    row['expirytime'] = getTime() + 86400

    row['members'] = arr['token']
    row['preferences'] = ""

    dbAdd(row)
    result = {}
    result['id'] = str(row['_id'])
    result['displayName'] = row['displayName']

    result['password'] = row['password']
    result['passwordSalt'] = row['passwordSalt']

    result['inviteCode'] = row['inviteCode']
    result['creator'] = row['creator']

    result['timestamp'] = row['timestamp']
    result['expirytime'] = row['expirytime']

    result['members'] = row['members']
    result['preferences'] = row['preferences']

    return jsonify(result)

if __name__ == '__main__':
    app.run()
