# Terminal Dating App - Database Integration Documentation

Welcome! This documentation package will help you connect this terminal-based dating application frontend to a PostgreSQL database.

---

## Quick Start Guide

### What You Have
- **Frontend UI Code**: Terminal-based interface with ASCII art profiles
- **Chat System**: Real-time messaging interface
- **Profile Management**: User profile viewing and editing
- **Mock Data**: Test implementation using in-memory data

### What You Need to Add
- **PostgreSQL Database**: To persist user data, messages, and matches
- **Database Connection Layer**: To interface between frontend and database
- **Authentication System**: For user login and session management
- **Data Models**: To handle database queries and operations

---

## Documentation Files

This package includes comprehensive documentation across multiple files:

### 1. **In-Code Documentation** (✓ Already Added)
All Python files have been documented with:
- Module-level docstrings explaining purpose and database requirements
- Function-level docstrings with database integration notes
- Inline comments marking critical database integration points
- Example code showing database query patterns

**Files Documented:**
- [`UI.py`](UI.py) - Profile display and editing interface
- [`chat.py`](chat.py) - Messaging system
- [`image_to_ascii_art.py`](image_to_ascii_art.py) - Image processing
- [`test.py`](test.py) - Test/demo implementation

### 2. **DATABASE_SCHEMA.md** (✓ Created)
Complete PostgreSQL database schema including:
- All required tables with field definitions
- Indexes for optimal query performance
- Sample SQL queries for common operations
- Database functions and triggers
- Migration scripts
- Backup strategies

**[→ Read DATABASE_SCHEMA.md](DATABASE_SCHEMA.md)**

### 3. **INTEGRATION_GUIDE.md** (✓ Created)
Step-by-step integration walkthrough:
- Project structure recommendations
- Database connection layer implementation
- Modifying existing code for database use
- Authentication system setup
- Testing procedures
- Deployment checklist

**[→ Read INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)**

---

## Overview of Current Architecture

### Current Flow (Mock Data)
```
User Input → UI.py → Profile Object (in-memory) → Display in Terminal
         → chat.py → Messages List (in-memory) → Display in Terminal
```

### Target Flow (With Database)
```
User Input → UI.py → Database Query → PostgreSQL → Result → Display in Terminal
         → chat.py → Database Query → PostgreSQL → Result → Display in Terminal
```

---

## Key Integration Points

### 1. User Profiles (UI.py)

**Current Implementation:**
```python
person = Profile("Bryan Holl", "delta_corps_priest_1")
ui.print_profile(person, "Bryan Holl")
```

**Database Implementation:**
```python
ui = UI(db_conn=connection)
ui.print_profile_from_db(user_id=2, current_user_id=1)
```

**Database Table Required:**
```sql
users (id, user_name, name_font, bio, github, profile_pic, ...)
```

---

### 2. Chat Messages (chat.py)

**Current Implementation:**
```python
chat = ChatUI("Bryan Holl", "Isaac")
chat.push_message("Isaac", "Hey!")
```

**Database Implementation:**
```python
chat = ChatUI(user_id=1, partner_id=2, db_conn=connection)
chat.push_message_to_db("Hey!")  # Saves to database
```

**Database Tables Required:**
```sql
conversations (id, user1_id, user2_id, last_message_at, ...)
messages (id, conversation_id, sender_id, receiver_id, message_text, timestamp, ...)
```

---

### 3. Profile Pictures (image_to_ascii_art.py)

**Current Implementation:**
```python
profile_picture("profile.png").to_ascii()
```

**Database Implementation:**
```python
# Option 1: Store file paths in database
image_path = get_from_db("SELECT profile_pic FROM users WHERE id = %s")
profile_picture(image_path).to_ascii()

# Option 2: Store binary data in database (requires conversion)
image_data = get_from_db("SELECT profile_pic_data FROM users WHERE id = %s")
temp_file = save_to_temp(image_data)
profile_picture(temp_file).to_ascii()
```

**Recommended:** Use Option 1 (file paths) for simplicity.

