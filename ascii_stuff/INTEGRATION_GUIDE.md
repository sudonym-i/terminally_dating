# Database Integration Guide
# Step-by-Step Guide to Connect Frontend to PostgreSQL

This guide walks you through integrating the terminal dating application frontend with a PostgreSQL database backend.

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Project Structure](#project-structure)
3. [Database Layer Implementation](#database-layer-implementation)
4. [Modifying Existing Code](#modifying-existing-code)
5. [Authentication System](#authentication-system)
6. [Testing the Integration](#testing-the-integration)
7. [Deployment Checklist](#deployment-checklist)

---

## Prerequisites

### Required Software
- Python 3.8+
- PostgreSQL 12+
- pip (Python package manager)

### Required Python Packages

Create a `requirements.txt` file:

```text
pyfiglet==0.8.post1
ascii-magic==2.3.0
psycopg2-binary==2.9.9
python-dotenv==1.0.0
bcrypt==4.1.2
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### PostgreSQL Setup

1. Install PostgreSQL on your system
2. Create database and user (see DATABASE_SCHEMA.md)
3. Run the schema creation scripts

---

## Project Structure

Recommended project structure after integration:

```
terminally_dating/
├── ascii_stuff/
│   ├── UI.py                    # Frontend UI (modify for DB)
│   ├── chat.py                  # Chat UI (modify for DB)
│   ├── image_to_ascii_art.py    # Image processing (no changes)
│   ├── test.py                  # Test file (modify for DB)
│   ├── db/
│   │   ├── __init__.py
│   │   ├── connection.py        # Database connection management
│   │   ├── models.py            # Database models/queries
│   │   └── migrations.sql       # Database schema
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── auth.py              # Authentication logic
│   │   └── session.py           # Session management
│   ├── config/
│   │   ├── __init__.py
│   │   └── config.py            # Configuration management
│   ├── .env                     # Environment variables (DO NOT COMMIT)
│   ├── .env.example             # Example environment file
│   ├── requirements.txt         # Python dependencies
│   └── main.py                  # New main application file
```

---

## Database Layer Implementation

### Step 1: Create Database Connection Module

Create `db/connection.py`:

```python
"""
Database connection management module.
Handles connection pooling and database initialization.
"""

import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseConnection:
    """Manages PostgreSQL database connections with connection pooling."""

    _pool = None

    @classmethod
    def initialize(cls):
        """Initialize the connection pool."""
        if cls._pool is None:
            try:
                cls._pool = pool.SimpleConnectionPool(
                    minconn=1,
                    maxconn=20,
                    host=os.getenv('DB_HOST', 'localhost'),
                    database=os.getenv('DB_NAME', 'dating_app'),
                    user=os.getenv('DB_USER'),
                    password=os.getenv('DB_PASSWORD'),
                    port=int(os.getenv('DB_PORT', 5432))
                )
                print("Database connection pool initialized successfully")
            except Exception as e:
                print(f"Error initializing database pool: {e}")
                raise

    @classmethod
    def get_connection(cls):
        """
        Get a connection from the pool.

        Returns:
            psycopg2.connection: Database connection
        """
        if cls._pool is None:
            cls.initialize()
        return cls._pool.getconn()

    @classmethod
    def return_connection(cls, connection):
        """
        Return a connection to the pool.

        Args:
            connection: Database connection to return
        """
        if cls._pool is not None:
            cls._pool.putconn(connection)

    @classmethod
    def close_all(cls):
        """Close all connections in the pool."""
        if cls._pool is not None:
            cls._pool.closeall()
            cls._pool = None
            print("All database connections closed")


def get_db():
    """
    Context manager for database connections.

    Usage:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
    """
    conn = DatabaseConnection.get_connection()
    try:
        yield conn
    finally:
        DatabaseConnection.return_connection(conn)
```

### Step 2: Create Database Models Module

Create `db/models.py`:

```python
"""
Database models and query functions.
Provides high-level interface for database operations.
"""

from psycopg2.extras import RealDictCursor
from db.connection import DatabaseConnection


class UserModel:
    """Database operations for users table."""

    @staticmethod
    def get_by_id(user_id):
        """
        Get user profile by ID.

        Args:
            user_id (int): User ID

        Returns:
            dict: User profile data or None
        """
        conn = DatabaseConnection.get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute('''
                    SELECT id, user_name, name_font, bio, github, profile_pic, created_at
                    FROM users WHERE id = %s AND is_active = TRUE
                ''', (user_id,))
                return cursor.fetchone()
        finally:
            DatabaseConnection.return_connection(conn)

    @staticmethod
    def get_by_username(username):
        """Get user by username."""
        conn = DatabaseConnection.get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute('''
                    SELECT id, user_name, email, password_hash, name_font, bio, github, profile_pic
                    FROM users WHERE user_name = %s AND is_active = TRUE
                ''', (username,))
                return cursor.fetchone()
        finally:
            DatabaseConnection.return_connection(conn)

    @staticmethod
    def create(user_name, email, password_hash, name_font='starwars', bio='', github='', profile_pic=''):
        """
        Create new user.

        Returns:
            int: New user ID
        """
        conn = DatabaseConnection.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO users (user_name, email, password_hash, name_font, bio, github, profile_pic)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                ''', (user_name, email, password_hash, name_font, bio, github, profile_pic))
                user_id = cursor.fetchone()[0]
                conn.commit()
                return user_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            DatabaseConnection.return_connection(conn)

    @staticmethod
    def update_profile(user_id, user_name=None, name_font=None, bio=None, github=None, profile_pic=None):
        """
        Update user profile fields.

        Args:
            user_id (int): User ID to update
            **kwargs: Fields to update
        """
        conn = DatabaseConnection.get_connection()
        try:
            updates = []
            params = []

            if user_name is not None:
                updates.append("user_name = %s")
                params.append(user_name)
            if name_font is not None:
                updates.append("name_font = %s")
                params.append(name_font)
            if bio is not None:
                updates.append("bio = %s")
                params.append(bio)
            if github is not None:
                updates.append("github = %s")
                params.append(github)
            if profile_pic is not None:
                updates.append("profile_pic = %s")
                params.append(profile_pic)

            if not updates:
                return

            updates.append("updated_at = CURRENT_TIMESTAMP")
            params.append(user_id)

            query = f"UPDATE users SET {', '.join(updates)} WHERE id = %s"

            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            DatabaseConnection.return_connection(conn)

    @staticmethod
    def get_next_profile(current_user_id):
        """
        Get next profile to display (random, not already seen).

        Args:
            current_user_id (int): Current logged-in user

        Returns:
            dict: Profile data or None
        """
        conn = DatabaseConnection.get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute('''
                    SELECT id, user_name, name_font, bio, github, profile_pic
                    FROM users
                    WHERE id != %s
                      AND is_active = TRUE
                      AND id NOT IN (
                        SELECT target_user_id FROM matches WHERE user_id = %s
                      )
                    ORDER BY RANDOM()
                    LIMIT 1
                ''', (current_user_id, current_user_id))
                return cursor.fetchone()
        finally:
            DatabaseConnection.return_connection(conn)


class ConversationModel:
    """Database operations for conversations and messages."""

    @staticmethod
    def get_or_create(user1_id, user2_id):
        """
        Get existing conversation or create new one.

        Returns:
            int: Conversation ID
        """
        conn = DatabaseConnection.get_connection()
        try:
            with conn.cursor() as cursor:
                # Try to find existing
                cursor.execute('''
                    SELECT id FROM conversations
                    WHERE (user1_id = %s AND user2_id = %s)
                       OR (user1_id = %s AND user2_id = %s)
                ''', (user1_id, user2_id, user2_id, user1_id))

                result = cursor.fetchone()
                if result:
                    return result[0]

                # Create new
                cursor.execute('''
                    INSERT INTO conversations (user1_id, user2_id)
                    VALUES (%s, %s)
                    RETURNING id
                ''', (user1_id, user2_id))
                conv_id = cursor.fetchone()[0]
                conn.commit()
                return conv_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            DatabaseConnection.return_connection(conn)

    @staticmethod
    def get_messages(conversation_id, limit=50):
        """
        Get messages from conversation.

        Args:
            conversation_id (int): Conversation ID
            limit (int): Maximum messages to retrieve

        Returns:
            list: List of message dicts
        """
        conn = DatabaseConnection.get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute('''
                    SELECT
                        m.id,
                        u.user_name as sender_name,
                        m.message_text,
                        m.timestamp,
                        m.sender_id
                    FROM messages m
                    JOIN users u ON m.sender_id = u.id
                    WHERE m.conversation_id = %s
                    ORDER BY m.timestamp ASC
                    LIMIT %s
                ''', (conversation_id, limit))
                return cursor.fetchall()
        finally:
            DatabaseConnection.return_connection(conn)

    @staticmethod
    def send_message(conversation_id, sender_id, receiver_id, message_text):
        """
        Send a message in conversation.

        Returns:
            dict: Message ID and timestamp
        """
        conn = DatabaseConnection.get_connection()
        try:
            with conn.cursor() as cursor:
                # Insert message
                cursor.execute('''
                    INSERT INTO messages (conversation_id, sender_id, receiver_id, message_text)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id, timestamp
                ''', (conversation_id, sender_id, receiver_id, message_text))
                msg_id, timestamp = cursor.fetchone()

                # Update conversation timestamp
                cursor.execute('''
                    UPDATE conversations
                    SET last_message_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                ''', (conversation_id,))

                conn.commit()
                return {'id': msg_id, 'timestamp': timestamp}
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            DatabaseConnection.return_connection(conn)

    @staticmethod
    def mark_as_read(conversation_id, user_id):
        """Mark all messages in conversation as read for user."""
        conn = DatabaseConnection.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute('''
                    UPDATE messages
                    SET is_read = TRUE
                    WHERE conversation_id = %s
                      AND receiver_id = %s
                      AND is_read = FALSE
                ''', (conversation_id, user_id))
                conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            DatabaseConnection.return_connection(conn)


class MatchModel:
    """Database operations for matches."""

    @staticmethod
    def record_interaction(user_id, target_user_id, match_type):
        """
        Record like/pass interaction.

        Args:
            user_id (int): User performing action
            target_user_id (int): Target user
            match_type (str): 'like', 'pass', or 'super_like'
        """
        conn = DatabaseConnection.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO matches (user_id, target_user_id, match_type)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (user_id, target_user_id)
                    DO UPDATE SET match_type = %s
                ''', (user_id, target_user_id, match_type, match_type))
                conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            DatabaseConnection.return_connection(conn)

    @staticmethod
    def is_mutual_match(user_id, target_user_id):
        """Check if two users have mutually liked each other."""
        conn = DatabaseConnection.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute('''
                    SELECT EXISTS(
                        SELECT 1 FROM matches m1
                        JOIN matches m2 ON m1.user_id = m2.target_user_id
                                       AND m1.target_user_id = m2.user_id
                        WHERE m1.user_id = %s
                          AND m1.target_user_id = %s
                          AND m1.match_type = 'like'
                          AND m2.match_type = 'like'
                    )
                ''', (user_id, target_user_id))
                return cursor.fetchone()[0]
        finally:
            DatabaseConnection.return_connection(conn)
```

---

## Modifying Existing Code

### Step 3: Update UI.py

Modify `UI.py` to work with database:

```python
# Add to UI.py after imports
from db.models import UserModel

class UI:
    def __init__(self, db_conn=None):
        """
        Initialize UI with optional database connection.

        Args:
            db_conn: Database connection (optional for backward compatibility)
        """
        self.db_conn = db_conn
        self.fonts = { "electronic", "dos_rebel", ... }  # Keep existing fonts

    def print_profile_from_db(self, profile_user_id, current_user_id):
        """
        Display a user's profile from database.

        Args:
            profile_user_id (int): Database ID of profile to display
            current_user_id (int): Database ID of logged-in user
        """
        # Fetch profile from database
        profile_data = UserModel.get_by_id(profile_user_id)

        if not profile_data:
            print("Profile not found")
            return

        # Convert to object-like structure for existing rendering code
        class ProfileObj:
            def __init__(self, data):
                self.user_name = data['user_name']
                self.name_font = data['name_font']
                self.bio = data['bio']
                self.github = data['github']
                self.profile_pic = data['profile_pic']

        profile = ProfileObj(profile_data)
        user = UserModel.get_by_id(current_user_id)['user_name']

        # Use existing rendering logic
        os.system('clear')
        term_width = os.get_terminal_size().columns
        print("\n\n" + Colors.AQUA + "\\"*term_width + Colors.RESET + "\n\n")
        print("\n\n")

        # ... rest of existing print_profile code ...

    def edit_profile_from_db(self, user_id):
        """
        Edit profile with database persistence.

        Args:
            user_id (int): User ID to edit
        """
        # Load current data from database
        profile_data = UserModel.get_by_id(user_id)

        fields = {
            'user_name': {'label': 'Username', 'current': profile_data['user_name']},
            'name_font': {'label': 'Name Font', 'current': profile_data['name_font']},
            'bio': {'label': 'Bio', 'current': profile_data['bio']},
            'github': {'label': 'GitHub', 'current': profile_data['github']},
            'profile_pic': {'label': 'Profile Picture Path', 'current': profile_data['profile_pic']}
        }

        # ... existing UI editing code ...

        # When user saves (presses Escape):
        # Update database instead of in-memory object
        UserModel.update_profile(
            user_id,
            user_name=fields['user_name']['current'],
            name_font=fields['name_font']['current'],
            bio=fields['bio']['current'],
            github=fields['github']['current'],
            profile_pic=fields['profile_pic']['current']
        )

        # Refresh and display updated profile
        self.print_profile_from_db(user_id, user_id)
```

### Step 4: Update chat.py

Modify `chat.py` to work with database:

```python
# Add to chat.py after imports
from db.models import ConversationModel, UserModel

class ChatUI:
    def __init__(self, user_id, partner_id, db_conn=None):
        """
        Initialize chat UI with database backing.

        Args:
            user_id (int): Current user's database ID
            partner_id (int): Chat partner's database ID
            db_conn: Database connection (optional)
        """
        self.user_id = user_id
        self.partner_id = partner_id
        self.db_conn = db_conn

        # Get usernames
        user_data = UserModel.get_by_id(user_id)
        partner_data = UserModel.get_by_id(partner_id)

        self.user_name = user_data['user_name']
        self.chat_partner = partner_data['user_name']

        # Get or create conversation
        self.conversation_id = ConversationModel.get_or_create(user_id, partner_id)

        # Load messages
        self.messages = []
        self.load_messages()

    def load_messages(self):
        """Load messages from database."""
        messages_data = ConversationModel.get_messages(self.conversation_id)

        # Convert to format expected by rendering code
        self.messages = [
            (msg['sender_name'], msg['message_text'], msg['timestamp'].strftime("%H:%M"))
            for msg in messages_data
        ]

    def push_message_to_db(self, message):
        """
        Send message and save to database.

        Args:
            message (str): Message text
        """
        # Save to database
        ConversationModel.send_message(
            self.conversation_id,
            self.user_id,
            self.partner_id,
            message
        )

        # Add to local cache
        timestamp = datetime.now().strftime("%H:%M")
        self.messages.append((self.user_name, message, timestamp))

    def refresh_messages(self):
        """Refresh messages from database (for real-time updates)."""
        self.load_messages()

        # Mark as read
        ConversationModel.mark_as_read(self.conversation_id, self.user_id)

    # Modify request_message to use database
    def request_message(self):
        """Request input and save to database."""
        self.refresh_messages()  # Get latest messages
        self.render_chat()

        try:
            message = input()

            if message == "/code":
                os.system('clear')
                print("CODE CHALLENGE")
                return None

            if message.strip():
                self.push_message_to_db(message.strip())

            return message.strip()
        except (KeyboardInterrupt, EOFError):
            return None
```

---

## Authentication System

### Step 5: Create Authentication Module

Create `auth/auth.py`:

```python
"""
Authentication module.
Handles user login, registration, and password hashing.
"""

import bcrypt
from db.models import UserModel


def hash_password(password):
    """
    Hash password using bcrypt.

    Args:
        password (str): Plain text password

    Returns:
        str: Hashed password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(password, hashed):
    """
    Verify password against hash.

    Args:
        password (str): Plain text password
        hashed (str): Hashed password from database

    Returns:
        bool: True if password matches
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


def register_user(username, email, password, name_font='starwars'):
    """
    Register new user.

    Args:
        username (str): Desired username
        email (str): User email
        password (str): Plain text password
        name_font (str): Font preference

    Returns:
        int: New user ID

    Raises:
        ValueError: If username/email already exists
    """
    # Check if user exists
    existing = UserModel.get_by_username(username)
    if existing:
        raise ValueError("Username already exists")

    # Hash password
    password_hash = hash_password(password)

    # Create user
    user_id = UserModel.create(username, email, password_hash, name_font)

    return user_id


def login_user(username, password):
    """
    Authenticate user login.

    Args:
        username (str): Username
        password (str): Plain text password

    Returns:
        dict: User data if successful, None otherwise
    """
    user = UserModel.get_by_username(username)

    if not user:
        return None

    if not verify_password(password, user['password_hash']):
        return None

    return user
```

Create `auth/session.py`:

```python
"""
Session management.
Handles user sessions in terminal application.
"""

class Session:
    """Manages user session state."""

    def __init__(self):
        self.user_id = None
        self.username = None
        self.is_authenticated = False

    def login(self, user_data):
        """
        Set session data after successful login.

        Args:
            user_data (dict): User data from database
        """
        self.user_id = user_data['id']
        self.username = user_data['user_name']
        self.is_authenticated = True

    def logout(self):
        """Clear session data."""
        self.user_id = None
        self.username = None
        self.is_authenticated = False

    def require_auth(self):
        """
        Check if user is authenticated.

        Raises:
            PermissionError: If not authenticated
        """
        if not self.is_authenticated:
            raise PermissionError("Authentication required")
```

---

## Testing the Integration

### Step 6: Create Test Script

Create `test_db.py`:

```python
"""
Database integration test script.
"""

from db.connection import DatabaseConnection
from db.models import UserModel, ConversationModel
from auth.auth import register_user, login_user

def test_database():
    """Test database operations."""
    print("Testing database integration...")

    # Initialize connection pool
    DatabaseConnection.initialize()

    try:
        # Test 1: User creation
        print("\n1. Creating test user...")
        try:
            user_id = register_user(
                username="test_user",
                email="test@example.com",
                password="testpass123",
                name_font="starwars"
            )
            print(f"✓ User created with ID: {user_id}")
        except ValueError as e:
            print(f"User already exists: {e}")

        # Test 2: User login
        print("\n2. Testing login...")
        user = login_user("test_user", "testpass123")
        if user:
            print(f"✓ Login successful: {user['user_name']}")
        else:
            print("✗ Login failed")

        # Test 3: Profile retrieval
        print("\n3. Fetching user profile...")
        profile = UserModel.get_by_id(user_id)
        if profile:
            print(f"✓ Profile retrieved: {profile['user_name']}")
        else:
            print("✗ Profile not found")

        # Test 4: Profile update
        print("\n4. Updating profile...")
        UserModel.update_profile(user_id, bio="Updated bio for testing")
        updated = UserModel.get_by_id(user_id)
        if updated['bio'] == "Updated bio for testing":
            print("✓ Profile updated successfully")
        else:
            print("✗ Profile update failed")

        print("\n✓ All tests passed!")

    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        raise

    finally:
        DatabaseConnection.close_all()

if __name__ == "__main__":
    test_database()
```

Run tests:
```bash
python test_db.py
```

---

## Deployment Checklist

### Environment Setup

1. **Create .env file:**
```bash
DB_HOST=localhost
DB_PORT=5432
DB_NAME=dating_app
DB_USER=dating_app_user
DB_PASSWORD=your_secure_password
SECRET_KEY=your_secret_key_here
DEBUG=True
```

2. **Create .env.example (for version control):**
```bash
DB_HOST=localhost
DB_PORT=5432
DB_NAME=dating_app
DB_USER=your_db_user
DB_PASSWORD=your_password_here
SECRET_KEY=generate_random_secret_key
DEBUG=False
```

3. **Add to .gitignore:**
```
.env
__pycache__/
*.pyc
*.pyo
.venv/
venv/
```

### Database Setup

```bash
# Create database
createdb dating_app

# Run migrations
psql -d dating_app -f db/migrations.sql

# Create initial admin user (optional)
psql -d dating_app -c "INSERT INTO users ..."
```

### Security Checklist

- [ ] All passwords are hashed with bcrypt
- [ ] Database credentials stored in .env (not in code)
- [ ] SQL injection prevented (using parameterized queries)
- [ ] Input validation implemented
- [ ] Rate limiting considered for production
- [ ] SSL/TLS configured for production database
- [ ] Database backups configured

### Performance Checklist

- [ ] Database indexes created
- [ ] Connection pooling implemented
- [ ] Query optimization reviewed
- [ ] N+1 query problems avoided

---

## Next Steps

1. **Implement full application flow** in `main.py`
2. **Add error handling** throughout the application
3. **Implement logging** for debugging
4. **Add data validation** for all user inputs
5. **Create migration scripts** for schema updates
6. **Set up monitoring** for production
7. **Write comprehensive tests**
8. **Document API endpoints** if adding web interface

---

## Common Issues and Solutions

### Issue: Connection Pool Exhausted
**Solution:** Ensure connections are always returned to pool with try/finally blocks.

### Issue: SQL Injection Vulnerability
**Solution:** Always use parameterized queries with %s placeholders, never string formatting.

### Issue: Slow Queries
**Solution:** Add appropriate indexes and use EXPLAIN ANALYZE to optimize.

### Issue: Password Security
**Solution:** Use bcrypt with proper salt rounds (12+), never store plain text.

---

For additional help, refer to:
- [DATABASE_SCHEMA.md](DATABASE_SCHEMA.md) for schema details
- [PostgreSQL documentation](https://www.postgresql.org/docs/)
- [psycopg2 documentation](https://www.psycopg.org/docs/)
