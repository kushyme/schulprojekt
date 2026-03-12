import sqlite3

connection = sqlite3.connect("cheapshark.db")
cursor = connection.cursor()

def insert_stores(stores):
    for store in stores:
        store_id = store["storeID"]
        store_name = store["storeName"]
        is_active = store["isActive"]

        cursor.execute("""
            INSERT OR IGNORE INTO stores (storeID, storeName, isActive)
            VALUES (?, ?, ?)
        """, (store_id, store_name, is_active))

    connection.commit()
    print("Stores eingefuegt: " + str(len(stores)))

def insert_deals(deals):
    for deal in deals:
        deal_id = deal["dealID"]
        title = deal["title"]
        store_id = deal["storeID"]
        game_id = deal["gameID"]
        sale_price = deal["salePrice"]
        normal_price = deal["normalPrice"]
        savings = deal["savings"]
        deal_rating = deal["dealRating"]
        thumb = deal["thumb"]

        cursor.execute("""
            INSERT OR IGNORE INTO games (gameID, title)
            VALUES (?, ?)
        """, (game_id, title))

        cursor.execute("""
            INSERT OR IGNORE INTO deals (dealID, gameID, storeID, title, salePrice, normalPrice, savings, dealRating, thumb)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (deal_id, game_id, store_id, title, sale_price, normal_price, savings, deal_rating, thumb))

    connection.commit()
    print("Deals eingefuegt: " + str(len(deals)))

def insert_games(games):
    for game in games:
        game_id = game["gameID"]
        name = game["external"]
        cheapest = game["cheapest"]

        steam_app_id = ""
        if "steamAppID" in game:
            steam_app_id = game["steamAppID"]

        cursor.execute("""
            INSERT OR IGNORE INTO games (gameID, title, steamAppID, cheapestPrice)
            VALUES (?, ?, ?, ?)
        """, (game_id, name, steam_app_id, cheapest))

    connection.commit()
    print("Games eingefuegt: " + str(len(games)))