def study():
    print("study")

def edit_flashcard():
    print("edit flashcard")

def create_flashcard():
    print("create flashcard")

def delete_flashcard():
    print("delete flashcard")

def edit_category():
    print("edit category")

def create_category():
    print("create category")

def delete_category():
    print("delete category")

def show_flashcards():
    print("show flashcards")

def show_decks():
    print("show decks")

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