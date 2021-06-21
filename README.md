# group_activity_recommendation

1.Change the database username and password to your own.

2.Run python app.py (python>=3.6)

3.Start the MongoDB in your local PC.




Localhost url:
http://127.0.0.1:8080


Postman Example:
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
