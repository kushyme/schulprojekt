from pymongo.errors import PyMongoError

from .storage import get_db, error_response, serialize_documents, handle_db_error


def get_decks():
    try:
        db = get_db()
        decks = list(db.decks.find())
        return serialize_documents(decks)
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