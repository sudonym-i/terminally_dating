import psycopg2
from psycopg2 import OperationalError
import argparse

# Define the database schema
SCHEMA1 = """
CREATE TABLE IF NOT EXISTS challenges (
    id SERIAL PRIMARY KEY,
    description TEXT,
    prompt1 TEXT,
    prompt2 TEXT
    );
"""

SCHEMA2 = """
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    message TEXT,
    sender TEXT,
    receiver TEXT,
    date_uploaded TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
"""

SCHEMA3 = """
CREATE TABLE IF NOT EXISTS answers (
    id SERIAL PRIMARY KEY,
    username TEXT,
    answer TEXT,
    problem_id INTEGER
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
            curr.execute(SCHEMA1)
            curr.execute(SCHEMA2)
            curr.execute(SCHEMA3)
        conn.commit()
    print("Help me")
    print(f"Initialized")

def add_challenge(args):
    desc = input("Enter a description").strip()
    prompt1 = input("Enter prompt 1.").strip()
    prompt2 = input("Enter prompt 2.").strip()
    with get_conn() as conn:
        with conn.cursor() as curr:
            curr.execute(
                "INSERT INTO challenges (description, prompt1, prompt2) VALUES (%s,%s,%s);",
                (desc, prompt1, prompt2)
            )
        conn.commit()
    print(f"Added challenge!")

def add_message(mess=None, send=None, rec=None):
    # Interactive mode if no parameters provided
    if mess is None:
        mess = input("Please Enter a message: ").strip()
    if send is None:
        send = input("Please Enter Sender Name: ").strip()
    if rec is None:
        rec = input("Please Enter the Name of the Receiver").strip()

    with get_conn() as conn:
        with conn.cursor() as curr:
            curr.execute(
                "INSERT INTO messages (message, sender, receiver) VALUES (%s,%s,%s);",
                (mess, send, rec)
            )
        conn.commit()
    print(f"{send} sent a message to {rec}.")

def add_answer(args):
    user = input("Please enter your name. ").strip()
    ans = input("Please enter your answer. ").strip()
    p_id = input("Please enter the id for the problem corresponding to the answer: ").input()
    with get_conn() as conn:
        with conn.cursor() as curr:
            curr.execute(
                "INSERT INTO tablesd (username, answer, problem_id) VALUES (%s,%s,%s);",
                (user, ans, p_id)
            )
        conn.commit()
    print(f"{user} added their answer to problem {p_id}") # Help me



def retrieve_problem(args):
    id = int(input("Challenge ID: ").strip())
    print("help" + str(id))
    with get_conn() as conn:
        print("help" + str(id))
        with conn.cursor() as curr:
            curr.execute("SELECT * FROM challenges WHERE id = %s;", (id,))
            info = curr.fetchone()
            print(f"Retrieved ID: {id}")
            return info
        
def retrieve_message(args):
    id = int(input("Message ID: ").strip())
    print("help" + str(id))
    with get_conn() as conn:
        print("help" + str(id))
        with conn.cursor() as curr:
            curr.execute("SELECT * FROM messages WHERE id = %s;", (id,))
            info = curr.fetchone()
            print(f"Retrieved ID: {id}")
            return info

def get_messages_between(user1, user2):
    """
    Retrieve all messages between two users.
    Returns list of tuples: (sender, message, timestamp)
    """
    try:
        with get_conn() as conn:
            with conn.cursor() as curr:
                curr.execute(
                    """SELECT sender, message, date_uploaded
                       FROM messages
                       WHERE (sender = %s AND receiver = %s)
                          OR (sender = %s AND receiver = %s)
                       ORDER BY date_uploaded ASC;""",
                    (user1, user2, user2, user1)
                )
                messages = curr.fetchall()
                # Convert to format expected by ChatUI: (sender, message, timestamp)
                formatted_messages = []
                for sender, message, timestamp in messages:
                    time_str = timestamp.strftime("%H:%M") if timestamp else "00:00"
                    formatted_messages.append((sender, message, time_str))
                return formatted_messages
    except Exception as e:
        print(f"Error loading messages: {e}")
        return []  # Return empty list if database fails
        
def retrieve_answers(args):
    id = int(input("Answers ID: ").strip())
    print("help" + str(id))
    with get_conn() as conn:
        print("help" + str(id))
        with conn.cursor() as curr:
            curr.execute("SELECT * FROM answers WHERE id = %s;", (id,))
            info = curr.fetchone()
            print(f"Retrieved ID: {id}")
            return info
        
def lookup(number):
    pp = "prompt" + str(number)
    with get_conn() as conn:
        with conn.cursor() as curr:
            curr.execute(f"SELECT {pp} FROM challenges WHERE challenges.id = 1")
            info = curr.fetchone()
            return info

def main():
    ap = argparse.ArgumentParser(description="SQLite terminal CLI")
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("init").set_defaults(func=init_db)
    sp.add_parser("add_c").set_defaults(func=add_challenge)
    sp.add_parser("add_m").set_defaults(func=add_message)
    sp.add_parser("add_a").set_defaults(func=add_answer)
    sp.add_parser("get_c").set_defaults(func=retrieve_problem)
    sp.add_parser("get_a").set_defaults(func=retrieve_answers)
    sp.add_parser("get_m").set_defaults(func=add_message)
    print(f"Added something :)")
    #num = input("Enter a player number")
    #print(lookup(num))



    args = ap.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()