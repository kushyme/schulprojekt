import uuid

from pymongo.errors import PyMongoError

from .storage import (
    get_db,
    error_response,
    serialize_document,
    serialize_documents,
    handle_db_error,
)


def get_categories():
    try:
        db = get_db()
        categories = list(db.categories.find())
        return serialize_documents(categories)
    except PyMongoError as error:
        return handle_db_error(error)


def get_category(category_uuid):
    try:
        db = get_db()

        category = db.categories.find_one({"uuid": category_uuid})
        if category is None:
            return error_response("Not found", 404)

        return serialize_document(category)
    except PyMongoError as error:
        return handle_db_error(error)


def get_category_flashcards(category_uuid):
    try:
        db = get_db()

        category = db.categories.find_one({"uuid": category_uuid})
        if category is None:
            return error_response("Category not found", 404)

        flashcards = list(db.flashcards.find({"category_id": category_uuid}))
        return serialize_documents(flashcards)
    except PyMongoError as error:
        return handle_db_error(error)


def create_category(name):
    if not name:
        return error_response("Missing required fields", 400)

    try:
        db = get_db()

        category = {
            "uuid": str(uuid.uuid4()),
            "name": name,
        }

        db.categories.insert_one(category)
        return category
    except PyMongoError as error:
        return handle_db_error(error)


def update_category(category_uuid, name):
    if not name:
        return error_response("Missing required fields", 400)

    try:
        db = get_db()

        existing = db.categories.find_one({"uuid": category_uuid})
        if existing is None:
            return error_response("Not found", 404)

        db.categories.update_one(
            {"uuid": category_uuid},
            {
                "$set": {
                    "name": name,
                }
            },
        )

        updated = db.categories.find_one({"uuid": category_uuid})
        return serialize_document(updated)
    except PyMongoError as error:
        return handle_db_error(error)


def delete_category(category_uuid):
    try:
        db = get_db()

        category = db.categories.find_one({"uuid": category_uuid})
        if category is None:
            return error_response("Not found", 404)

        db.categories.delete_one({"uuid": category_uuid})
        db.decks.delete_many({"category_id": category_uuid})
        db.flashcards.delete_many({"category_id": category_uuid})

        return serialize_document(category)
    except PyMongoError as error:
        return handle_db_error(error)