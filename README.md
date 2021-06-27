# Group Act Back-end


## Project File Structure

### `app.py`

This is the entry point of the entire backend service. The file includes code that:

1. Initializes the server, the database, etc.
2. Registers RESTful resources and defines the endpoints.
3. Configures global settings.

### `/authentication`

This directory includes code that configures the environment for JWT tokens, which are used for managing logged-in user
sessions, and helper functions for the Twilio Mobile Auth flow.

### `/database`

This directory includes code that configures the MongoDB database. 

### `/models`

This directory contains schema definitions of the 2 types of data objects used in this project: **Users** and
**Groups**. These schema definitions match 1-to-1 with data document objects stored in the database (e.g. attribute
names, attribute types, and attribute properties). The schemas are written in an object-oriented fashion, with the help
of the `mongoengine` library. Each class attribute corresponds to a field of the data document object in the database.

### `/resources`

This directory contains all endpoint definitions (GET, PUT, POST, etc.) to manipulate the RESTful resources of the 
service.

### `/scripts`

This directory contains scripts for auto-deployment by AWS CodeDeploy. 

### `/services`

This directory contains a series of helper functions for manipulating database document object, organized by the type of
resource being manipulated on. For example, one of the services in this directory may include a function that populates
a new User entry in the database.

### `/utils`

This directory contains a set of utility functions for the application.


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

## Production Server and Deployment

The production back-end server is currently run on Amazon EC2 through Gunicorn, a Python WSGI (Web Server Gateway
Interface) HTTP server. An Nginx reverse proxy is then set up to redirect HTTP requests received from port 80 and HTTPS
requests received from port 443 to `127.0.0.1:8000`, the local port the Gunicorn server listens to.

Code is deployed with AWS CodeDeploy.


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
