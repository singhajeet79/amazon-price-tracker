import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path("tracker.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT UNIQUE,
        title TEXT,
        last_price REAL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS trackers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        target_price REAL,
        channel TEXT,
        contact TEXT,
        active INTEGER DEFAULT 1,
        FOREIGN KEY(product_id) REFERENCES products(id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS price_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        price REAL,
        checked_at TEXT,
        FOREIGN KEY(product_id) REFERENCES products(id)
    )
    """)

    conn.commit()
    conn.close()


# -------------------------
# PRODUCT OPERATIONS
# -------------------------

def get_or_create_product(url, title, price):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM products WHERE url=?", (url,))
    row = cur.fetchone()

    if row:
        product_id = row[0]
        cur.execute(
            "UPDATE products SET last_price=?, title=? WHERE id=?",
            (price, title, product_id)
        )
    else:
        cur.execute(
            "INSERT INTO products(url,title,last_price) VALUES (?,?,?)",
            (url, title, price)
        )
        product_id = cur.lastrowid

    conn.commit()
    conn.close()
    return product_id


# -------------------------
# TRACKER OPERATIONS
# -------------------------

def create_tracker(product_id, target_price, channel, contact):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO trackers(product_id,target_price,channel,contact)
        VALUES (?,?,?,?)
    """, (product_id, target_price, channel, contact))

    conn.commit()
    conn.close()


def get_active_trackers():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, product_id, target_price, channel, contact
        FROM trackers WHERE active=1
    """)

    rows = cur.fetchall()
    conn.close()
    return rows


def deactivate_tracker(tracker_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE trackers SET active=0 WHERE id=?",
        (tracker_id,)
    )

    conn.commit()
    conn.close()


# -------------------------
# PRICE HISTORY
# -------------------------

def record_price(product_id, price):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO price_history(product_id,price,checked_at)
        VALUES (?,?,?)
    """, (product_id, price, datetime.utcnow().isoformat()))

    conn.commit()
    conn.close()

# -------------------------
# QUERY TRACKERS BY CONTACT
# -------------------------

def get_trackers_by_contact(contact):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT t.id, p.title, p.last_price, t.target_price
        FROM trackers t
        JOIN products p ON t.product_id = p.id
        WHERE t.active=1 AND t.contact=?
    """, (contact,))

    rows = cur.fetchall()
    conn.close()
    return rows
