# write_mongo.py
from pymongo import MongoClient
from datetime import datetime, timezone

MONGO_URI = "mongodb://admin:secret123@localhost:27017"

client = MongoClient(MONGO_URI)

db = client["test"]
collection = db["luca"]

document = {
    "message": "Hallo MongoDB!",
    "created_at": datetime.now(timezone.utc),
}

result = collection.insert_one(document)

print(f"Eintrag geschrieben mit _id: {result.inserted_id}")

client.close()