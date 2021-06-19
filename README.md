# Group Act Back-end

## Runtime Environment Setup

There are 2 runtime environments defined for this project: `dev`, and `prod`. 

1. In the `dev` environment, the server runs locally and is connected to a local database. There are also more endpoints
   available in the dev environment for testing purposes.
2. In the `prod` environment, the server can be running locally or remotely on the cloud, but in either case it is
   connected to a remote database. Endpoints for testing purposes will not be available in this environment.

**Prod is the default environment.** This makes deployment easier, but also means that you must properly set up your
local environment in order to run the server & the database locally. The recommended coding environment for this project
is PyCharm. To start with, set up two "Run/Debug Configuration" for the project: one for dev, and one for prod. In both
configs, point the target to `app.py`, and for the dev config, set `FLASK_ENV` to `development`.


## Flask App Configuration

There are 2 separate flask app configs meant for the dev and the prod environment respectively, and both of them can be
found under `configs.py`. This file references keys from a file `app_secrets.py` that is intentionally made not to be
included in the repo for obvious security considerations. In your local directory, create `app_secrets.py` in the
project's root directory as shown below:

```python
# MongoDb related secrets
DATABASE_USERNAME = 'group_act_backend'
DATABASE_PASSWORD = '<secret>'
DATABASE_GROUP_ACT_HOSTNAME_PROD = '<remote_location>'
DATABASE_GROUP_ACT_HOSTNAME_DEV = '<local_location>'

# Flask related secrets
FLASK_APP_SECRET_KEY = '<secret>'

# Twilio related secrets
TWILIO_ACCOUNT_SID = '<secret>'
TWILIO_AUTH_TOKEN = '<secret>'
TWILIO_VERIFY_SERVICE_ID = '<secret>'

# JWT related secrets
JWT_SECRET_KEY = '<secret>'
```

You may ask the team members for the database password and the secret key for the app. 

**DO NOT UPLOAD `app_secrets.py`**

## Production and Deployment

The production back-end server is currently run on Amazon EC2 through Gunicorn. 

## Postman Example:

GET
http://127.0.0.1:8080/groups/60ca89d65d06bf46ec80b915

GET
http://127.0.0.1:8080/groups?code=tmyr&pwd=123456

POST
http://127.0.0.1:8080/groups

BODY
{"displayName": "mygroyp","password": "123456","token": "123"}

GET
http://127.0.0.1:8080/users/60ca7c15a6be39f30ef0249d

PUT
http://127.0.0.1:8080/users/60ca7c15a6be39f30ef0249d/preferences
BODY
[{"activityType": "hiking"}]

POST
http://127.0.0.1:8080/users

BODY
{"displayName": "Lucy","phoneNumber": "4326548873"}
