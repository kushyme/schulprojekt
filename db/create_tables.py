import sqlite3

connection = sqlite3.connect("cheapshark.db")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS stores (
        storeID INTEGER PRIMARY KEY,
        storeName TEXT,
        isActive INTEGER
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS games (
        gameID INTEGER PRIMARY KEY,
        title TEXT,
        steamAppID TEXT,
        cheapestPrice TEXT
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS deals (
        dealID TEXT PRIMARY KEY,
        gameID INTEGER,
        storeID INTEGER,
        title TEXT,
        salePrice TEXT,
        normalPrice TEXT,
        savings TEXT,
        dealRating TEXT,
        thumb TEXT,
        FOREIGN KEY (gameID) REFERENCES games(gameID),
        FOREIGN KEY (storeID) REFERENCES stores(storeID)
    )
""")

connection.commit()

print("Tabellen wurden erfolgreich erstellt!")
print("  - stores")
print("  - games")
print("  - deals")

connection.close()