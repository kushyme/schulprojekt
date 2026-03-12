import sqlite3
import unittest


class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Datenbankverbindung einmalig vor allen Tests aufbauen."""
        cls.connection = sqlite3.connect("cheapshark.db")
        cls.cursor = cls.connection.cursor()


    @classmethod
    def tearDownClass(cls):
        """Datenbankverbindung nach allen Tests schliessen."""
        cls.connection.close()


    def test_01_tables_exist(self):
        """Stellt sicher, dass alle drei Tabellen existieren."""
        expected_tables = ["stores", "games", "deals"]
        for table in expected_tables:
            self.cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                (table,)
            )
            result = self.cursor.fetchone()
            self.assertIsNotNone(result, f"Tabelle '{table}' existiert nicht.")


    def test_02_stores_not_empty(self):
        """Stellt sicher, dass die Stores-Tabelle Eintraege enthaelt."""
        self.cursor.execute("SELECT COUNT(*) FROM stores")
        count = self.cursor.fetchone()[0]
        self.assertGreater(count, 0, "Stores-Tabelle ist leer.")


    def test_03_games_not_empty(self):
        """Stellt sicher, dass die Games-Tabelle Eintraege enthaelt."""
        self.cursor.execute("SELECT COUNT(*) FROM games")
        count = self.cursor.fetchone()[0]
        self.assertGreater(count, 0, "Games-Tabelle ist leer.")


    def test_04_deals_not_empty(self):
        """Stellt sicher, dass die Deals-Tabelle Eintraege enthaelt."""
        self.cursor.execute("SELECT COUNT(*) FROM deals")
        count = self.cursor.fetchone()[0]
        self.assertGreater(count, 0, "Deals-Tabelle ist leer.")


    def test_05_deals_have_valid_store_fk(self):
        """Stellt sicher, dass alle Deals eine gueltige storeID referenzieren."""
        self.cursor.execute("""
            SELECT COUNT(*) FROM deals
            WHERE storeID NOT IN (SELECT storeID FROM stores)
        """)
        invalid_count = self.cursor.fetchone()[0]
        self.assertEqual(invalid_count, 0, f"{invalid_count} Deals haben eine ungueltige storeID.")


    def test_06_deals_have_valid_game_fk(self):
        """Stellt sicher, dass alle Deals eine gueltige gameID referenzieren."""
        self.cursor.execute("""
            SELECT COUNT(*) FROM deals
            WHERE gameID NOT IN (SELECT gameID FROM games)
        """)
        invalid_count = self.cursor.fetchone()[0]
        self.assertEqual(invalid_count, 0, f"{invalid_count} Deals haben eine ungueltige gameID.")


    def test_07_no_duplicate_deals(self):
        """Stellt sicher, dass keine doppelten Deals existieren."""
        self.cursor.execute("""
            SELECT dealID, COUNT(*) as cnt FROM deals
            GROUP BY dealID
            HAVING cnt > 1
        """)
        duplicates = self.cursor.fetchall()
        self.assertEqual(len(duplicates), 0, f"{len(duplicates)} doppelte Deals gefunden.")


    def test_08_no_duplicate_stores(self):
        """Stellt sicher, dass keine doppelten Stores existieren."""
        self.cursor.execute("""
            SELECT storeID, COUNT(*) as cnt FROM stores
            GROUP BY storeID
            HAVING cnt > 1
        """)
        duplicates = self.cursor.fetchall()
        self.assertEqual(len(duplicates), 0, f"{len(duplicates)} doppelte Stores gefunden.")


if __name__ == "__main__":
    unittest.main(verbosity=2)