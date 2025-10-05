"""
Chat Module - Real-time Messaging Interface
============================================

This module provides a terminal-based chat interface for the dating application.
It handles message display, sending, and real-time chat rendering.

DATABASE INTEGRATION REQUIREMENTS:
----------------------------------
To connect this to PostgreSQL, you'll need to:

1. Store messages in a database table
2. Implement real-time message fetching
3. Track conversation threads between users
4. Add message status (sent, delivered, read)
5. Consider implementing WebSocket or polling for real-time updates

REQUIRED DATABASE TABLES:
------------------------
messages table:
- id: SERIAL PRIMARY KEY
- sender_id: INTEGER REFERENCES users(id) NOT NULL
- receiver_id: INTEGER REFERENCES users(id) NOT NULL
- message_text: TEXT NOT NULL
- timestamp: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- is_read: BOOLEAN DEFAULT FALSE
- conversation_id: INTEGER REFERENCES conversations(id)

conversations table:
- id: SERIAL PRIMARY KEY
- user1_id: INTEGER REFERENCES users(id) NOT NULL
- user2_id: INTEGER REFERENCES users(id) NOT NULL
- last_message_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

INDEXES (for performance):
- CREATE INDEX idx_messages_conversation ON messages(conversation_id, timestamp);
- CREATE INDEX idx_messages_sender ON messages(sender_id);
- CREATE INDEX idx_messages_receiver ON messages(receiver_id);

RECOMMENDED DATABASE FUNCTIONS:
-------------------------------
- get_conversation_messages(conv_id, limit) -> Returns recent messages
- send_message(sender_id, receiver_id, text) -> Inserts new message
- mark_messages_read(conv_id, user_id) -> Marks messages as read
- get_or_create_conversation(user1_id, user2_id) -> Gets/creates conversation thread

Example PostgreSQL Queries:
---------------------------
```python
import psycopg2

# Get recent messages
def get_messages(conversation_id, limit=50):
    cursor.execute('''
        SELECT m.id, u.user_name, m.message_text, m.timestamp
        FROM messages m
        JOIN users u ON m.sender_id = u.id
        WHERE m.conversation_id = %s
        ORDER BY m.timestamp DESC
        LIMIT %s
    ''', (conversation_id, limit))
    return cursor.fetchall()

# Send new message
def send_message(sender_id, receiver_id, text, conversation_id):
    cursor.execute('''
        INSERT INTO messages (sender_id, receiver_id, message_text, conversation_id)
        VALUES (%s, %s, %s, %s)
        RETURNING id, timestamp
    ''', (sender_id, receiver_id, text, conversation_id))
    conn.commit()
    return cursor.fetchone()
```
"""

import pyfiglet
import os
from datetime import datetime
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'bryan_data'))
from lord_save_me import add_message, get_messages_between


# Soft Retro Gruvbox color scheme
class Colors:
    RESET = '\033[0m'
    # Foreground colors
    BLACK = '\033[38;2;40;40;40m'       # black/dark
    BG = '\033[38;2;40;40;40m'          # gruvbox dark bg
    FG = '\033[38;2;213;196;161m'       # gruvbox warm fg
    RED = '\033[38;2;204;143;129m'      # subtle red
    GREEN = '\033[38;2;164;167;58m'     # subtle green
    YELLOW = '\033[38;2;215;169;87m'    # subtle yellow
    BLUE = '\033[38;2;121;145;142m'     # subtle blue
    PURPLE = '\033[38;2;181;124;145m'   # subtle purple
    AQUA = '\033[38;2;132;172;114m'     # subtle aqua
    ORANGE = '\033[38;2;214;138;75m'    # subtle orange
    # Background colors
    BG_RED = '\033[48;2;204;143;129m'      # subtle red bg
    BG_GREEN = '\033[48;2;164;167;58m'     # subtle green bg
    BG_YELLOW = '\033[48;2;215;169;87m'    # subtle yellow bg
    BG_BLUE = '\033[48;2;121;145;142m'     # subtle blue bg
    BG_PURPLE = '\033[48;2;181;124;145m'   # subtle purple bg
    BG_AQUA = '\033[48;2;132;172;114m'     # subtle aqua bg
    BG_ORANGE = '\033[48;2;214;138;75m'    # subtle orange bg
    BG_DARK = '\033[48;2;40;40;40m'        # dark bg
    BG_WHITE = '\033[48;2;255;255;255m'    # white bg