---

## Database Schema Summary

### Core Tables

```
┌─────────────────────────────────────────────────────────┐
│                         USERS                           │
├─────────────────────────────────────────────────────────┤
│ id, user_name, email, password_hash, name_font, bio,   │
│ github, profile_pic, created_at, updated_at             │
└─────────────────────────────────────────────────────────┘
                          ▲
                          │
         ┌────────────────┴────────────────┐
         │                                  │
┌────────┴─────────────┐       ┌───────────┴──────────────┐
│   CONVERSATIONS      │       │       MESSAGES           │
├──────────────────────┤       ├──────────────────────────┤
│ id                   │◄──────┤ conversation_id          │
│ user1_id  ───────────┼─┐     │ sender_id  ──────────────┼─┐
│ user2_id  ───────────┼─┼─┐   │ receiver_id  ────────────┼─┼─┐
│ last_message_at      │ │ │   │ message_text             │ │ │
└──────────────────────┘ │ │   │ timestamp                │ │ │
                         │ │   │ is_read                  │ │ │
                         │ │   └──────────────────────────┘ │ │
                         │ └────────────────────────────────┘ │
                         └────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                       MATCHES (Optional)                │
├─────────────────────────────────────────────────────────┤
│ user_id → users.id                                      │
│ target_user_id → users.id                               │
│ match_type (like/pass/super_like)                       │
└─────────────────────────────────────────────────────────┘
```

**Full schema details:** See [DATABASE_SCHEMA.md](DATABASE_SCHEMA.md)

---

## Integration Roadmap

### Phase 1: Database Setup (1-2 hours)
- [ ] Install PostgreSQL
- [ ] Create database and user
- [ ] Run schema creation script
- [ ] Test database connection
- [ ] Insert sample data

