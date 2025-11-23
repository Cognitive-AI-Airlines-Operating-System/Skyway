import sqlite3

DB_PATH = "backend/app/skyway.db"  # adjust path if needed

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
