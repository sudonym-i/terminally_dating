"""
UI Module - Profile Display and Editing Interface
==================================================

This module provides the terminal-based user interface for the dating application.
It handles profile display, navigation, and editing functionality.

DATABASE INTEGRATION REQUIREMENTS:
----------------------------------
To connect this to PostgreSQL, you'll need to:

1. Replace the Profile class with database queries
2. Implement CRUD operations for user profiles
3. Handle image storage (either as BLOB or file paths)
4. Implement real-time updates when profiles are edited

REQUIRED DATABASE TABLES:
------------------------
users table:
- id: SERIAL PRIMARY KEY
- user_name: VARCHAR(50) NOT NULL UNIQUE
- name_font: VARCHAR(50) NOT NULL
- bio: TEXT
- github: VARCHAR(255)
- profile_pic: VARCHAR(255) or BYTEA (for storing image path or binary data)
- created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- updated_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

RECOMMENDED DATABASE FUNCTIONS:
-------------------------------
- get_user_profile(user_id) -> Returns complete user profile
- update_user_profile(user_id, field, value) -> Updates specific profile field
- upload_profile_picture(user_id, image_data) -> Stores profile image

KEY INTEGRATION POINTS:
-----------------------
1. __init__(): Load fonts from database or config
2. print_profile(): Fetch profile data from database using user_id
3. edit_profile(): Update database when user saves changes
4. capture_keypress(): No database changes needed

Example PostgreSQL Query Pattern:
---------------------------------
```python
import psycopg2

def get_profile_from_db(user_id):
    conn = psycopg2.connect(
        host="localhost",
        database="dating_app",
        user="your_user",
        password="your_password"
    )
    cursor = conn.cursor()
    cursor.execute(
        "SELECT user_name, name_font, bio, github, profile_pic FROM users WHERE id = %s",
        (user_id,)
    )
    result = cursor.fetchone()
    conn.close()
    return result
```
"""

import profile
import pyfiglet
import os
import sys
import tty
import termios
from image_to_ascii_art import profile_picture

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


fonts = { "electronic", "dos_rebel", "def_leppard", "sweet", "5lineoblique", "bigmono9", "lean", 
             "georgi16", "3d-ascii", "georgia11", "banner3", "new_asci", "the_edge", "nscript",
             "cybermedium", "big_money-nw", "starwars", "pagga", "delta_corps_priest_1", "rozzo", "sub-zero",
             "this", "amc_aaa01", "fraktur", "nvscript"}


