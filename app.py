import sqlite3, argparse

#DB_PATH = Path("app.db")
DB_PATH = "/Users/bryanholl/Documents/COMP_SCI_2025_2026/" \
"Hackathon/terminally_dating/app.db"

# Define the database schema
SCHEMA = """
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    age INTEGER,
    usr_location TEXT,
    bio TEXT,
    profile_link TEXT, -- Link to user's profile page on LinkedIn??
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

def get_db(db_path=DB_PATH):
    conn = sqlite3.connect(db_path) # Create a connection to the database
    return conn

def init_db(args):
    with get_db(args.db) as conn:
        conn.executescript(SCHEMA)
    print(f"Initialized {args.db}")

def add_user(args):
    username = input("Username: ").strip()
    email = input("Email: ").strip()
    age = int(input("Age: ").strip())
    usr_location = input("Location: ").strip()
    bio = input("Bio: ").strip()
    profile_link = input("Profile Link: ").strip()
    password_hash = input("Password Hash: ").strip()

    with get_db(args.db) as conn:
        try:
            conn.execute(
                "INSERT INTO Users"\
                "(usrnm,email,age,usr_location,bio,profile_link,password_hash)"\
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (username,email,age,usr_location,bio,profile_link,password_hash),
            )
            print(f"Added user {username}")
        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")

def list_users(args):
    with get_db(args.db) as conn:
        rows = conn.execute(
            "SELECT id, username, email, age, usr_location, " \
            "created_at FROM users ORDER BY id DESC"
        ).fetchall()
    if not rows:
        print("(no users)")
        return
    for r in rows:
        print(f"{r[0]:>3} | {r[1]:<20} | {r[2]:<28} | age={r[3]} | \
              {r[4]} | {r[5]}")
    return rows

def search_users(args):
    q = input("Username contains: ").strip() # or args.query
    with get_db(args.db) as conn:
        rows = conn.execute(
            "SELECT id, username, email FROM users WHERE username LIKE " \
            "? ORDER BY id",
            (f"%{q}%",),
        ).fetchall()
    for r in rows:
        print(f"{r[0]} | {r[1]} | {r[2]}")
    if not rows:
        print("(no matches)")
    return rows

def main():
    ap = argparse.ArgumentParser(description="SQLite terminal CLI")
    ap.add_argument("--db", default=str(DB_PATH), help="Path to SQLite " \
    "database file")
    sp = ap.add_subparsers(dest="cmd", required=True) # Needed?

    sp.add_parser("init").set_defaults(func=init_db)
    sp.add_parser("add").set_defaults(func=add_user)
    sp.add_parser("list").set_defaults(func=list_users)
    p_find = sp.add_parser("find").set_defaults(func=search_users)
    #p_find.add_argument("query", nargs="?")
    #p_find.set_defaults(func=search_users)

    # parse args and call the appropriate function
    args = ap.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()