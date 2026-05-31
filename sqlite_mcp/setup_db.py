"""Create and populate a local SQLite database with random sample data.

Schema:
  - customers(id, name, email, city, signup_date)
  - products(id, name, category, price, stock)
  - orders(id, customer_id, product_id, quantity, total, order_date)

Usage:
  python sqlite_mcp/setup_db.py
  python sqlite_mcp/setup_db.py --db /tmp/store.db --reset
"""

from __future__ import annotations

import argparse
import random
import sqlite3
from datetime import date, timedelta
from pathlib import Path

DEFAULT_DB = Path(__file__).parent / "store.db"

FIRST_NAMES = [
    "Alice",
    "Bob",
    "Carol",
    "David",
    "Eve",
    "Frank",
    "Grace",
    "Henry",
    "Ivy",
    "Jack",
    "Kate",
    "Leo",
    "Maya",
    "Noah",
    "Olivia",
    "Paul",
    "Quinn",
    "Ruth",
    "Sam",
    "Tina",
]
LAST_NAMES = [
    "Smith",
    "Johnson",
    "Williams",
    "Brown",
    "Jones",
    "Garcia",
    "Miller",
    "Davis",
    "Rodriguez",
    "Martinez",
    "Lee",
    "Walker",
    "Hall",
    "Allen",
]
CITIES = [
    "New York",
    "San Francisco",
    "Chicago",
    "Austin",
    "Seattle",
    "Boston",
    "Denver",
    "Miami",
    "Portland",
    "Atlanta",
]

PRODUCTS = [
    ("Wireless Mouse", "Electronics", 25.99, 120),
    ("Mechanical Keyboard", "Electronics", 89.50, 60),
    ("USB-C Hub", "Electronics", 34.00, 200),
    ("Noise-Cancelling Headphones", "Electronics", 199.99, 45),
    ("Standing Desk", "Furniture", 349.00, 15),
    ("Office Chair", "Furniture", 219.00, 25),
    ("Desk Lamp", "Furniture", 39.99, 80),
    ("Notebook", "Stationery", 4.50, 500),
    ("Pen Set", "Stationery", 12.00, 300),
    ("Coffee Mug", "Kitchen", 9.99, 250),
    ("Water Bottle", "Kitchen", 14.50, 180),
    ("Yoga Mat", "Fitness", 29.95, 70),
]


def create_schema(conn: sqlite3.Connection) -> None:
    conn.executescript("""
        CREATE TABLE customers (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            name         TEXT    NOT NULL,
            email        TEXT    NOT NULL UNIQUE,
            city         TEXT,
            signup_date  TEXT    NOT NULL
        );

        CREATE TABLE products (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            name      TEXT    NOT NULL,
            category  TEXT    NOT NULL,
            price     REAL    NOT NULL,
            stock     INTEGER NOT NULL DEFAULT 0
        );

        CREATE TABLE orders (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL REFERENCES customers(id),
            product_id  INTEGER NOT NULL REFERENCES products(id),
            quantity    INTEGER NOT NULL,
            total       REAL    NOT NULL,
            order_date  TEXT    NOT NULL
        );
        """)


def seed(
    conn: sqlite3.Connection, *, num_customers: int = 25, num_orders: int = 80
) -> None:
    rng = random.Random(42)
    today = date.today()

    customers = []
    used_emails: set[str] = set()
    for _ in range(num_customers):
        first = rng.choice(FIRST_NAMES)
        last = rng.choice(LAST_NAMES)
        name = f"{first} {last}"
        base = f"{first}.{last}".lower()
        email = f"{base}@example.com"
        suffix = 1
        while email in used_emails:
            suffix += 1
            email = f"{base}{suffix}@example.com"
        used_emails.add(email)
        city = rng.choice(CITIES)
        signup = today - timedelta(days=rng.randint(0, 365 * 2))
        customers.append((name, email, city, signup.isoformat()))

    conn.executemany(
        "INSERT INTO customers (name, email, city, signup_date) VALUES (?, ?, ?, ?)",
        customers,
    )

    conn.executemany(
        "INSERT INTO products (name, category, price, stock) VALUES (?, ?, ?, ?)",
        PRODUCTS,
    )

    customer_ids = [r[0] for r in conn.execute("SELECT id FROM customers")]
    products = list(conn.execute("SELECT id, price FROM products"))

    orders = []
    for _ in range(num_orders):
        cust_id = rng.choice(customer_ids)
        prod_id, price = rng.choice(products)
        qty = rng.randint(1, 5)
        total = round(price * qty, 2)
        order_date = today - timedelta(days=rng.randint(0, 180))
        orders.append((cust_id, prod_id, qty, total, order_date.isoformat()))

    conn.executemany(
        "INSERT INTO orders (customer_id, product_id, quantity, total, order_date) "
        "VALUES (?, ?, ?, ?, ?)",
        orders,
    )

    conn.commit()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--db", type=Path, default=DEFAULT_DB, help="Path to SQLite DB file"
    )
    parser.add_argument(
        "--reset", action="store_true", help="Delete existing DB before creating"
    )
    args = parser.parse_args()

    db_path: Path = args.db
    if db_path.exists():
        if args.reset:
            db_path.unlink()
        else:
            print(f"DB already exists at {db_path}. Use --reset to recreate.")
            return

    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        create_schema(conn)
        seed(conn)

    with sqlite3.connect(db_path) as conn:
        counts = {
            t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
            for t in ("customers", "products", "orders")
        }
    print(f"Created {db_path} with: {counts}")


if __name__ == "__main__":
    main()
