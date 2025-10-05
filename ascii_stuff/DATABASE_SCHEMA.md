# Database Schema Documentation
# PostgreSQL Schema for Terminal Dating Application

This document provides the complete PostgreSQL database schema needed to integrate this frontend with a database backend.

---

## Table of Contents
1. [Overview](#overview)
2. [Database Tables](#database-tables)
3. [Indexes](#indexes)
4. [Sample Queries](#sample-queries)
5. [Migration Guide](#migration-guide)
6. [Connection Setup](#connection-setup)

---

## Overview

This application requires a PostgreSQL database with the following core functionality:
- User profile management
- Real-time messaging between users
- Conversation threading
- Profile browsing and matching
- Code challenges (optional feature)

**Database Name:** `dating_app` (or your preferred name)

---

## Database Tables

### 1. users

Stores user profile information.

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    user_name VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name_font VARCHAR(50) NOT NULL DEFAULT 'starwars',
    bio TEXT,
    github VARCHAR(255),
    profile_pic VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Add comment
COMMENT ON TABLE users IS 'Stores user profile and authentication data';
COMMENT ON COLUMN users.name_font IS 'PyFiglet font name for displaying username';
COMMENT ON COLUMN users.profile_pic IS 'File path to profile picture (or BYTEA for binary storage)';
```

**Field Descriptions:**
- `id`: Auto-incrementing primary key
- `user_name`: Unique username displayed in terminal UI
- `email`: User's email for authentication
- `password_hash`: Hashed password (use bcrypt or argon2)
- `name_font`: PyFiglet font name (from fonts set in UI.py)
- `bio`: User's biography/about section
- `github`: GitHub profile URL
- `profile_pic`: Path to profile image file (e.g., `/uploads/profile_1.png`)
- `created_at`: Account creation timestamp
- `updated_at`: Last profile update timestamp
- `last_login`: Last login timestamp
- `is_active`: Account status flag

---

### 2. conversations

Tracks conversation threads between two users.

```sql
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user1_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    user2_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_message_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_conversation UNIQUE(user1_id, user2_id),
    CONSTRAINT different_users CHECK (user1_id != user2_id)
);

COMMENT ON TABLE conversations IS 'Tracks messaging conversations between users';
```

**Field Descriptions:**
- `id`: Auto-incrementing primary key
- `user1_id`: First participant's user ID
- `user2_id`: Second participant's user ID
- `created_at`: When conversation was started
- `last_message_at`: Timestamp of most recent message (for sorting)

**Constraints:**
- Unique conversation per user pair
- Prevents self-conversations
- Cascading delete when user is deleted

---

### 3. messages

Stores individual chat messages.

```sql
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    sender_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    receiver_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    message_text TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_read BOOLEAN DEFAULT FALSE,
    CONSTRAINT valid_message_length CHECK (LENGTH(message_text) > 0)
);

COMMENT ON TABLE messages IS 'Stores individual chat messages between users';
```

**Field Descriptions:**
- `id`: Auto-incrementing primary key
- `conversation_id`: Reference to parent conversation
- `sender_id`: User who sent the message
- `receiver_id`: User who receives the message
- `message_text`: Message content
- `timestamp`: When message was sent
- `is_read`: Whether receiver has read the message

---

### 4. matches (Optional)

Tracks user matching/liking system.

```sql
CREATE TABLE matches (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    target_user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    match_type VARCHAR(20) NOT NULL CHECK (match_type IN ('like', 'pass', 'super_like')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, target_user_id)
);

COMMENT ON TABLE matches IS 'Tracks user likes, passes, and matches';
```

**Field Descriptions:**
- `user_id`: User performing the action
- `target_user_id`: User being liked/passed
- `match_type`: Type of interaction (like/pass/super_like)
- `created_at`: When the interaction occurred

---

### 5. challenges (Optional)

Tracks code challenges between users.

```sql
CREATE TABLE challenges (
    id SERIAL PRIMARY KEY,
    sender_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    receiver_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    challenge_type VARCHAR(50) DEFAULT 'coding',
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'completed', 'declined')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

COMMENT ON TABLE challenges IS 'Tracks code challenges sent between users';
```

**Field Descriptions:**
- `sender_id`: User who initiated the challenge
- `receiver_id`: User receiving the challenge
- `challenge_type`: Type of challenge
- `status`: Current challenge status
- `created_at`: When challenge was sent
- `completed_at`: When challenge was completed

---

## Indexes

Create these indexes for optimal query performance:

```sql
-- User lookups
CREATE INDEX idx_users_username ON users(user_name);
CREATE INDEX idx_users_email ON users(email);

-- Conversation lookups
CREATE INDEX idx_conversations_user1 ON conversations(user1_id);
CREATE INDEX idx_conversations_user2 ON conversations(user2_id);
CREATE INDEX idx_conversations_last_message ON conversations(last_message_at DESC);

-- Message lookups
CREATE INDEX idx_messages_conversation ON messages(conversation_id, timestamp);
CREATE INDEX idx_messages_sender ON messages(sender_id);
CREATE INDEX idx_messages_receiver ON messages(receiver_id);
CREATE INDEX idx_messages_unread ON messages(receiver_id, is_read) WHERE is_read = FALSE;

-- Match lookups
CREATE INDEX idx_matches_user ON matches(user_id);
CREATE INDEX idx_matches_target ON matches(target_user_id);

-- Challenge lookups
CREATE INDEX idx_challenges_receiver ON challenges(receiver_id, status);
CREATE INDEX idx_challenges_sender ON challenges(sender_id);
```

---

## Sample Queries

### User Management

#### Create New User
```sql
INSERT INTO users (user_name, email, password_hash, name_font, bio, github, profile_pic)
VALUES ('john_doe', 'john@example.com', '$2b$12$...', 'starwars', 'Love coding!',
        'https://github.com/johndoe', '/uploads/profile_1.png')
RETURNING id;
```

#### Get User Profile
```sql
SELECT id, user_name, name_font, bio, github, profile_pic, created_at
FROM users
WHERE id = $1;
```

#### Update User Profile
```sql
UPDATE users
SET user_name = $1,
    name_font = $2,
    bio = $3,
    github = $4,
    profile_pic = $5,
    updated_at = CURRENT_TIMESTAMP
WHERE id = $6;
```

#### Get Next Profile (Simple Random)
```sql
SELECT id, user_name, name_font, bio, github, profile_pic
FROM users
WHERE id != $1  -- Exclude current user
  AND is_active = TRUE
  AND id NOT IN (
    SELECT target_user_id FROM matches WHERE user_id = $1
  )  -- Exclude already seen profiles
ORDER BY RANDOM()
LIMIT 1;
```

---

### Messaging

#### Get or Create Conversation
```sql
-- First, try to find existing conversation
SELECT id FROM conversations
WHERE (user1_id = $1 AND user2_id = $2)
   OR (user1_id = $2 AND user2_id = $1);

-- If not found, create new one
INSERT INTO conversations (user1_id, user2_id)
VALUES ($1, $2)
ON CONFLICT DO NOTHING
RETURNING id;
```

#### Send Message
```sql
INSERT INTO messages (conversation_id, sender_id, receiver_id, message_text)
VALUES ($1, $2, $3, $4)
RETURNING id, timestamp;

-- Update conversation's last_message_at
UPDATE conversations
SET last_message_at = CURRENT_TIMESTAMP
WHERE id = $1;
```

#### Get Conversation Messages
```sql
SELECT
    m.id,
    u.user_name as sender_name,
    m.message_text,
    m.timestamp,
    m.is_read
FROM messages m
JOIN users u ON m.sender_id = u.id
WHERE m.conversation_id = $1
ORDER BY m.timestamp ASC
LIMIT 50;
```

#### Mark Messages as Read
```sql
UPDATE messages
SET is_read = TRUE
WHERE conversation_id = $1
  AND receiver_id = $2
  AND is_read = FALSE;
```

#### Get User's Conversations List
```sql
SELECT
    c.id as conversation_id,
    CASE
        WHEN c.user1_id = $1 THEN u2.user_name
        ELSE u1.user_name
    END as partner_name,
    CASE
        WHEN c.user1_id = $1 THEN c.user2_id
        ELSE c.user1_id
    END as partner_id,
    c.last_message_at,
    (SELECT COUNT(*) FROM messages
     WHERE conversation_id = c.id
       AND receiver_id = $1
       AND is_read = FALSE) as unread_count
FROM conversations c
JOIN users u1 ON c.user1_id = u1.id
JOIN users u2 ON c.user2_id = u2.id
WHERE c.user1_id = $1 OR c.user2_id = $1
ORDER BY c.last_message_at DESC;
```

---

### Matching System

#### Record Like/Pass
```sql
INSERT INTO matches (user_id, target_user_id, match_type)
VALUES ($1, $2, $3)
ON CONFLICT (user_id, target_user_id)
DO UPDATE SET match_type = $3;
```

#### Check Mutual Match
```sql
SELECT EXISTS(
    SELECT 1 FROM matches m1
    JOIN matches m2 ON m1.user_id = m2.target_user_id
                   AND m1.target_user_id = m2.user_id
    WHERE m1.user_id = $1
      AND m1.target_user_id = $2
      AND m1.match_type = 'like'
      AND m2.match_type = 'like'
) as is_mutual_match;
```

---

### Code Challenges

#### Create Challenge
```sql
INSERT INTO challenges (sender_id, receiver_id, challenge_type)
VALUES ($1, $2, 'coding')
RETURNING id;
```

#### Get Pending Challenges
```sql
SELECT
    c.id,
    u.user_name as sender_name,
    c.challenge_type,
    c.created_at
FROM challenges c
JOIN users u ON c.sender_id = u.id
WHERE c.receiver_id = $1
  AND c.status = 'pending'
ORDER BY c.created_at DESC;
```

---

## Migration Guide

### Step 1: Create Database
```bash
# Login to PostgreSQL
psql -U postgres

# Create database and user
CREATE DATABASE dating_app;
CREATE USER dating_app_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE dating_app TO dating_app_user;
```

### Step 2: Run Schema
```bash
# Run this schema file
psql -U dating_app_user -d dating_app -f DATABASE_SCHEMA.sql
```

### Step 3: Insert Sample Data
```sql
-- Sample user
INSERT INTO users (user_name, email, password_hash, name_font, bio, github, profile_pic)
VALUES
    ('bryan_holl', 'bryan@example.com', 'hashed_password_here', 'delta_corps_priest_1',
     'Hello! I am a prominent figure on the reinmann sum of nerds podcast',
     'https://github.com/example', 'profile.png'),
    ('isaac', 'isaac@example.com', 'hashed_password_here', 'starwars',
     'Love coding and terminal UIs!',
     'https://github.com/example2', 'profile2.png');
```

### Step 4: Test Queries
```sql
-- Test user retrieval
SELECT * FROM users WHERE user_name = 'bryan_holl';

-- Test conversation creation
INSERT INTO conversations (user1_id, user2_id) VALUES (1, 2);

-- Test message insertion
INSERT INTO messages (conversation_id, sender_id, receiver_id, message_text)
VALUES (1, 1, 2, 'Hey there!');
```

---

## Connection Setup

### Python (psycopg2)

```python
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import closing

# Connection configuration
DB_CONFIG = {
    'host': 'localhost',
    'database': 'dating_app',
    'user': 'dating_app_user',
    'password': 'your_secure_password',
    'port': 5432
}

# Basic connection
def get_db_connection():
    """Create database connection."""
    return psycopg2.connect(**DB_CONFIG)

# With connection pooling (recommended for production)
from psycopg2 import pool

connection_pool = pool.SimpleConnectionPool(1, 20, **DB_CONFIG)

def get_db_connection_from_pool():
    """Get connection from pool."""
    return connection_pool.getconn()

def return_connection_to_pool(conn):
    """Return connection to pool."""
    connection_pool.putconn(conn)

# Usage example
def get_user_profile(user_id):
    """Fetch user profile from database."""
    with closing(get_db_connection()) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute('''
                SELECT id, user_name, name_font, bio, github, profile_pic
                FROM users WHERE id = %s
            ''', (user_id,))
            return cursor.fetchone()
```

### Environment Variables (.env)

```bash
# Database configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=dating_app
DB_USER=dating_app_user
DB_PASSWORD=your_secure_password

# Application settings
SECRET_KEY=your_secret_key_here
DEBUG=False
```

### Loading Environment Variables

```python
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'dating_app'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'port': int(os.getenv('DB_PORT', 5432))
}
```

---

## Additional Recommendations

### 1. Database Functions for Common Operations

Create PostgreSQL functions for frequently used operations:

```sql
-- Function to get or create conversation
CREATE OR REPLACE FUNCTION get_or_create_conversation(
    p_user1_id INTEGER,
    p_user2_id INTEGER
) RETURNS INTEGER AS $$
DECLARE
    v_conversation_id INTEGER;
BEGIN
    -- Try to find existing conversation
    SELECT id INTO v_conversation_id
    FROM conversations
    WHERE (user1_id = p_user1_id AND user2_id = p_user2_id)
       OR (user1_id = p_user2_id AND user2_id = p_user1_id);

    -- Create if doesn't exist
    IF v_conversation_id IS NULL THEN
        INSERT INTO conversations (user1_id, user2_id)
        VALUES (LEAST(p_user1_id, p_user2_id), GREATEST(p_user1_id, p_user2_id))
        RETURNING id INTO v_conversation_id;
    END IF;

    RETURN v_conversation_id;
END;
$$ LANGUAGE plpgsql;
```

### 2. Triggers for Automatic Updates

```sql
-- Trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

### 3. Security Considerations

- **Always use parameterized queries** to prevent SQL injection
- **Hash passwords** using bcrypt or argon2 before storing
- **Use SSL/TLS** for database connections in production
- **Implement rate limiting** on message sending
- **Validate all user input** before database insertion
- **Set up proper database permissions** (read-only users where appropriate)

### 4. Backup Strategy

```bash
# Daily backup
pg_dump -U dating_app_user dating_app > backup_$(date +%Y%m%d).sql

# Restore from backup
psql -U dating_app_user dating_app < backup_20250104.sql
```

---

## Next Steps

1. Review the schema and modify as needed for your specific requirements
2. Set up your PostgreSQL database
3. Run the migration scripts
4. Update the Python code in UI.py and chat.py to use database queries
5. Implement authentication and session management
6. Add error handling and logging
7. Test thoroughly with sample data
8. Deploy to production with proper security measures

For questions or issues, refer to:
- PostgreSQL documentation: https://www.postgresql.org/docs/
- psycopg2 documentation: https://www.psycopg.org/docs/
