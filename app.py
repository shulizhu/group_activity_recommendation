from authentication.jwt import initialize_jwt
from configs import ProductionConfig, DevelopmentConfig, is_in_prod
from database.db import initialize_db
from flask import request, Flask
from flask_restful import Api
from resources.Sessions import Sessions
from resources.Users import Users
from resources.UserPreferences import UserPreferences
from resources.Groups import Groups
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
api.add_resource(
    UserPreferences,
    '/users',
    '/users/<string:user_id>',
    '/users/<string:user_id>/preferences'
)
api.add_resource(Sessions, '/sessions')
api.add_resource(Groups, '/groups', '/groups/<string:group_id>')


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

# Group

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

if __name__ == '__main__':
    app.run()
