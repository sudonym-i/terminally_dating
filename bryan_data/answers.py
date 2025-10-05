import sqlite3, argparse
import random, psycopg2

DB_PATH2 = "/Users/bryanholl/Documents/COMP_SCI_2025_2026/" \
          "Hackathon/terminally_dating/app.db"

# Define the database schema
SCHEMA2 = """
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

def get_db2(db_path=DB_PATH2):
    conn = sqlite3.connect(db_path) # Create a connection to the database
    return conn

def init_db2(args):
    with get_db(args.db) as conn:
        conn.executescript(SCHEMA2)
    print(f"Initialized {args.db}")

###########################################################################

DB_PATH = "users.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS Answers (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  answer      TEXT NOT NULL,
  usr_flag    INTEGER CHECK (usr_flag IN (1,2)) DEFAULT 1,
  user_id     INTEGER NOT NULL REFERENCES Users(id) ON DELETE CASCADE
);
"""

def get_db(db_path=DB_PATH):
    conn = sqlite3.connect(db_path) # Create a connection to the database
    return conn

def init_db(args):
    with get_db(args.db) as conn:
        conn.executescript(SCHEMA)
    print(f"Initialized {args.db}")

def list(args):
    with get_db(args.db) as conn:
        rows = conn.execute("""
            SELECT id, answer, usr_flag, user_id
            FROM Answers
            ORDER BY id DESC
        """
        ).fetchall()
    if not rows:
        print("(no answers)")
        return
    for r in rows:
        print(f"{r[0]:>3} | {r[1]:<20} | {r[2]:<28} | {r[3]} |")
    return rows

def return_answer(args):
    ans_id = int(input("Answer ID: ").strip())
    with get_db(args.db) as conn:
        row = conn.execute(
            "SELECT id, answer, usr_flag, user_id FROM Answers WHERE id = ?",
            (ans_id,)
        ).fetchone()
    if not row:
        print(f"(no answer with id {ans_id})")
        return
    print(f"{row[1]}")

def add_answer(args):
    answer = input("Answer: ").strip()
    usr_flag = determine_usr_flag()  # Func to det if user is 1 or 2
    user_id = int(input("User ID: ").strip())

    with get_db(args.db) as conn:
        try:
            conn.execute(
                "INSERT INTO Answers (answer, usr_flag, user_id) VALUES (?, ?, ?)",
                (answer, usr_flag, user_id),
            )
            print(f"Added answer for user ID {user_id}")
        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")

def determine_usr_flag():
    return random.choice([1, 2])

def main():
    ap = argparse.ArgumentParser(description="SQLite terminal CLI")
    ap.add_argument("--db", default=str(DB_PATH), help="Path to SQLite " \
    "database file")
    sp = ap.add_subparsers(dest="cmd", required=True)

    sp.add_parser("init").set_defaults(func=init_db)
    sp.add_parser("answer").set_defaults(func=add_answer)
    sp.add_parser("init2").set_defaults(func=init_db2)
    sp.add_parser("list").set_defaults(func=list)
    sp.add_parser("return").set_defaults(func=return_answer)
    
    # parse args and call the appropriate function
    args = ap.parse_args()
    args.func(args)
    

if __name__ == "__main__":
    main()
    