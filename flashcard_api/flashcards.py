import uuid

from pymongo.errors import PyMongoError

from .storage import get_db, error_response, serialize_document, handle_db_error


def get_flashcard(flashcard_uuid):
    try:
        db = get_db()
        flashcard = db.flashcards.find_one({"uuid": flashcard_uuid})

        if flashcard is None:
            return error_response("Not found", 404)

        return serialize_document(flashcard)
    except PyMongoError as error:
        return handle_db_error(error)


def create_flashcard(deck_id, question, answer):
    if not deck_id or not question or not answer:
        return error_response("Missing required fields", 400)

    try:
        db = get_db()

        deck = db.decks.find_one({"uuid": deck_id})
        if deck is None:
            return error_response("Deck not found", 404)

        flashcard = {
            "uuid": str(uuid.uuid4()),
            "question": question,
            "answer": answer,
            "deck_id": deck_id,
        }

        db.flashcards.insert_one(flashcard)
        return flashcard
    except PyMongoError as error:
        return handle_db_error(error)


def update_flashcard(flashcard_uuid, question, answer):
    if not question or not answer:
        return error_response("Missing required fields", 400)

    try:
        db = get_db()

        existing = db.flashcards.find_one({"uuid": flashcard_uuid})
        if existing is None:
            return error_response("Not found", 404)

        db.flashcards.update_one(
            {"uuid": flashcard_uuid},
            {
                "$set": {
                    "question": question,
                    "answer": answer,
                }
            },
        )

        updated = db.flashcards.find_one({"uuid": flashcard_uuid})
        return serialize_document(updated)
    except PyMongoError as error:
        return handle_db_error(error)


def delete_flashcard(flashcard_uuid):
    try:
        db = get_db()

        flashcard = db.flashcards.find_one({"uuid": flashcard_uuid})
        if flashcard is None:
            return error_response("Not found", 404)

        db.flashcards.delete_one({"uuid": flashcard_uuid})
        return serialize_document(flashcard)
    except PyMongoError as error:
        return handle_db_error(error)