import pymongo


#a test of my mongodb
client = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = client.mydb
collection = mydb.user
data1 = { "age" : 24 , "userName" : "zuofanixu" }
data2 = { "age" : 26 , "userName" : "yanghang" }
dblist = client.list_database_names()


collection.insert(data1)
collection.insert(data2)

result = collection.find()
print (result)