class UI:
    """
    Main UI class for rendering and managing user profiles.

    DATABASE INTEGRATION:
    --------------------
    This class currently works with in-memory Profile objects. To integrate with PostgreSQL:

    1. Inject a database connection object in __init__:
       def __init__(self, db_connection=None):
           self.db = db_connection

    2. Load available fonts from database or config file instead of hardcoded set

    Attributes:
    ----------
    fonts : set
        Available pyfiglet fonts for username display. In production, consider
        storing this in a database config table or loading from environment.
    """
    def __init__(self):
        """
        Initialize UI with available fonts.

        DATABASE TODO:
        - Load fonts from database config table: SELECT font_name FROM available_fonts;
        - Or inject database connection: def __init__(self, db_conn):
        """
        self.fonts = { "electronic", "dos_rebel", "def_leppard", "sweet", "5lineoblique", "bigmono9", "lean",
             "georgi16", "3d-ascii", "georgia11", "banner3", "new_asci", "the_edge", "nscript",
             "cybermedium", "big_money-nw", "starwars", "pagga", "delta_corps_priest_1", "rozzo", "sub-zero",
             "this", "amc_aaa01", "fraktur", "nvscript"}
        self.pointing_at_self = True

    def print_profile( self, profile, user):
        """
        Display a user's profile in terminal with ASCII art and formatting.

        DATABASE INTEGRATION REQUIRED:
        -----------------------------
        Currently accepts a Profile object. Modify to fetch from database:

        Parameters (Current):
        --------------------
        profile : Profile object
            User profile to display (name, bio, github, profile_pic path, name_font)
        user : str
            Logged-in user's username (to determine which buttons to show)

        Parameters (Database Version):
        ------------------------------
        profile_user_id : int
            Database ID of the profile to display
        current_user_id : int
            Database ID of the logged-in user viewing the profile

        Database Queries Needed:
        -----------------------
        1. Fetch profile data:
           SELECT user_name, name_font, bio, github, profile_pic
           FROM users WHERE id = %s

        2. Check if viewer is profile owner:
           SELECT (id = %s) as is_owner FROM users WHERE id = %s

        3. Fetch profile picture (if stored as BLOB):
           SELECT profile_pic FROM users WHERE id = %s
           Or just use file path if stored on filesystem

        Example Database Implementation:
        --------------------------------
        ```python
        def print_profile_from_db(self, profile_user_id, current_user_id):
            cursor = self.db.cursor()
            cursor.execute('''
                SELECT user_name, name_font, bio, github, profile_pic
                FROM users WHERE id = %s
            ''', (profile_user_id,))

            row = cursor.fetchone()
            if not row:
                print("Profile not found")
                return

            # Create temporary profile-like dict
            profile = {
                'user_name': row[0],
                'name_font': row[1],
                'bio': row[2],
                'github': row[3],
                'profile_pic': row[4]
            }

            is_own_profile = (profile_user_id == current_user_id)
            # ... rest of rendering logic
        ```

        Returns:
        -------
        None
            Renders directly to terminal
        """

        # "user" is the logged in user, teh user who is viewing this terminal output


        os.system('clear')
        term_width = os.get_terminal_size().columns
        print("\n\n" + Colors.AQUA + "\\"*term_width + Colors.RESET + "\n\n")
        print("\n\n")

        # Print profile NAME and PICTURE


        # Print PROFILE 
        f =  pyfiglet.figlet_format( profile.user_name , font=profile.name_font)

        figlet_lines = f.split('\n')

        left_margin = 5
        right_margin = 5


        # Ensure profile_pic is a list of lines
        profile_pic_lines = profile.profile_pic.split('\n') if isinstance(profile.profile_pic, str) else profile.profile_pic

        # Print figlet and ASCII art side by side
        for i in range(max(len(figlet_lines), len(profile_pic_lines))):
            # Print left margin
            print(' ' * left_margin, end='')

            # Print figlet line (or empty if exhausted) in orange
            if i < len(figlet_lines):
                figlet_line = figlet_lines[i]
                print(Colors.YELLOW + figlet_line + Colors.RESET, end='')
                spacing = term_width - left_margin - len(figlet_line) - 46 - right_margin
            else:
                spacing = term_width - left_margin - 46 - right_margin

            # Print ASCII art line on the same row
            if i < len(profile_pic_lines):
                print(' ' * spacing + profile_pic_lines[i] + Colors.RESET)
            else:
                print()


        # Print description/bio and other info

        print("\n\n" + Colors.ORANGE + "/"*term_width + Colors.RESET + "\n\n")


        print(Colors.BG_ORANGE + Colors.BLACK + "About me:" + Colors.RESET + "\n")

        # Wrap bio text to half screen width
        max_width = term_width // 2
        words = profile.bio.split()
        lines = []
        current_line = ""

    # for loop to format our text to stay only on the left side of the screen
        for word in words:
            if len(current_line) + len(word) + 1 <= max_width:
                current_line += f"{word} "
            else:
                lines.append(current_line.rstrip())
                current_line = f"{word} "
        if current_line:
            lines.append(current_line.rstrip())


        
        print(f"{Colors.FG}{'\n'.join(lines)}{Colors.RESET}", end='')

        # Calculate spacing to align github to the right
        github_text = profile.github
        spacing = term_width - len(lines[-1]) - len("GITHUB: " + github_text)
        print(f"{' ' * spacing}{Colors.ORANGE} ⚡GITHUB: {github_text}{Colors.RESET}")


        # Print instructions at the bottom
        instruction_font = "pagga"

        if self.pointing_at_self == True:
            instructions = [
            pyfiglet.figlet_format("[<-] Chat", font=instruction_font),
            pyfiglet.figlet_format("[^] Edit", font=instruction_font),
            pyfiglet.figlet_format("[->] Explore", font=instruction_font)
            ]
        else:
            instructions = [
            pyfiglet.figlet_format("[<-] My profile", font=instruction_font),
            pyfiglet.figlet_format("[^] Chat", font=instruction_font),
            pyfiglet.figlet_format("[->] Next", font=instruction_font)
        ]


        # Split each instruction into lines
        instruction_lines = [instr.split('\n') for instr in instructions]
        max_height = max(len(lines) for lines in instruction_lines)

        # Calculate widths of each instruction
        instruction_widths = [max(len(line) for line in instr_lines) for instr_lines in instruction_lines]
        total_instruction_width = sum(instruction_widths)

        # Calculate spacing to distribute evenly across terminal width
        available_space = term_width - total_instruction_width
        spacing = available_space // (len(instructions) + 1)

        print("\n" * 10)
        # Print instructions evenly spaced across terminal width
        for i in range(max_height):
            print(' ' * spacing, end='')  # Left margin
            for j, instr_lines in enumerate(instruction_lines):
                if i < len(instr_lines):
                    print(Colors.BLUE + instr_lines[i] + Colors.RESET, end='')
                else:
                    print(' ' * instruction_widths[j], end='')  # Empty space for alignment
                if j < len(instruction_lines) - 1:
                    print(' ' * spacing, end='')  # Spacing between instructions
            print()


        print("\n\n" + Colors.AQUA + "\\"*term_width + Colors.RESET + "\n\n")


        return


    def capture_keypress(self):
        """
        Capture single keypress from user without requiring Enter.

        DATABASE INTEGRATION:
        --------------------
        No database interaction needed in this function.
        However, the return value is used for navigation which may trigger database queries:
        - Return 1 (Left): Browse to previous profile -> Load previous user from DB
        - Return 2 (Up): Edit/Chat action -> May trigger profile update or message insert
        - Return 3 (Right): Next profile/Challenge -> Load next user from DB
        - Return 4 (Down): Not currently used
        - Return 69 (Enter): Confirm action
        - Return 99 (q): Quit

        Returns:
        -------
        int or None
            1: Left arrow
            2: Up arrow
            3: Right arrow
            4: Down arrow
            69: Enter key
            99: 'q' key (quit)
            0: Exception occurred
            None: Other key
        """
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            if ch == 'q':
                    return 99
            elif ch == '\n' or ch == '\r':
                return 69


            if ch == '\x1b':  # ESC sequence
                ch = sys.stdin.read(2)
                if ch == '[D':    # Left arrow
                    return 1
                elif ch == '[A':  # Up arrow
                    return 2
                elif ch == '[C':  # Right arrow
                    return 3
                elif ch == '[B':  # Down arrow
                    return 4
            return None
        except Exception:
            return 0
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


    def edit_profile(self, profile):
        """
        Interactive profile editing interface.

        DATABASE INTEGRATION CRITICAL:
        ------------------------------
        This function currently modifies a Profile object in memory.
        You MUST add database UPDATE statements when user saves changes.

        Parameters (Current):
        --------------------
        profile : Profile object
            Profile object to edit (modified in-place)

        Parameters (Database Version):
        ------------------------------
        user_id : int
            Database ID of user whose profile to edit

        Database Queries Needed:
        -----------------------
        1. Load current profile data:
           SELECT user_name, name_font, bio, github, profile_pic
           FROM users WHERE id = %s

        2. Update profile fields (called when user presses Escape to save):
           UPDATE users
           SET user_name = %s, name_font = %s, bio = %s, github = %s, profile_pic = %s, updated_at = CURRENT_TIMESTAMP
           WHERE id = %s

        3. Individual field updates (alternative approach for each edit):
           UPDATE users SET {field_name} = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s

        Example Database Implementation:
        --------------------------------
        ```python
        def edit_profile_from_db(self, user_id):
            # Load current data
            cursor = self.db.cursor()
            cursor.execute('''
                SELECT user_name, name_font, bio, github, profile_pic
                FROM users WHERE id = %s
            ''', (user_id,))

            row = cursor.fetchone()
            fields = {
                'user_name': {'label': 'Username', 'current': row[0]},
                'name_font': {'label': 'Name Font', 'current': row[1]},
                'bio': {'label': 'Bio', 'current': row[2]},
                'github': {'label': 'GitHub', 'current': row[3]},
                'profile_pic': {'label': 'Profile Picture Path', 'current': row[4]}
            }

            # ... UI logic for editing ...

            # When user saves (presses Escape):
            cursor.execute('''
                UPDATE users
                SET user_name = %s, name_font = %s, bio = %s, github = %s,
                    profile_pic = %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            ''', (fields['user_name']['current'], fields['name_font']['current'],
                  fields['bio']['current'], fields['github']['current'],
                  fields['profile_pic']['current'], user_id))
            self.db.commit()
        ```

        IMPORTANT NOTES:
        ---------------
        - Line 293: setattr(profile, field_key, new_value) needs to become UPDATE query
        - Line 281: profile.name_font = new_font needs to become UPDATE query
        - Consider adding validation before database updates
        - Handle database errors gracefully
        - Consider transaction rollback on error

        Returns:
        -------
        Profile object (current) or None (database version)
            Modified profile, or None if database-backed
        """
        os.system('clear')
        term_width = os.get_terminal_size().columns

        fields = {
            'user_name': {'label': 'Username', 'current': profile.user_name},
            'name_font': {'label': 'Name Font', 'current': profile.name_font},
            'bio': {'label': 'Bio', 'current': profile.bio},
            'github': {'label': 'GitHub', 'current': profile.github},
            'profile_pic': {'label': 'Profile Picture Path', 'current': profile.profile_pic}
        }

        field_keys = list(fields.keys())
        selected_index = 0

        end = False

        while not end:
            os.system('clear')
            print("\n\n" + Colors.AQUA + "\\"*term_width + Colors.RESET + "\n\n")
            print(Colors.BG_ORANGE + Colors.BLACK + " Edit Profile " + Colors.RESET + "\n\n")

            # Display all fields
            for i, (key, field_data) in enumerate(fields.items()):
                if i == selected_index:
                    prefix = Colors.BG_YELLOW + Colors.BLACK + " > " + Colors.RESET + " "
                else:
                    prefix = "   "

                label = field_data['label']
                value = field_data['current']

                # Truncate long values for display
                display_value = value if len(str(value)) < 60 else str(value)[:57] + "..."

                print(f"{prefix}{Colors.ORANGE}{label}:{Colors.RESET} {Colors.FG}{display_value}{Colors.RESET}")

                # Show font preview for name_font field
                if key == 'name_font' and i == selected_index:
                    try:
                        preview = pyfiglet.figlet_format(profile.user_name, font=value)
                        preview_lines = preview.split('\n')[:4]  # Show first 4 lines
                        for line in preview_lines:
                            if line.strip():
                                print(f"      {Colors.BLUE}{line[:term_width-10]}{Colors.RESET}")
                    except:
                        print(f"      {Colors.RED}(Invalid font){Colors.RESET}")

                print()

            # Instructions
            print("\n" + Colors.AQUA + "/"*term_width + Colors.RESET + "\n")
            instructions = f"{Colors.BLUE}[↑/↓] Navigate  [Enter] Edit  [q] Save & Exit{Colors.RESET}"
            print(instructions)

            # Capture keypress
            key = self.capture_keypress()

            if key == 4:  # Down arrow
                selected_index = (selected_index + 1) % len(field_keys)
            elif key == 2:  # Up arrow
                selected_index = (selected_index - 1) % len(field_keys)

            elif key == 99:  # Escape key
                end = True
                break
            elif key == 69:  # Enter key
                # Edit the selected field
                field_key = field_keys[selected_index]

                if field_key == 'name_font':
                    # Special handling for font selection with preview
                    new_font = self._select_font(profile.user_name, fields[field_key]['current'])
                    if new_font:
                        fields[field_key]['current'] = new_font
                        profile.name_font = new_font
                else:
                    # Regular text input
                    os.system('clear')
                    print(f"\n{Colors.ORANGE}Edit {fields[field_key]['label']}:{Colors.RESET}\n")
                    print(f"{Colors.FG}Current: {fields[field_key]['current']}{Colors.RESET}\n")

                    # Restore terminal to normal mode for input
                    new_value = input(f"{Colors.YELLOW}New value: {Colors.RESET}")

                    if new_value.strip():
                        fields[field_key]['current'] = new_value
                        setattr(profile, field_key, new_value)

        self.print_profile(profile, profile.user_name)
        return profile


    def _select_font(self, preview_text, current_font):
        """
        Font selection UI with live preview.

        DATABASE INTEGRATION:
        --------------------
        No direct database interaction needed.
        This is a helper function for edit_profile.
        The selected font will be saved when edit_profile calls the database UPDATE.

        Parameters:
        ----------
        preview_text : str
            Text to preview with different fonts (usually username)
        current_font : str
            Currently selected font

        Returns:
        -------
        str or None
            Selected font name, or None if cancelled
        """
        fonts_list = sorted(list(self.fonts))
        try:
            selected_index = fonts_list.index(current_font)
        except ValueError:
            selected_index = 0

        term_width = os.get_terminal_size().columns

        while True:
            os.system('clear')
            print("\n\n" + Colors.AQUA + "\\"*term_width + Colors.RESET + "\n\n")
            print(Colors.BG_ORANGE + Colors.BLACK + " Select Font " + Colors.RESET + "\n\n")

            current_font_name = fonts_list[selected_index]

            # Show preview
            try:
                preview = pyfiglet.figlet_format(preview_text, font=current_font_name)
                preview_lines = preview.split('\n')
                for line in preview_lines:
                    if line.strip():
                        # Truncate if too wide
                        display_line = line if len(line) < term_width - 10 else line[:term_width-10]
                        print(f"  {Colors.YELLOW}{display_line}{Colors.RESET}")
            except:
                print(f"  {Colors.RED}Error rendering font{Colors.RESET}")

            print("\n" + Colors.AQUA + "/"*term_width + Colors.RESET + "\n")

            # Show current font name and position
            print(f"{Colors.ORANGE}Font:{Colors.RESET} {Colors.FG}{current_font_name}{Colors.RESET}")
            print(f"{Colors.BLUE}({selected_index + 1}/{len(fonts_list)}){Colors.RESET}\n")

            # Instructions
            print(f"{Colors.BLUE}[←/→] Browse  [Enter] Select  [q] Cancel{Colors.RESET}")

            key = self.capture_keypress()

            if key == 3:  # Right arrow
                selected_index = (selected_index + 1) % len(fonts_list)
            elif key == 1:  # Left arrow
                selected_index = (selected_index - 1) % len(fonts_list)
            elif key == 69:  # Enter
                return fonts_list[selected_index]
            elif key == 99:  # Escape
                return None



    