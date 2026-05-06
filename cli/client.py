import os
import sys
from uuid import UUID

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from flashcard_api import (
    get_flashcard,
    create_flashcard,
    update_flashcard,
    delete_flashcard,
    get_decks,
    get_deck_flashcards,
    get_categories,
    get_category,
    get_category_flashcards,
    create_category,
    update_category,
    delete_category,
)


def is_valid_uuid(value):
    try:
        UUID(value)
        return True
    except ValueError:
        return False


def is_error_response(result):
    return isinstance(result, dict) and "error" in result and "status" in result


def print_error(result):
    if is_error_response(result):
        print(f"Fehler: {result['error']} (HTTP {result['status']})")
    else:
        print("Ein unbekannter Fehler ist aufgetreten.")


def study():
    decks = get_decks()

    if is_error_response(decks):
        print_error(decks)
        return

    if not decks:
        print("Keine Decks verfügbar.")
        return

    print("Verfügbare Decks:")
    for index, deck in enumerate(decks, start=1):
        print(f" [{index}] {deck.get('name', 'Unbenannt')} (UUID: {deck.get('uuid')})")

    choice = input("Deck auswählen: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(decks)):
        print("Ungültige Auswahl.")
        return

    selected_deck = decks[int(choice) - 1]
    deck_uuid = selected_deck["uuid"]

    flashcards = get_deck_flashcards(deck_uuid)

    if is_error_response(flashcards):
        print_error(flashcards)
        return

    if not flashcards:
        print("Dieses Deck enthält keine Flashcards.")
        return

    print(f"Lerne Deck: {selected_deck.get('name', 'Unbenannt')}")
    for index, card in enumerate(flashcards, start=1):
        print("=" * 45)
        print(f"Karte {index}/{len(flashcards)}")
        print(f"Frage: {card.get('question', '')}")
        input("Enter drücken zum Umdrehen...")
        print(f"Antwort: {card.get('answer', '')}")
        if index < len(flashcards):
            input("Enter drücken für die nächste Karte...")

    print("Alle Karten wurden durchgegangen.")


def edit_flashcard():
    flashcard_uuid = input("UUID der Flashcard: ").strip()
    if not is_valid_uuid(flashcard_uuid):
        print("Ungültige UUID.")
        return

    flashcard = get_flashcard(flashcard_uuid)
    if is_error_response(flashcard):
        print_error(flashcard)
        return

    current_question = flashcard.get("question", "")
    current_answer = flashcard.get("answer", "")

    print(f"Aktuelle Frage: {current_question}")
    new_question = input("Neue Frage (leer lassen = unverändert): ").strip()

    print(f"Aktuelle Antwort: {current_answer}")
    new_answer = input("Neue Antwort (leer lassen = unverändert): ").strip()

    updated_question = new_question if new_question else current_question
    updated_answer = new_answer if new_answer else current_answer

    result = update_flashcard(flashcard_uuid, updated_question, updated_answer)
    if is_error_response(result):
        print_error(result)
        return

    print("Flashcard erfolgreich aktualisiert.")


def create_flashcard_cli():
    decks = get_decks()

    if is_error_response(decks):
        print_error(decks)
        return

    if not decks:
        print("Keine Decks verfügbar.")
        return

    print("Verfügbare Decks:")
    for index, deck in enumerate(decks, start=1):
        print(f" [{index}] {deck.get('name', 'Unbenannt')} (UUID: {deck.get('uuid')})")

    choice = input("Deck auswählen: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(decks)):
        print("Ungültige Auswahl.")
        return

    selected_deck = decks[int(choice) - 1]
    question = input("Frage eingeben: ").strip()
    answer = input("Antwort eingeben: ").strip()

    if not question or not answer:
        print("Frage und Antwort dürfen nicht leer sein.")
        return

    result = create_flashcard(
        deck_id=selected_deck["uuid"],
        question=question,
        answer=answer,
    )
    if is_error_response(result):
        print_error(result)
        return

    print("Flashcard erfolgreich erstellt.")
    print(f"UUID: {result['uuid']}")


def delete_flashcard_cli():
    flashcard_uuid = input("UUID der Flashcard: ").strip()
    if not is_valid_uuid(flashcard_uuid):
        print("Ungültige UUID.")
        return

    result = delete_flashcard(flashcard_uuid)
    if is_error_response(result):
        print_error(result)
        return

    print("Flashcard erfolgreich gelöscht.")


def edit_category():
    category_uuid = input("UUID der Category: ").strip()
    if not is_valid_uuid(category_uuid):
        print("Ungültige UUID.")
        return

    category = get_category(category_uuid)
    if is_error_response(category):
        print_error(category)
        return

    current_name = category.get("name", "")
    print(f"Aktueller Name: {current_name}")
    new_name = input("Neuer Name (leer lassen = unverändert): ").strip()

    updated_name = new_name if new_name else current_name

    result = update_category(category_uuid, updated_name)
    if is_error_response(result):
        print_error(result)
        return

    print("Category erfolgreich aktualisiert.")


def create_category_cli():
    name = input("Name der neuen Category: ").strip()
    if not name:
        print("Der Name darf nicht leer sein.")
        return

    result = create_category(name)
    if is_error_response(result):
        print_error(result)
        return

    print("Category erfolgreich erstellt.")
    print(f"UUID: {result['uuid']}")


def delete_category_cli():
    category_uuid = input("UUID der Category: ").strip()
    if not is_valid_uuid(category_uuid):
        print("Ungültige UUID.")
        return

    result = delete_category(category_uuid)
    if is_error_response(result):
        print_error(result)
        return

    print("Category erfolgreich gelöscht.")


def show_flashcards():
    categories = get_categories()

    if is_error_response(categories):
        print_error(categories)
        return

    if not categories:
        print("Keine Categories verfügbar.")
        return

    print("Verfügbare Categories:")
    for index, category in enumerate(categories, start=1):
        print(f" [{index}] {category.get('name', 'Unbenannt')} (UUID: {category.get('uuid')})")

    choice = input("Category auswählen: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(categories)):
        print("Ungültige Auswahl.")
        return

    selected_category = categories[int(choice) - 1]
    category_uuid = selected_category["uuid"]

    flashcards = get_category_flashcards(category_uuid)

    if is_error_response(flashcards):
        print_error(flashcards)
        return

    if not flashcards:
        print("Keine Flashcards in dieser Category gefunden.")
        return

    print(f"Flashcards in Category: {selected_category.get('name', 'Unbenannt')}")
    for card in flashcards:
        print("-" * 45)
        print(f"UUID: {card.get('uuid')}")
        print(f"Frage: {card.get('question', '')}")
        print(f"Antwort: {card.get('answer', '')}")
        print(f"Deck UUID: {card.get('deck_id', '')}")


def show_decks():
    decks = get_decks()

    if is_error_response(decks):
        print_error(decks)
        return

    if not decks:
        print("Keine Decks verfügbar.")
        return

    print("Alle Decks:")
    for deck in decks:
        print("-" * 45)
        print(f"UUID: {deck.get('uuid')}")
        print(f"Name: {deck.get('name', 'Unbenannt')}")
        print(f"Category UUID: {deck.get('category_id', '')}")


def print_menu():
    print("Flashcard CLI - Hauptmenü")
    print(" [1] Lernen")
    print(" [2] Flashcard bearbeiten")
    print(" [3] Flashcard erstellen")
    print(" [4] Flashcard löschen")
    print(" [5] Kategorie erstellen")
    print(" [6] Kategorie bearbeiten")
    print(" [7] Kategorie löschen")
    print(" [8] Alle Flashcards anzeigen")
    print(" [9] Alle Decks anzeigen")
    print(" [0] Beenden")
    print("=" * 45)


ACTIONS = {
    "1": study,
    "2": edit_flashcard,
    "3": create_flashcard_cli,
    "4": delete_flashcard_cli,
    "5": create_category_cli,
    "6": edit_category,
    "7": delete_category_cli,
    "8": show_flashcards,
    "9": show_decks,
}


def main():
    while True:
        print_menu()
        choice = input("    Auswahl: ").strip()

        if choice == "0":
            print("Auf Wiedersehen!")
            break
        elif choice in ACTIONS:
            ACTIONS[choice]()
        else:
            print("Ungueltige Eingabe, bitte nochmal versuchen.")


if __name__ == "__main__":
    main()