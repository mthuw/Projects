from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client.wearables
collection = db.raw
collection.insert_one({"test": 1})

print("Database and collection created!")