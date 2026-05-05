import requests
from uuid import UUID

BASE_URL = "http://localhost:1337"


def is_valid_uuid(value):
    try:
        UUID(value)
        return True
    except ValueError:
        return False


def handle_request_error(response):
    if response.status_code == 404:
        print("Ressource nicht gefunden.")
    elif response.status_code >= 500:
        print("Serverfehler bei der API.")
    else:
        print(f"API-Fehler: HTTP {response.status_code}")


def get_json(url):
    try:
        response = requests.get(url)
    except requests.RequestException:
        print("Verbindung zur API fehlgeschlagen.")
        return None

    if response.ok:
        return response.json()

    handle_request_error(response)
    return None


def study():
    decks = get_json(f"{BASE_URL}/decks")
    if decks is None:
        return

    if not decks:
        print("Keine Decks verfügbar.")
        return

    print("Verfügbare Decks:")
    for index, deck in enumerate(decks, start=1):
        print(f" [{index}] {deck.get('name', 'Unbenannt')} (ID: {deck.get('id')})")

    choice = input("Deck auswählen: ")
    if not choice.isdigit() or not (1 <= int(choice) <= len(decks)):
        print("Ungültige Auswahl.")
        return

    selected_deck = decks[int(choice) - 1]
    deck_id = selected_deck.get("id")

    flashcards = get_json(f"{BASE_URL}/decks/{deck_id}/flashcards")
    if flashcards is None:
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

    flashcard = get_json(f"{BASE_URL}/flashcards/{flashcard_uuid}")
    if flashcard is None:
        return

    current_question = flashcard.get("question", "")
    current_answer = flashcard.get("answer", "")

    print(f"Aktuelle Frage: {current_question}")
    new_question = input("Neue Frage (leer lassen = unverändert): ").strip()

    print(f"Aktuelle Antwort: {current_answer}")
    new_answer = input("Neue Antwort (leer lassen = unverändert): ").strip()

    payload = {
        "question": new_question if new_question else current_question,
        "answer": new_answer if new_answer else current_answer,
    }

    try:
        response = requests.put(f"{BASE_URL}/flashcards/{flashcard_uuid}", json=payload)
    except requests.RequestException:
        print("Verbindung zur API fehlgeschlagen.")
        return

    if response.ok:
        print("Flashcard erfolgreich aktualisiert.")
    else:
        handle_request_error(response)


def create_flashcard():
    decks = get_json(f"{BASE_URL}/decks")
    if decks is None:
        return

    if not decks:
        print("Keine Decks verfügbar.")
        return

    print("Verfügbare Decks:")
    for index, deck in enumerate(decks, start=1):
        print(f" [{index}] {deck.get('name', 'Unbenannt')} (ID: {deck.get('id')})")

    choice = input("Deck auswählen: ")
    if not choice.isdigit() or not (1 <= int(choice) <= len(decks)):
        print("Ungültige Auswahl.")
        return

    selected_deck = decks[int(choice) - 1]
    question = input("Frage eingeben: ").strip()
    answer = input("Antwort eingeben: ").strip()

    if not question or not answer:
        print("Frage und Antwort dürfen nicht leer sein.")
        return

    payload = {
        "deck_id": selected_deck.get("id"),
        "question": question,
        "answer": answer,
    }

    try:
        response = requests.post(f"{BASE_URL}/flashcards", json=payload)
    except requests.RequestException:
        print("Verbindung zur API fehlgeschlagen.")
        return

    if response.ok:
        print("Flashcard erfolgreich erstellt.")
    else:
        handle_request_error(response)


def delete_flashcard():
    flashcard_uuid = input("UUID der Flashcard: ").strip()
    if not is_valid_uuid(flashcard_uuid):
        print("Ungültige UUID.")
        return

    try:
        response = requests.delete(f"{BASE_URL}/flashcards/{flashcard_uuid}")
    except requests.RequestException:
        print("Verbindung zur API fehlgeschlagen.")
        return

    if response.ok:
        print("Flashcard erfolgreich gelöscht.")
    else:
        handle_request_error(response)


def edit_category():
    category_uuid = input("UUID der Category: ").strip()
    if not is_valid_uuid(category_uuid):
        print("Ungültige UUID.")
        return

    category = get_json(f"{BASE_URL}/categories/{category_uuid}")
    if category is None:
        return

    current_name = category.get("name", "")
    print(f"Aktueller Name: {current_name}")
    new_name = input("Neuer Name (leer lassen = unverändert): ").strip()

    payload = {
        "name": new_name if new_name else current_name
    }

    try:
        response = requests.put(f"{BASE_URL}/categories/{category_uuid}", json=payload)
    except requests.RequestException:
        print("Verbindung zur API fehlgeschlagen.")
        return

    if response.ok:
        print("Category erfolgreich aktualisiert.")
    else:
        handle_request_error(response)


def create_category():
    name = input("Name der neuen Category: ").strip()
    if not name:
        print("Der Name darf nicht leer sein.")
        return

    payload = {"name": name}

    try:
        response = requests.post(f"{BASE_URL}/categories", json=payload)
    except requests.RequestException:
        print("Verbindung zur API fehlgeschlagen.")
        return

    if response.ok:
        print("Category erfolgreich erstellt.")
    else:
        handle_request_error(response)


def delete_category():
    category_uuid = input("UUID der Category: ").strip()
    if not is_valid_uuid(category_uuid):
        print("Ungültige UUID.")
        return

    try:
        response = requests.delete(f"{BASE_URL}/categories/{category_uuid}")
    except requests.RequestException:
        print("Verbindung zur API fehlgeschlagen.")
        return

    if response.ok:
        print("Category erfolgreich gelöscht.")
    else:
        handle_request_error(response)


def show_flashcards():
    categories = get_json(f"{BASE_URL}/categories")
    if categories is None:
        return

    if not categories:
        print("Keine Categories verfügbar.")
        return

    print("Verfügbare Categories:")
    for index, category in enumerate(categories, start=1):
        print(f" [{index}] {category.get('name', 'Unbenannt')} (UUID: {category.get('uuid')})")

    choice = input("Category auswählen: ")
    if not choice.isdigit() or not (1 <= int(choice) <= len(categories)):
        print("Ungültige Auswahl.")
        return

    selected_category = categories[int(choice) - 1]
    category_uuid = selected_category.get("uuid")

    flashcards = get_json(f"{BASE_URL}/categories/{category_uuid}/flashcards")
    if flashcards is None:
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


def show_decks():
    categories = get_json(f"{BASE_URL}/categories")
    if categories is None:
        return

    if not categories:
        print("Keine Categories verfügbar.")
        return

    print("Alle Categories:")
    for category in categories:
        print("-" * 45)
        print(f"UUID: {category.get('uuid')}")
        print(f"Name: {category.get('name', 'Unbenannt')}")


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
    "3": create_flashcard,
    "4": delete_flashcard,
    "5": edit_category,
    "6": create_category,
    "7": delete_category,
    "8": show_flashcards,
    "9": show_decks,
}


def main():
    while True:
        print_menu()
        choice = input("    Auswahl: ")

        if choice == "0":
            print("Auf Wiedersehen!")
            break
        elif choice in ACTIONS:
            ACTIONS[choice]()
        else:
            print("Ungueltige Eingabe, bitte nochmal versuchen.")


if __name__ == "__main__":
    main()