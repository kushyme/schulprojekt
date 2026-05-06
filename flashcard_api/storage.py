from pymongo import MongoClient
from pymongo.errors import PyMongoError

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "flashcard_app"


def get_db():
    client = MongoClient(MONGO_URI)
    return client[DB_NAME]


def error_response(message, status):
    return {
        "error": message,
        "status": status,
    }


def serialize_document(document):
    if document is None:
        return None

    serialized = dict(document)
    serialized.pop("_id", None)
    return serialized


def serialize_documents(documents):
    return [serialize_document(document) for document in documents]


def handle_db_error(error):
    return error_response(f"Datenbankfehler: {error}", 500)