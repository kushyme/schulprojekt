import unittest
from api.fetch_data import (
    fetch_all_stores,
    fetch_all_deals,
    fetch_deal_by_id,
    fetch_games_by_title,
    fetch_game_by_id,
)


class TestApi(unittest.TestCase):


    def test_01_fetch_all_stores_returns_list(self):
        """Stellt sicher, dass fetch_all_stores eine Liste zurueckgibt."""
        result = fetch_all_stores()
        self.assertIsInstance(result, list)


    def test_02_fetch_all_stores_not_empty(self):
        """Stellt sicher, dass mindestens ein Store zurueckgegeben wird."""
        result = fetch_all_stores()
        self.assertGreater(len(result), 0, "Keine Stores zurueckgegeben.")


    def test_03_fetch_all_stores_has_required_fields(self):
        """Stellt sicher, dass jeder Store die erwarteten Felder enthaelt."""
        result = fetch_all_stores()
        for store in result:
            self.assertIn("storeID", store)
            self.assertIn("storeName", store)
            self.assertIn("isActive", store)


    def test_04_fetch_all_deals_returns_list(self):
        """Stellt sicher, dass fetch_all_deals eine Liste zurueckgibt."""
        result = fetch_all_deals(page_size=5)
        self.assertIsInstance(result, list)


    def test_05_fetch_all_deals_respects_page_size(self):
        """Stellt sicher, dass nicht mehr Deals zurueckgegeben werden als angefragt."""
        result = fetch_all_deals(page_size=5)
        self.assertLessEqual(len(result), 5)


    def test_06_fetch_all_deals_has_required_fields(self):
        """Stellt sicher, dass jeder Deal die erwarteten Felder enthaelt."""
        result = fetch_all_deals(page_size=5)
        for deal in result:
            self.assertIn("dealID", deal)
            self.assertIn("title", deal)
            self.assertIn("storeID", deal)
            self.assertIn("gameID", deal)
            self.assertIn("salePrice", deal)
            self.assertIn("normalPrice", deal)
            self.assertIn("savings", deal)


    def test_07_fetch_deal_by_id_returns_dict(self):
        """Stellt sicher, dass fetch_deal_by_id ein Dictionary zurueckgibt."""
        deals = fetch_all_deals(page_size=1)
        deal_id = deals[0]["dealID"]
        result = fetch_deal_by_id(deal_id)
        self.assertIsInstance(result, dict)


    def test_08_fetch_deal_by_id_has_required_fields(self):
        """Stellt sicher, dass der Deal-Detail die erwarteten Felder enthaelt."""
        deals = fetch_all_deals(page_size=1)
        deal_id = deals[0]["dealID"]
        result = fetch_deal_by_id(deal_id)
        self.assertIn("gameInfo", result)
        self.assertIn("cheapestPriceEver", result)


    def test_09_fetch_games_by_title_returns_list(self):
        """Stellt sicher, dass fetch_games_by_title eine Liste zurueckgibt."""
        result = fetch_games_by_title("batman")
        self.assertIsInstance(result, list)


    def test_10_fetch_games_by_title_not_empty(self):
        """Stellt sicher, dass die Suche nach 'batman' Ergebnisse liefert."""
        result = fetch_games_by_title("batman")
        self.assertGreater(len(result), 0, "Keine Games fuer 'batman' gefunden.")


    def test_11_fetch_games_by_title_has_required_fields(self):
        """Stellt sicher, dass jedes Game die erwarteten Felder enthaelt."""
        result = fetch_games_by_title("batman")
        for game in result:
            self.assertIn("gameID", game)
            self.assertIn("external", game)
            self.assertIn("cheapest", game)


    def test_12_fetch_games_by_title_results_match_query(self):
        """Stellt sicher, dass die Ergebnisse zum Suchbegriff passen."""
        result = fetch_games_by_title("batman")
        for game in result:
            title = game["external"].lower()
            self.assertIn("batman", title, f"'{game['external']}' enthaelt nicht 'batman'.")


    def test_13_fetch_game_by_id_returns_dict(self):
        """Stellt sicher, dass fetch_game_by_id ein Dictionary zurueckgibt."""
        games = fetch_games_by_title("batman")
        game_id = games[0]["gameID"]
        result = fetch_game_by_id(game_id)
        self.assertIsInstance(result, dict)


    def test_14_fetch_game_by_id_has_required_fields(self):
        """Stellt sicher, dass das Game-Detail die erwarteten Felder enthaelt."""
        games = fetch_games_by_title("batman")
        game_id = games[0]["gameID"]
        result = fetch_game_by_id(game_id)
        self.assertIn("info", result)
        self.assertIn("deals", result)
        self.assertIn("cheapest", result["info"])


if __name__ == "__main__":
    unittest.main(verbosity=2)