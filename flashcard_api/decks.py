import uuid

from pymongo.errors import PyMongoError

from .storage import (
    get_db,
    error_response,
    serialize_document,
    serialize_documents,
    handle_db_error,
)


def get_decks():
    try:
        db = get_db()
        decks = list(db.decks.find())
        return serialize_documents(decks)
    except PyMongoError as error:
        return handle_db_error(error)


def get_deck(deck_uuid):
    try:
        db = get_db()

        deck = db.decks.find_one({"uuid": deck_uuid})
        if deck is None:
            return error_response("Deck not found", 404)

        return serialize_document(deck)
    except PyMongoError as error:
        return handle_db_error(error)


def get_deck_flashcards(deck_uuid):
    try:
        db = get_db()

        deck = db.decks.find_one({"uuid": deck_uuid})
        if deck is None:
            return error_response("Deck not found", 404)

        flashcards = list(db.flashcards.find({"deck_id": deck_uuid}))
        return serialize_documents(flashcards)
    except PyMongoError as error:
        return handle_db_error(error)


def create_deck(name):
    if not name:
        return error_response("Missing required fields", 400)

    try:
        db = get_db()

        deck = {
            "uuid": str(uuid.uuid4()),
            "name": name,
        }

        db.decks.insert_one(deck)
        return deck
    except PyMongoError as error:
        return handle_db_error(error)


def update_deck(deck_uuid, name):
    if not name:
        return error_response("Missing required fields", 400)

    try:
        db = get_db()

        existing = db.decks.find_one({"uuid": deck_uuid})
        if existing is None:
            return error_response("Deck not found", 404)

        db.decks.update_one(
            {"uuid": deck_uuid},
            {
                "$set": {
                    "name": name,
                }
            },
        )

        updated = db.decks.find_one({"uuid": deck_uuid})
        return serialize_document(updated)
    except PyMongoError as error:
        return handle_db_error(error)


def delete_deck(deck_uuid):
    try:
        db = get_db()

        deck = db.decks.find_one({"uuid": deck_uuid})
        if deck is None:
            return error_response("Deck not found", 404)

        db.decks.delete_one({"uuid": deck_uuid})
        db.flashcards.delete_many({"deck_id": deck_uuid})

        return serialize_document(deck)
    except PyMongoError as error:
        return handle_db_error(error)