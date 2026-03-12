from api.fetch_data import (
    fetch_all_stores,
    fetch_all_deals,
    fetch_deal_by_id,
    fetch_games_by_title,
    fetch_game_by_id,
)
 
def main():
    # 1. Alle Stores abrufen
    print("=" * 40)
    print("STORES")
    print("=" * 40)
    stores = fetch_all_stores()
    for store in stores:
        status = "✅ aktiv" if store.get("isActive") == 1 else "❌ inaktiv"
        print(f"  [{store.get('storeID')}] {store.get('storeName')} – {status}")
 
    # 2. Deals abrufen
    print("\n" + "=" * 40)
    print("DEALS (Top 5)")
    print("=" * 40)
    deals = fetch_all_deals(page_size=5)
    for deal in deals:
        print(f"  {deal.get('title')}")
        print(f"    Normal: ${deal.get('normalPrice')}  →  Sale: ${deal.get('salePrice')}  ({float(deal.get('savings', 0)):.0f}% Rabatt)")
 
    # 3. Einzelnen Deal abrufen
    if deals:
        first_deal_id = deals[0].get("dealID")
        print("\n" + "=" * 40)
        print(f"DEAL DETAIL – {deals[0].get('title')}")
        print("=" * 40)
        detail = fetch_deal_by_id(first_deal_id)
        cheapest_ever = detail.get("cheapestPriceEver", {})
        print(f"  Günstigster Preis je: ${cheapest_ever.get('price')} (am {cheapest_ever.get('date')})")
 
    # 4. Spiele suchen
    print("\n" + "=" * 40)
    print("SPIELSUCHE – 'batman'")
    print("=" * 40)
    games = fetch_games_by_title("batman")
    for game in games[:5]:
        print(f"  [{game.get('gameID')}] {game.get('external')} – ab ${game.get('cheapest')}")
 
    # 5. Einzelnes Spiel abrufen
    if games:
        first_game_id = games[0].get("gameID")
        print("\n" + "=" * 40)
        print(f"SPIEL DETAIL – {games[0].get('external')}")
        print("=" * 40)
        game_detail = fetch_game_by_id(first_game_id)
        if game_detail:
            info = game_detail.get("info", {})
            print(f"  Günstigster Preis: ${info.get('cheapest')}")
            print(f"  Steam App ID:      {info.get('steamAppID', 'n/a')}")
            print(f"  Anzahl Deals:      {len(game_detail.get('deals', []))}")
            print("  Deals:")
            for d in game_detail.get("deals", []):
                print(f"    Store {d.get('storeID')} – ${d.get('price')} (Rating: {d.get('dealRating')})")
 
if __name__ == "__main__":
    main()