from api.fetch_data import (
    fetch_all_stores,
    fetch_all_deals,
    fetch_deal_by_id,
    fetch_games_by_title,
    fetch_game_by_id,
    set_price_alert,
    delete_price_alert,
)
from db.insert_data import insert_stores, insert_deals, insert_games

def print_header(title):
    print("\n" + "=" * 45)
    print("  " + title)
    print("=" * 45)

def print_menu():
    print_header("CheapShark CLI - Hauptmenu")
    print("  [1]  Alle Stores anzeigen")
    print("  [2]  Aktuelle Deals anzeigen")
    print("  [3]  Deal per ID suchen")
    print("  [4]  Spiele per Titel suchen")
    print("  [5]  Spiel per ID suchen")
    print("  [6]  Preisalarm setzen")
    print("  [7]  Preisalarm loeschen")
    print("  [0]  Beenden")
    print("-" * 45)

def show_stores():
    print_header("STORES")
    stores = fetch_all_stores()
    insert_stores(stores)

    for store in stores:
        store_id = store["storeID"]
        store_name = store["storeName"]
        is_active = store["isActive"]

        if is_active == 1:
            status = "aktiv"
        else:
            status = "inaktiv"

        print("  [" + store_id + "] " + store_name + " - " + status)

def show_deals():
    anzahl = input("  Wie viele Deals? (z.B. 10): ")
    anzahl = int(anzahl)

    print_header("DEALS")
    deals = fetch_all_deals(page_size=anzahl)
    insert_deals(deals)

    for deal in deals:
        title = deal["title"]
        normal_price = deal["normalPrice"]
        sale_price = deal["salePrice"]
        deal_id = deal["dealID"]
        savings = deal["savings"]
        savings = float(savings)
        savings = round(savings)

        print("  " + title)
        print("  Normalpreis: $" + normal_price + "  Salepreis: $" + sale_price + "  Rabatt: " + str(savings) + "%")
        print("  Deal-ID: " + deal_id)
        print("")

def show_deal_by_id():
    deal_id = input("  Deal-ID eingeben: ")

    print_header("DEAL DETAIL")
    detail = fetch_deal_by_id(deal_id)

    if detail is None or len(detail) == 0:
        print("  Kein Deal gefunden.")
        return

    game_info = detail.get("gameInfo", {})
    cheapest = detail.get("cheapestPriceEver", {})

    name = game_info.get("name", "n/a")
    store_id = game_info.get("storeID", "n/a")
    sale_price = game_info.get("salePrice", "n/a")
    retail_price = game_info.get("retailPrice", "n/a")
    metacritic = game_info.get("metacriticScore", "n/a")
    steam_rating = game_info.get("steamRatingText", "n/a")
    steam_percent = game_info.get("steamRatingPercent", "n/a")
    cheapest_price = cheapest.get("price", "n/a")
    cheapest_date = cheapest.get("date", "n/a")

    print("  Titel: " + str(name))
    print("  Store-ID: " + str(store_id))
    print("  Aktueller Preis: $" + str(sale_price))
    print("  Normalpreis: $" + str(retail_price))
    print("  Metacritic: " + str(metacritic))
    print("  Steam-Rating: " + str(steam_rating) + " (" + str(steam_percent) + "%)")
    print("  Guenstigster Preis je: $" + str(cheapest_price) + " am " + str(cheapest_date))

def search_games_by_title():
    title = input("  Spieltitel eingeben: ")

    print_header("SPIELSUCHE - " + title)
    games = fetch_games_by_title(title)
    insert_games(games)

    for game in games:
        game_id = game["gameID"]
        name = game["external"]
        cheapest = game["cheapest"]

        print("  [" + str(game_id) + "] " + name + " - ab $" + str(cheapest))

def show_game_by_id():
    game_id = input("  Game-ID eingeben: ")

    print_header("SPIEL DETAIL - ID " + game_id)
    result = fetch_game_by_id(game_id)

    info = result["info"]
    deals = result["deals"]

    cheapest = info["cheapest"]
    steam_id = info["steamAppID"]

    print("  Guenstigster Preis: $" + str(cheapest))
    print("  Steam App ID: " + str(steam_id))
    print("  Anzahl Deals: " + str(len(deals)))
    print("  Deals:")

    for d in deals:
        store_id = d["storeID"]
        price = d["price"]
        rating = d["dealRating"]
        print("    Store " + str(store_id) + " - $" + str(price) + " (Rating: " + str(rating) + ")")

def create_alert():
    print_header("PREISALARM SETZEN")
    email = input("  E-Mail-Adresse: ")
    game_id = input("  Game-ID: ")
    price = input("  Zielpreis ($): ")

    set_price_alert(email, game_id, price)

def remove_alert():
    print_header("PREISALARM LOESCHEN")
    email = input("  E-Mail-Adresse: ")
    game_id = input("  Game-ID: ")

    delete_price_alert(email, game_id)

ACTIONS = {
    "1": show_stores,
    "2": show_deals,
    "3": show_deal_by_id,
    "4": search_games_by_title,
    "5": show_game_by_id,
    "6": create_alert,
    "7": remove_alert,
}

def main():
    print("Willkommen beim CheapShark CLI!")
    while True:
        print_menu()
        choice = input("  Auswahl: ")

        if choice == "0":
            print("Auf Wiedersehen!")
            break
        elif choice in ACTIONS:
            ACTIONS[choice]()
        else:
            print("Ungueltige Eingabe, bitte nochmal versuchen.")

if __name__ == "__main__":
    main()