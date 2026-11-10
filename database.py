import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name('sales.db')


def connect(db_path=DB_PATH):
    return sqlite3.connect(db_path)


def initialize(db_path=DB_PATH):
    with connect(db_path) as con:
        con.execute('''CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY,
            sale_date TEXT NOT NULL,
            category TEXT NOT NULL,
            product TEXT NOT NULL,
            quantity INTEGER NOT NULL CHECK(quantity > 0),
            unit_price REAL NOT NULL CHECK(unit_price >= 0)
        )''')


def seed_demo(db_path=DB_PATH):
    from datetime import date, timedelta
    categories = {'Clothing': ['Jeans', 'Jacket', 'T-shirt'], 'Accessories': ['Bag', 'Belt', 'Scarf'], 'Shoes': ['Sneakers', 'Boots', 'Flats']}
    rows = []
    for day in range(90):
        d = (date(2026, 8, 1) + timedelta(days=day)).isoformat()
        for ci, (category, products) in enumerate(categories.items()):
            for pi, product in enumerate(products):
                if (day + ci * 2 + pi) % 4 != 0:
                    quantity = 1 + (day * 3 + ci + pi) % 5
                    price = 12 + ci * 9 + pi * 7
                    rows.append((d, category, product, quantity, float(price)))
    with connect(db_path) as con:
        if con.execute('SELECT COUNT(*) FROM sales').fetchone()[0] == 0:
            con.executemany('INSERT INTO sales (sale_date, category, product, quantity, unit_price) VALUES (?, ?, ?, ?, ?)', rows)
    return len(rows)
