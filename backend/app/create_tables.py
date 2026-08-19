from .db import get_conn

def init_db():
    conn = get_conn()
    conn.row_factory = None    # optional: no dict rows needed here
    cur = conn.cursor()

    # ----------------------
    # Users table (with password)
    # ----------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT,
      email TEXT UNIQUE,
      password TEXT,           -- store plain password for mini-project
      home_airport TEXT,
      monthly_salary REAL,
      monthly_savings REAL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS user_preferences (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER,
      themes TEXT,
      usual_budget REAL,
      trip_length_days INTEGER,
      FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # ----------------------
    # Block R - Group Travel Tables
    # ----------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS groups (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT,
      trip_city TEXT,
      trip_start_date TEXT,
      trip_end_date TEXT,
      owner_user_id INTEGER
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS group_members (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      group_id INTEGER,
      user_id INTEGER,
      role TEXT,
      FOREIGN KEY(group_id) REFERENCES groups(id),
      FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("✅ DB initialized (users, preferences, groups, group_members)")
