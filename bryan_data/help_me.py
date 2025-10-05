import psycopg2
from psycopg2 import OperationalError
import argparse


# Define the database schema
SCHEMA = """
CREATE TABLE IF NOT EXISTS tablesd (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    age INTEGER,
    usr_location TEXT,
    bio TEXT,
    profile_link TEXT,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
    );
"""

def get_conn():
    # Update with your server details
    conn = psycopg2.connect(
        host="192.168.137.50",  # e.g., "localhost" or IP address
        database="mydatabase",
        user="terminally",
        password="dating",
        port=5432  # default PostgreSQL port
    )
    return conn

def init_db(args):
    print("Help")
    with get_conn() as conn:
        with conn.cursor() as curr:
            curr.execute(SCHEMA)
        conn.commit()
    print("Help me")
    print(f"Initialized")

def add_user(args):
    username = input("Username: ").strip()
    email = input("Email: ").strip()
    age = int(input("Age: ").strip())
    usr_location = input("Location: ").strip()
    bio = input("Bio: ").strip()
    profile_link = input("Profile Link: ").strip()
    password_hash = input("Password Hash: ").strip()
    user_font = input("User Font: ").strip()
    with open("../ascii_stuff/output.txt", "r") as f:
        user_pict = f.read()
    with get_conn() as conn:
        with conn.cursor() as curr:
            curr.execute(
                "INSERT INTO tablesd (username,email,age,usr_location,bio,profile_link,password_hash,font,pict) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);",
                (username,email,age,usr_location,bio,profile_link,password_hash,user_font,user_pict)
            )
        conn.commit()
    print(f"Added user: {username}")

def retrieve_usr(args):
    usr_id = 3
    print("help" + str(usr_id))
    with get_conn() as conn:
        print("help" + str(usr_id))
        with conn.cursor() as curr:
            curr.execute("SELECT * FROM tablesd WHERE id = %s;", (usr_id,))
            info = curr.fetchone()
            print(f"Retrieved user ID: {usr_id}")
            return info

def main():
    ap = argparse.ArgumentParser(description="SQLite terminal CLI")
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("init").set_defaults(func=init_db)
    sp.add_parser("add").set_defaults(func=add_user)
    sp.add_parser("get").set_defaults(func=retrieve_usr)
    with get_conn() as conn:
        with conn.cursor() as curr:
            curr.execute("ALTER TABLE tablesd ADD COLUMN pict TEXT;")
        conn.commit()
    print(f"Added font :)")



    args = ap.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()