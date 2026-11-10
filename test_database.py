import sqlite3
import tempfile
import unittest
from pathlib import Path
from database import initialize, seed_demo


class DatabaseTests(unittest.TestCase):
    def test_seed_is_repeatable_and_does_not_duplicate(self):
        with tempfile.TemporaryDirectory() as folder:
            db = Path(folder) / 'test.db'
            initialize(db)
            seed_demo(db)
            with sqlite3.connect(db) as con:
                first = con.execute('SELECT COUNT(*) FROM sales').fetchone()[0]
                revenue = con.execute('SELECT SUM(quantity * unit_price) FROM sales').fetchone()[0]
            seed_demo(db)
            with sqlite3.connect(db) as con:
                second = con.execute('SELECT COUNT(*) FROM sales').fetchone()[0]
            self.assertGreater(first, 0)
            self.assertGreater(revenue, 0)
            self.assertEqual(first, second)

    def test_database_rejects_invalid_quantity(self):
        with tempfile.TemporaryDirectory() as folder:
            db = Path(folder) / 'test.db'
            initialize(db)
            with sqlite3.connect(db) as con:
                with self.assertRaises(sqlite3.IntegrityError):
                    con.execute("INSERT INTO sales (sale_date,category,product,quantity,unit_price) VALUES ('2026-08-01','Shoes','Boots',0,25)")


if __name__ == '__main__':
    unittest.main()
