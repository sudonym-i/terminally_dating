import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from bryan_data_for_ascii.help_me import retrieve_usr
from chat import ChatUI 

"""
Test Module - Mock Implementation for Frontend Testing
======================================================

This file demonstrates how the UI and Chat modules work with mock data.
Use this as a reference for understanding the data flow when connecting to PostgreSQL.

DATABASE REPLACEMENT GUIDE:
--------------------------
This file uses a mock Profile class to simulate database data.
When integrating with PostgreSQL:

1. Remove the Profile class entirely
2. Replace Profile objects with database queries
3. Use user IDs instead of usernames
4. Inject database connection into UI and ChatUI classes

MOCK vs DATABASE COMPARISON:
---------------------------

CURRENT (Mock):
```python
person = Profile("Bryan Holl", "delta_corps_priest_1")
ui.print_profile(person, "Bryan Holl")
```

WITH DATABASE:
```python
import psycopg2

# Connect to database
conn = psycopg2.connect(
    host="localhost",
    database="dating_app",
    user="db_user",
    password="db_password"
)

# Initialize UI with database connection
ui = UI(db_conn=conn)

# Display profile by user ID (not username)
current_user_id = 1  # From login session
profile_to_view_id = 2  # From navigation/matching

ui.print_profile_from_db(profile_to_view_id, current_user_id)
```

MIGRATION STEPS:
---------------
1. Set up PostgreSQL database
2. Create required tables (see DATABASE_SCHEMA.md)
3. Modify UI.__init__() to accept database connection
4. Replace Profile object usage with database queries
5. Update ChatUI to use database-backed messages
6. Implement user authentication and session management
"""

from chat import ChatUI
from UI import UI
import os

## Mock profile class for testing
## DATABASE NOTE: This class simulates what would come from the database.
## In production, remove this class and fetch data from users table.

class Profile:
    """
    Mock profile class for testing.

    DATABASE EQUIVALENT:
    -------------------
    This represents a row from the users table:

    SELECT id, user_name, name_font, bio, github, profile_pic
    FROM users WHERE id = %s

    When integrating with database:
    - Replace this class with direct database queries
    - Use dictionaries or named tuples to hold query results
    - Or create a database model class with ORM (like SQLAlchemy)

    Attributes:
    ----------
    user_name : str
        Username (from users.user_name)
    name_font : str
        Font for displaying name (from users.name_font)
    bio : str
        User biography (from users.bio)
    github : str
        GitHub profile URL (from users.github)
    profile_pic : str
        Path to profile picture (from users.profile_pic)
    """
    def __init__(self):

        data = retrieve_usr(3)

        self.id = data[0]
        self.user_name = data[1]
        self.name_font = data[9]
        self.bio = data[5]
        self.github = data[6]
        self.profile_pic = data[10]
        self.i = 3




if __name__ == "__main__":
    """
    Main test flow demonstrating UI navigation.

    DATABASE MIGRATION GUIDE:
    -------------------------
    This main block shows the flow of the application with mock data.
    When connecting to PostgreSQL, replace with:

    ```python
    import psycopg2
    from contextlib import closing

    def main():
        # Database connection
        with closing(psycopg2.connect(
            host="localhost",
            database="dating_app",
            user="your_user",
            password="your_password"
        )) as conn:

            # Get current user from login session
            current_user_id = get_logged_in_user()  # Implement session management

            # Initialize UI with database
            ui = UI(db_conn=conn)

            # Get next profile to show (from matching algorithm)
            profile_id = get_next_match(current_user_id, conn)

            # Display profile
            ui.print_profile_from_db(profile_id, current_user_id)

            # Handle navigation
            key = ui.capture_keypress()

            if key == 3:  # Right arrow - Chat
                # Get partner info
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM users WHERE id = %s", (profile_id,))
                partner_id = cursor.fetchone()[0]

                # Start chat with database backing
                chat = ChatUI(current_user_id, partner_id, conn)

                # Load existing messages and render
                chat.render_chat()

                # Enter message loop
                while True:
                    msg = chat.request_message()
                    if msg is None:
                        break

            elif key == 2:  # Up arrow - Edit profile
                ui.edit_profile_from_db(current_user_id)

    if __name__ == "__main__":
        main()
    ```

    KEY CHANGES FROM MOCK TO DATABASE:
    ---------------------------------
    1. Database connection management (use connection pooling in production)
    2. Session management for logged-in user
    3. Matching algorithm to find profiles to show
    4. All data comes from database queries, not in-memory objects
    5. Error handling for database failures
    6. Transaction management for data consistency
    """

    # Mock data flow (current implementation)
    person = Profile()
    ui = UI()
    repeat = True
    while repeat:

        ui.pointing_at_self = (person.i == 3)
        ui.print_profile(person, "Bryan Holl")

        key = ui.capture_keypress()

        if ui.pointing_at_self:
            # When viewing own profile
            if key == 1:  # Left arrow - Chat
                # DATABASE NOTE: Replace with chat = ChatUI(user_id, partner_id, db_conn)
                chat = ChatUI("Bryan Holl", "Isaac")
                chat.render_chat()

                chat.request_message()

            elif key == 2:  # Up arrow - Edit
                # DATABASE NOTE: Replace with ui.edit_profile_from_db(user_id)
                ui.edit_profile(person)

            elif key == 3:  # Right arrow - Explore (go to next profile)
                ui.pointing_at_self = False
                if person.i > 5:
                    person.i = 3  # CHANGE THESE IF YOU CHANGE # OF USERS
                else:
                    person.i += 1
                data = retrieve_usr(person.i)
                person.id = data[0]
                person.user_name = data[1]
                person.name_font = data[9]
                person.bio = data[5]
                person.github = data[6]
                person.profile_pic = data[10]

        else:
            # When viewing other profiles
            if key == 1:  # Left arrow - Return to My profile
                person.i = 3  # Return to user's own profile (ID 3)
                data = retrieve_usr(person.i)
                person.id = data[0]
                person.user_name = data[1]
                person.name_font = data[9]
                person.bio = data[5]
                person.github = data[6]
                person.profile_pic = data[10]
                # Loop will update pointing_at_self automatically on next iteration

            elif key == 2:  # Up arrow - Chat
                # DATABASE NOTE: Replace with chat = ChatUI(user_id, partner_id, db_conn)
                chat = ChatUI("Bryan Holl", person.user_name)

                while True:
                    msg = chat.request_message()
                    print(f"DEBUG: msg = {repr(msg)}")  # Debug output
                    if msg is None or (msg and msg.lower() == 'exit'):
                        break
                    chat.update()
               

            elif key == 3:  # Right arrow - Next profile
                if person.i > 5:
                    person.i = 3  # CHANGE THESE IF YOU CHANGE # OF USERS
                else:
                    person.i += 1
                data = retrieve_usr(person.i)
                person.id = data[0]
                person.user_name = data[1]
                person.name_font = data[9]
                person.bio = data[5]
                person.github = data[6]
                person.profile_pic = data[10]

        repeat = True
            