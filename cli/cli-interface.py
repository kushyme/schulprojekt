import sys
from pathlib import Path

from bson.errors import InvalidId
from pymongo.errors import PyMongoError, ServerSelectionTimeoutError


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from mongodb.api import (  # noqa: E402
    MONGO_URI,
    add_flashcard,
    delete_flashcard,
    list_flashcards,
    ping,
    seed_test_dataset,
)


def print_menu():
    print()
    print("Flashcard CLI")
    print("1. Check MongoDB connection")
    print("2. List flashcards")
    print("3. Add flashcard")
    print("4. Delete flashcard")
    print("5. Seed test data")
    print("q. Quit")


def prompt_required(label):
    while True:
        value = input(f"{label}: ").strip()
        if value:
            return value

        print(f"{label} cannot be empty.")


def print_flashcard(card):
    print(f"{card['_id']} | [{card.get('deck', '')}] {card.get('front', '')} -> {card.get('back', '')}")


def check_connection():
    ping()
    print(f"Connected to {MONGO_URI}")


def show_flashcards():
    deck = input("Deck filter (leave empty for all): ").strip() or None
    cards = list_flashcards(deck)

    if not cards:
        print("No flashcards found.")
        return

    for card in cards:
        print_flashcard(card)


def create_flashcard():
    front = prompt_required("Front")
    back = prompt_required("Back")
    deck = prompt_required("Deck")
    flashcard_id = add_flashcard(front, back, deck)
    print(f"Added flashcard {flashcard_id}")


def remove_flashcard():
    flashcard_id = prompt_required("Flashcard id")
    deleted_count = delete_flashcard(flashcard_id)

    if deleted_count:
        print("Deleted flashcard.")
    else:
        print("No flashcard found with that id.")


def seed_data():
    inserted_ids = seed_test_dataset()
    print(f"Seeded {len(inserted_ids)} test flashcards.")


def handle_choice(choice):
    if choice == "1":
        check_connection()
    elif choice == "2":
        show_flashcards()
    elif choice == "3":
        create_flashcard()
    elif choice == "4":
        remove_flashcard()
    elif choice == "5":
        seed_data()
    elif choice.lower() == "q":
        return False
    else:
        print("Unknown option.")

    return True


def main():
    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        try:
            if not handle_choice(choice):
                return 0
        except ServerSelectionTimeoutError:
            print("Could not connect to MongoDB. Run mongodb/initiate-db.py first.")
        except InvalidId:
            print("That is not a valid MongoDB id.")
        except PyMongoError as e:
            print("MongoDB error:", e)
        except KeyboardInterrupt:
            print()
            return 0


if __name__ == "__main__":
    sys.exit(main())
