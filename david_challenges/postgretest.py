import psycopg2
from psycopg2 import OperationalError

def test_postgres_connection():
    try:
        # Update with your server details
        conn = psycopg2.connect(
            host="192.168.137.50",  # e.g., "localhost" or IP address
            database="mydatabase",
            user="terminally",
            password="dating",
            port=5432  # default PostgreSQL port
        )
        cursor = conn.cursor()
        
        # Simple test query
        cursor.execute("SELECT version();")
        cursor.execute("SELECT * FROM Users;")
        rows = cursor.fetchall()
        print(rows)
        db_version = cursor.fetchone()
        print("Connected successfully!")
        print("PostgreSQL version:", db_version)
        
        cursor.close()
        conn.close()
        
    except OperationalError as e:
        print(f"Could not connect to PostgreSQL server: {e}")

if __name__ == "__main__":
    test_postgres_connection()
