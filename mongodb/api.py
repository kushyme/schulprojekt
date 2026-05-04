import os

import pymongo
from bson import ObjectId


MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DATABASE_NAME = "mydatabase"
FLASHCARD_COLLECTION = "flashcards"


TEST_FLASHCARDS = [
    {
        "front": "What is MongoDB?",
        "back": "A document database",
        "deck": "databases",
    },
    {
        "front": "What is a collection?",
        "back": "A group of MongoDB documents",
        "deck": "databases",
    },
    {
        "front": "What is pymongo?",
        "back": "The Python driver for MongoDB",
        "deck": "python",
    },
]


def get_client(uri=MONGO_URI, server_selection_timeout_ms=5000):
    return pymongo.MongoClient(uri, serverSelectionTimeoutMS=server_selection_timeout_ms)


def ping(client=None):
    if client is None:
        client = get_client()

        try:
            client.admin.command("ping")
        finally:
            client.close()

        return

    client.admin.command("ping")


def get_flashcards_collection(client):
    return client[DATABASE_NAME][FLASHCARD_COLLECTION]


def add_flashcard(front, back, deck):
    client = get_client()

    try:
        flashcards = get_flashcards_collection(client)
        result = flashcards.insert_one({"front": front, "back": back, "deck": deck})
        return result.inserted_id
    finally:
        client.close()


def list_flashcards(deck=None):
    client = get_client()

    try:
        flashcards = get_flashcards_collection(client)
        query = {"deck": deck} if deck else {}
        return list(flashcards.find(query))
    finally:
        client.close()


def get_flashcard(flashcard_id):
    client = get_client()

    try:
        flashcards = get_flashcards_collection(client)
        return flashcards.find_one({"_id": ObjectId(flashcard_id)})
    finally:
        client.close()


def delete_flashcard(flashcard_id):
    client = get_client()

    try:
        flashcards = get_flashcards_collection(client)
        result = flashcards.delete_one({"_id": ObjectId(flashcard_id)})
        return result.deleted_count
    finally:
        client.close()


def seed_test_dataset():
    client = get_client()

    try:
        ping(client)
        flashcards = get_flashcards_collection(client)
        flashcards.delete_many({})
        result = flashcards.insert_many(TEST_FLASHCARDS)
        return result.inserted_ids
    finally:
        client.close()