**See:** [DATABASE_SCHEMA.md - Migration Guide](DATABASE_SCHEMA.md#migration-guide)

### Phase 2: Connection Layer (2-3 hours)
- [ ] Create `db/connection.py` for connection pooling
- [ ] Create `db/models.py` for database operations
- [ ] Test database queries
- [ ] Implement error handling

**See:** [INTEGRATION_GUIDE.md - Database Layer](INTEGRATION_GUIDE.md#database-layer-implementation)

### Phase 3: Authentication (2-3 hours)
- [ ] Create `auth/auth.py` for login/registration
- [ ] Implement password hashing (bcrypt)
- [ ] Create session management
- [ ] Test authentication flow

**See:** [INTEGRATION_GUIDE.md - Authentication](INTEGRATION_GUIDE.md#authentication-system)

### Phase 4: Modify Frontend (3-4 hours)
- [ ] Update `UI.py` to use database queries
- [ ] Update `chat.py` to persist messages
- [ ] Create database-backed `main.py`
- [ ] Test all functionality

**See:** [INTEGRATION_GUIDE.md - Modifying Code](INTEGRATION_GUIDE.md#modifying-existing-code)

### Phase 5: Testing & Deployment (2-3 hours)
- [ ] Write comprehensive tests
- [ ] Set up environment variables
- [ ] Configure production database
- [ ] Deploy application
- [ ] Set up backups

**See:** [INTEGRATION_GUIDE.md - Deployment](INTEGRATION_GUIDE.md#deployment-checklist)

**Total Estimated Time: 10-15 hours**

---

## File-by-File Documentation Reference

### UI.py
**Purpose:** Terminal UI for profile display and editing

**Database Integration Points:**
- `print_profile()` → `print_profile_from_db(user_id)` - Fetch user from database
- `edit_profile()` → `edit_profile_from_db(user_id)` - Update user in database
- `__init__()` - Add database connection parameter

**Key Changes:**
```python
# Before
ui = UI()
ui.print_profile(profile_object, "username")

# After
ui = UI(db_conn=connection)
ui.print_profile_from_db(user_id=2, current_user_id=1)
```

**Documentation Location:** Lines 1-63 in [UI.py](UI.py)

---

### chat.py
**Purpose:** Real-time messaging interface

**Database Integration Points:**
- `__init__()` - Get/create conversation, load messages from DB
- `push_message()` → `push_message_to_db()` - Insert message into database
- `render_chat()` - Add `refresh_messages()` to load latest from DB

**Key Changes:**
```python
# Before
chat = ChatUI("User1", "User2")
chat.push_message("User1", "Hello")

# After
chat = ChatUI(user_id=1, partner_id=2, db_conn=connection)
chat.push_message_to_db("Hello")  # Auto-saves to database
```

**Database Tables Used:**
- `conversations` - Thread between two users
- `messages` - Individual messages

**Documentation Location:** Lines 1-75 in [chat.py](chat.py)

---

### image_to_ascii_art.py
**Purpose:** Convert profile images to ASCII art

**Database Integration Points:**
- No direct database queries needed
- Works with file paths from database
- Consider BYTEA → temp file conversion if storing binary data

**Key Changes:**
```python
# Image path from database
cursor.execute("SELECT profile_pic FROM users WHERE id = %s", (user_id,))
image_path = cursor.fetchone()[0]

# Use with existing code
ascii_art = profile_picture(image_path).to_ascii()
```

**Recommendation:** Store file paths in database, not binary data.

**Documentation Location:** Lines 1-75 in [image_to_ascii_art.py](image_to_ascii_art.py)

---

### test.py
**Purpose:** Demo/test implementation with mock data

**Database Integration:**
- Replace `Profile` class with database queries
- Shows before/after comparison
- Contains example database implementation

**Use this file as reference** for understanding data flow.

**Documentation Location:** Lines 1-57 in [test.py](test.py)

---

## Quick Reference: Common Queries

### Get User Profile
```python
from db.models import UserModel
profile = UserModel.get_by_id(user_id)
# Returns: {'user_name': 'john', 'bio': '...', ...}
```

### Send Message
```python
from db.models import ConversationModel
ConversationModel.send_message(conv_id, sender_id, receiver_id, "Hello!")
```

### Update Profile
```python
from db.models import UserModel
UserModel.update_profile(user_id, bio="New bio", github="https://github.com/...")
```

### Get Next Profile to Show
```python
from db.models import UserModel
next_profile = UserModel.get_next_profile(current_user_id)
```

**Full query reference:** [DATABASE_SCHEMA.md - Sample Queries](DATABASE_SCHEMA.md#sample-queries)

---

## Environment Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

Required packages:
- `psycopg2-binary` - PostgreSQL adapter
- `python-dotenv` - Environment variable management
- `bcrypt` - Password hashing
- `pyfiglet` - ASCII art text
- `ascii-magic` - Image to ASCII conversion

### 2. Configure Environment Variables
Create `.env` file:
```bash
DB_HOST=localhost
DB_PORT=5432
DB_NAME=dating_app
DB_USER=your_user
DB_PASSWORD=your_password
SECRET_KEY=your_secret_key
```

### 3. Initialize Database
```bash
# Create database
createdb dating_app

# Run schema
psql -d dating_app -f db/migrations.sql

# Test connection
python test_db.py
```

---

## Security Considerations

### Critical Security Requirements:

1. **Password Storage**
   - ✓ Use bcrypt with 12+ rounds
   - ✗ Never store plain text passwords
   - ✓ Example: `bcrypt.hashpw(password.encode(), bcrypt.gensalt())`

2. **SQL Injection Prevention**
   - ✓ Always use parameterized queries: `cursor.execute(query, (param1, param2))`
   - ✗ Never use string formatting: `f"SELECT * FROM users WHERE id = {user_id}"`

3. **Environment Variables**
   - ✓ Store credentials in `.env` file
   - ✗ Never commit `.env` to git
   - ✓ Add `.env` to `.gitignore`

4. **Input Validation**
   - ✓ Validate all user inputs before database insertion
   - ✓ Sanitize file uploads
   - ✓ Limit message length

**Full security checklist:** [INTEGRATION_GUIDE.md - Security](INTEGRATION_GUIDE.md#security-checklist)

---

## Troubleshooting

### Common Issues:

**1. "Connection refused" error**
- **Cause:** PostgreSQL not running or wrong host/port
- **Solution:** Check PostgreSQL service status, verify `.env` settings

**2. "relation does not exist" error**
- **Cause:** Database tables not created
- **Solution:** Run migration script: `psql -d dating_app -f db/migrations.sql`

**3. "password authentication failed"**
- **Cause:** Wrong database credentials
- **Solution:** Verify username/password in `.env` match database user

**4. "too many connections" error**
- **Cause:** Connection pool exhausted
- **Solution:** Ensure connections are returned to pool in `finally` blocks

**5. Images not displaying**
- **Cause:** Invalid file path in database
- **Solution:** Verify `profile_pic` paths exist on filesystem

**Full troubleshooting guide:** [INTEGRATION_GUIDE.md - Common Issues](INTEGRATION_GUIDE.md#common-issues-and-solutions)

---

## Testing Your Integration

### Manual Testing Checklist:

- [ ] User registration works
- [ ] User login authenticates correctly
- [ ] Profile display shows data from database
- [ ] Profile editing updates database
- [ ] Messages save to database
- [ ] Messages load from database
- [ ] Conversation threading works correctly
- [ ] Profile pictures display correctly
- [ ] Navigation between profiles works
- [ ] Match system records interactions (if implemented)

### Automated Testing:

```bash
# Run database tests
python test_db.py

# Expected output:
# ✓ User created with ID: 1
# ✓ Login successful: test_user
# ✓ Profile retrieved: test_user
# ✓ Profile updated successfully
# ✓ All tests passed!
```

---

## Performance Optimization

### Database Indexes
All recommended indexes are included in the schema:
- User lookups by username/email
- Message queries by conversation
- Conversation lookups by user

### Connection Pooling
Implemented in `db/connection.py`:
- Min connections: 1
- Max connections: 20
- Automatically manages connection lifecycle

### Query Optimization
- Use `LIMIT` on message queries
- Index all foreign keys
- Use `EXPLAIN ANALYZE` to optimize slow queries

---

## Next Steps After Integration

1. **Add Real-time Features**
   - Implement WebSocket for live message updates
   - Add typing indicators
   - Add read receipts

2. **Enhance Matching Algorithm**
   - Implement preference-based matching
   - Add location-based filtering
   - Create match scoring system

3. **Add Features**
   - Code challenge implementation
   - User blocking/reporting
   - Message search
   - Profile verification

4. **Improve UX**
   - Add loading indicators
   - Implement error messages
   - Add confirmation dialogs
   - Create help system

5. **Production Readiness**
   - Set up logging
   - Implement monitoring
   - Configure backups
   - Add rate limiting
   - Security audit

---

## Support and Resources

### Documentation Files:
- **In-code documentation:** All `.py` files have detailed docstrings
- **[DATABASE_SCHEMA.md](DATABASE_SCHEMA.md):** Complete database schema
- **[INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md):** Step-by-step integration guide
- **This file (README_DATABASE.md):** Overview and quick reference

### External Resources:
- PostgreSQL Docs: https://www.postgresql.org/docs/
- psycopg2 Docs: https://www.psycopg.org/docs/
- Python bcrypt: https://github.com/pyca/bcrypt
- pyfiglet Fonts: http://www.figlet.org/fontdb.cgi

---

## Summary

This documentation package provides everything needed to integrate your terminal dating app frontend with a PostgreSQL database:

✓ **In-code documentation** in all Python files
✓ **Complete database schema** with migrations
✓ **Step-by-step integration guide** with code examples
✓ **Authentication system** implementation
✓ **Security best practices** and checklists
✓ **Testing procedures** and troubleshooting
✓ **Deployment guide** with environment setup

**Estimated integration time:** 10-15 hours for a fully functional database-backed application.

**Start here:** Read [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) for step-by-step instructions.

Good luck with your database integration! 🚀
