#!/usr/bin/env python3
import os
import argparse
import random
import psycopg2
from psycopg2 import errors  # for FK/unique violations

# Use env var or edit this string:
PG_DSN = os.getenv(
    "DATABASE_URL",
    "//terminally:dating@192.168.137.50:5432/mydatabase"
)

DDL_USERS = """
CREATE TABLE IF NOT EXISTS users (
    id            BIGSERIAL PRIMARY KEY,
    username      TEXT NOT NULL UNIQUE,
    email         TEXT NOT NULL UNIQUE,
    age           INTEGER,
    usr_location  TEXT,
    bio           TEXT,
    profile_link  TEXT,
    password_hash TEXT NOT NULL,
    created_at    TIMESTAMPTZ DEFAULT NOW()
);
"""

DDL_ANSWERS = """
CREATE TABLE IF NOT EXISTS answers (
    id        BIGSERIAL PRIMARY KEY,
    answer    TEXT NOT NULL,
    usr_flag  INTEGER CHECK (usr_flag IN (1,2)) DEFAULT 1,
    user_id   BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE
);
"""

def get_conn(dsn: str):
    return psycopg2.connect(dsn)

# ---------- commands ----------
def init_db(args):
    with get_conn(args.dsn) as conn:
        with conn.cursor() as cur:
            cur.execute(DDL_USERS)
            cur.execute(DDL_ANSWERS)
    print("✅ Initialized schema (users, answers).")

def add_user(args):
    username = input("Username: ").strip()
    email = input("Email: ").strip()
    age_txt = input("Age (optional): ").strip()
    loc = input("Location (optional): ").strip()
    bio = input("Bio (optional): ").strip()
    link = input("Profile link (optional): ").strip()
    pw_hash = input("Password hash (demo only): ").strip()  # hash before storing in real apps

    age = int(age_txt) if age_txt else None

    with get_conn(args.dsn) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO users (username, email, age, usr_location, bio, profile_link, password_hash)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (username) DO NOTHING
                RETURNING id
                """,
                (username, email, age, loc or None, bio or None, link or None, pw_hash),
            )
            row = cur.fetchone()
            if row:
                print(f"✅ Created user id={row[0]}")
            else:
                print("ℹ️  Username already exists; no insert.")

def list_users(args):
    with get_conn(args.dsn) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, username, email, age, usr_location, created_at
                FROM users
                ORDER BY id DESC
                LIMIT 100
            """)
            rows = cur.fetchall()
    if not rows:
        print("(no users)")
        return
    for r in rows:
        print(f"{r[0]:>3} | {r[1]:<18} | {r[2]:<28} | age={r[3]!s:<3} | {r[4] or ''} | {r[5]}")

def determine_usr_flag():
    return random.choice([1, 2])

def add_answer(args):
    answer = input("Answer: ").strip()
    usr_flag = determine_usr_flag()
    user_id = int(input("User ID: ").strip())

    try:
        with get_conn(args.dsn) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO answers (answer, usr_flag, user_id) VALUES (%s, %s, %s) RETURNING id",
                    (answer, usr_flag, user_id),
                )
                ans_id = cur.fetchall()[0]
                print(f"✅ Added answer id={ans_id} for user_id={user_id}")
    except errors.ForeignKeyViolation:
        print("❌ Invalid user_id (no such user).")
    except psycopg2.IntegrityError as e:
        print(f"❌ Integrity error: {e}")

def list_answers(args):
    with get_conn(args.dsn) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, answer, usr_flag, user_id
                FROM answers
                ORDER BY id DESC
            """)
            rows = cur.fetchall()
    if not rows:
        print("(no answers)")
        return
    for r in rows:
        print(f"{r[0]:>3} | {r[1]:<40.40} | flag={r[2]} | user_id={r[3]}")

def show_answer(args):
    ans_id = int(input("Answer ID: ").strip())
    with get_conn(args.dsn) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, answer, usr_flag, user_id FROM answers WHERE id = %s",
                (ans_id,),
            )
            row = cur.fetchone()
    if not row:
        print(f"(no answer with id {ans_id})")
        return
    print(row[1])

# ---------- CLI wiring ----------
def main():
    ap = argparse.ArgumentParser(description="PostgreSQL terminal CLI")
    ap.add_argument("--dsn", default=PG_DSN, help="Postgres DSN (postgresql://user:pass@host:port/db)")
    sp = ap.add_subparsers(dest="cmd", required=True)

    sp.add_parser("init").set_defaults(func=init_db)
    sp.add_parser("add-user").set_defaults(func=add_user)
    sp.add_parser("list-users").set_defaults(func=list_users)
    sp.add_parser("answer").set_defaults(func=add_answer)
    sp.add_parser("list-answers").set_defaults(func=list_answers)
    sp.add_parser("show-answer").set_defaults(func=show_answer)

    args = ap.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()