class ChatUI:
    """
    Chat UI class for terminal-based messaging.

    DATABASE INTEGRATION:
    --------------------
    This class currently stores messages in memory (self.messages list).
    For production, messages must be stored in and loaded from PostgreSQL.

    Attributes:
    ----------
    user_name : str
        Name of the current user (viewer)
    chat_partner : str
        Name of the user they're chatting with
    messages : list
        In-memory message cache. Should be replaced with database queries.
    """
    def __init__(self, user_name, chat_partner):
        """
        Initialize chat UI.

        DATABASE TODO:
        - Accept user_id and partner_id instead of names
        - Fetch or create conversation_id from database
        - Load initial message history from database

        Parameters (Current):
        --------------------
        user_name : str
            Current user's username
        chat_partner : str
            Chat partner's username

        Parameters (Database Version):
        ------------------------------
        user_id : int
            Current user's database ID
        partner_id : int
            Chat partner's database ID
        db_connection : connection object
            Active database connection

        Example Database Implementation:
        --------------------------------
        ```python
        def __init__(self, user_id, partner_id, db_conn):
            self.db = db_conn
            self.user_id = user_id
            self.partner_id = partner_id

            # Get or create conversation
            cursor = self.db.cursor()
            cursor.execute('''
                SELECT id FROM conversations
                WHERE (user1_id = %s AND user2_id = %s)
                   OR (user1_id = %s AND user2_id = %s)
            ''', (user_id, partner_id, partner_id, user_id))

            result = cursor.fetchone()
            if result:
                self.conversation_id = result[0]
            else:
                cursor.execute('''
                    INSERT INTO conversations (user1_id, user2_id)
                    VALUES (%s, %s) RETURNING id
                ''', (user_id, partner_id))
                self.conversation_id = cursor.fetchone()[0]
                self.db.commit()

            # Load recent messages
            self.load_messages()
        ```
        """
        self.user_name = user_name
        self.chat_partner = chat_partner
        # Load existing messages from database
        self.messages = get_messages_between(user_name, chat_partner)

    def update(self):
        self.messages = get_messages_between(self.user_name, self.chat_partner)

    def push_message(self, sender, message):
        """
        Add a message to the chat.

        DATABASE INTEGRATION CRITICAL:
        ------------------------------
        This function currently only adds to in-memory list.
        You MUST add an INSERT query to persist messages to database.

        Parameters (Current):
        --------------------
        sender : str
            Username of message sender
        message : str
            Message text

        Parameters (Database Version):
        ------------------------------
        sender_id : int
            Database ID of sender
        message : str
            Message text

        Database Query Needed:
        ---------------------
        ```python
        def push_message_to_db(self, sender_id, message):
            cursor = self.db.cursor()
            cursor.execute('''
                INSERT INTO messages (sender_id, receiver_id, message_text, conversation_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id, timestamp
            ''', (sender_id,
                  self.partner_id if sender_id == self.user_id else self.user_id,
                  message,
                  self.conversation_id))

            msg_id, timestamp = cursor.fetchone()
            self.db.commit()

            # Update conversation last_message_at
            cursor.execute('''
                UPDATE conversations
                SET last_message_at = CURRENT_TIMESTAMP
                WHERE id = %s
            ''', (self.conversation_id,))
            self.db.commit()

            # Add to local cache
            self.messages.append((sender_id, message, timestamp))
            return msg_id
        ```
        """
        timestamp = datetime.now().strftime("%H:%M")
        self.messages.append((sender, message, timestamp))

        # Determine receiver based on sender
        receiver = self.chat_partner if sender == self.user_name else self.user_name

        # Add message to database
        try:
            add_message(mess=message, send=sender, rec=receiver)
        except Exception as e:
            print(f"Warning: Failed to save message to database: {e}")

    def render_chat(self):
        """
        Render the chat UI in terminal.

        DATABASE INTEGRATION:
        --------------------
        Before rendering, you may want to refresh messages from database
        to show new messages from the chat partner (for real-time effect).

        Add this before rendering:
        ```python
        def refresh_messages(self):
            cursor = self.db.cursor()
            cursor.execute('''
                SELECT u.user_name, m.message_text, m.timestamp
                FROM messages m
                JOIN users u ON m.sender_id = u.id
                WHERE m.conversation_id = %s
                ORDER BY m.timestamp ASC
            ''', (self.conversation_id,))

            self.messages = cursor.fetchall()

            # Mark messages as read
            cursor.execute('''
                UPDATE messages
                SET is_read = TRUE
                WHERE conversation_id = %s AND receiver_id = %s
            ''', (self.conversation_id, self.user_id))
            self.db.commit()
        ```

        Call refresh_messages() at the start of this function for real-time updates.
        """
        os.system('clear')
        print('\033[H', end='')
        term_width = os.get_terminal_size().columns
        term_height = os.get_terminal_size().lines

        # Top border
        print( Colors.AQUA + "/"*term_width + Colors.RESET)
        print( Colors.AQUA + "_-"* (term_width//2) + Colors.RESET + "\n")

        # Chat header with partner name
        header = pyfiglet.figlet_format(f"Chatting with: {self.chat_partner}", font="pagga")
        header_lines = header.split('\n')
        for line in header_lines:
            print(Colors.YELLOW + line.center(term_width) + Colors.RESET)


        print( "_"*term_width + "\n")

        # Chat messages area
        max_msg_area = term_height - 15  # Reserve space for header and input
        visible_messages = self.messages[-max_msg_area:]

        for sender, message, timestamp in visible_messages:
            if sender == self.user_name:
                # User's messages (right-aligned)
                self._render_user_message(message, timestamp, term_width)
            else:
                # Partner's messages (left-aligned)
                self._render_partner_message(message, timestamp, term_width, sender)

        # Input prompt
        print(Colors.BG_BLUE + Colors.BLACK + " Type your message:" + Colors.RESET, end='' + " ")

    def _render_user_message(self, message, timestamp, term_width):
        """
        Render user's message (right-aligned).

        DATABASE INTEGRATION:
        --------------------
        No database queries needed. This is purely a UI rendering function.
        """
        max_width = term_width // 2
        wrapped_lines = self._wrap_text(message, max_width - 4)

        for i, line in enumerate(wrapped_lines):
            if i == 0:
                # First line with timestamp
                spacing = term_width - len(line) - len(timestamp) - 8
                print(f"{' ' * spacing}{Colors.AQUA}{timestamp}{Colors.RESET}  {Colors.GREEN}{line}{Colors.RESET}")
            else:
                spacing = term_width - len(line) - 4
                print(f"{' ' * spacing}{Colors.GREEN}{line}{Colors.RESET}")
        print()

    def _render_partner_message(self, message, timestamp, term_width, sender):
        """
        Render partner's message (left-aligned).

        DATABASE INTEGRATION:
        --------------------
        No database queries needed. This is purely a UI rendering function.
        """
        max_width = term_width // 2
        wrapped_lines = self._wrap_text(message, max_width - 4)

        for i, line in enumerate(wrapped_lines):
            if i == 0:
                # First line with timestamp
                print(f"  {Colors.PURPLE}{timestamp}{Colors.RESET}  {Colors.FG}{line}{Colors.RESET}")
            else:
                print(f"        {Colors.FG}{line}{Colors.RESET}")
        print()

    def _wrap_text(self, text, max_width):
        """
        Wrap text to fit within max_width.

        DATABASE INTEGRATION:
        --------------------
        No database queries needed. This is a pure utility function.
        """
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            if len(current_line) + len(word) + 1 <= max_width:
                current_line += f"{word} "
            else:
                if current_line:
                    lines.append(current_line.rstrip())
                current_line = f"{word} "
        if current_line:
            lines.append(current_line.rstrip())

        return lines if lines else [""]

    def request_message(self):
        """
        Request input from user and return the message.

        DATABASE INTEGRATION CRITICAL:
        ------------------------------
        After user types a message, you should:
        1. Call push_message() to add it to the chat
        2. push_message() should INSERT into database (see push_message docs)

        Special Commands:
        ----------------
        - "/code": Triggers code challenge (implement DB tracking for challenges)

        Example Implementation:
        ----------------------
        ```python
        def request_message(self):
            self.render_chat()
            try:
                message = input()

                if message == "/code":
                    # Track code challenge in database
                    cursor = self.db.cursor()
                    cursor.execute('''
                        INSERT INTO challenges (sender_id, receiver_id, created_at)
                        VALUES (%s, %s, CURRENT_TIMESTAMP)
                        RETURNING id
                    ''', (self.user_id, self.partner_id))
                    self.db.commit()
                    os.system('clear')
                    print("CODE CHALLENGE")
                    return None

                if message.strip():
                    self.push_message(self.user_id, message.strip())

                return message.strip()
            except (KeyboardInterrupt, EOFError):
                return None
        ```

        Returns:
        -------
        str or None
            The message text, or None if cancelled/special command
        """
        self.render_chat()
        try:
            message = input()
            if message == "/code":
                os.system('clear')
                print("CODE CHALLENGE")

            else:
                self.push_message(self.user_name, message.strip())

            return message.strip()
        
        except (KeyboardInterrupt, EOFError):
            return None
