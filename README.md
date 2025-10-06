# Terminally Dating 💻💘

A terminal-based dating application for developers, featuring ASCII art profiles, real-time chat, and collaborative coding challenges.

## Overview

Terminally Dating is a unique social networking application that runs entirely in the terminal. Users can view ASCII art profiles, chat with matches, edit their profiles, and participate in collaborative coding challenges with their matches.

## Features

### 🎨 ASCII Art Profiles
- Beautiful ASCII art profile pictures rendered in the terminal
- Customizable username fonts from a curated selection of pyfiglet fonts
- Personalized bios and GitHub links
- Soft retro Gruvbox color scheme for a comfortable viewing experience

### 💬 Real-Time Chat
- Terminal-based chat interface with color-coded messages
- Message history stored in PostgreSQL database
- Intuitive left/right-aligned message display (user vs. partner)
- Type `/code` to initiate a coding challenge with your match

### 🎯 Collaborative Coding Challenges
- Random coding challenges fetched from the database
- Two-part challenges where each user writes complementary code
- Live code execution to test if both solutions work together
- Competitive element with countdown animations
- Success/failure feedback based on combined code execution

### ⚙️ Profile Management
- Interactive profile editing with arrow key navigation
- Live font preview when selecting username fonts
- Edit username, bio, GitHub link, and profile picture
- Save changes directly to the database

## Project Structure

```
terminally_dating/
├── ascii_stuff/                 # Main application code
│   ├── main.py                 # Application entry point
│   ├── UI.py                   # Profile display and editing
│   ├── chat.py                 # Chat interface
│   ├── image_to_ascii_art.py   # ASCII art conversion
│   ├── requirements.txt        # Python dependencies
│   └── setup.sh                # Setup script
├── david_challenges/           # Coding challenge system
│   ├── code_challenge.py       # Challenge logic
│   ├── challenge.sh           # Challenge script runner
│   └── postgretest.py         # Database testing
├── isaacs_challenge_stuff/    # Challenge animations
│   └── animation.py           # Countdown and challenge start
├── bryan_data_for_ascii/      # Database utilities
│   └── help_me.py            # User retrieval functions
└── bryan_data/               # Additional database utilities
    └── lord_save_me.py       # Message storage and retrieval
```

## How It Works

### Navigation System

The application uses arrow keys for navigation:

**When viewing your own profile:**
- `←` Left Arrow: Open chat with matches
- `↑` Up Arrow: Edit your profile
- `→` Right Arrow: Explore other profiles
- `q`: Quit

**When viewing other profiles:**
- `←` Left Arrow: Return to your profile
- `↑` Up Arrow: Chat with this person
- `→` Right Arrow: View next profile
- `q`: Quit

### Profile Display

1. **Username**: Rendered in large ASCII art using the user's chosen font
2. **Profile Picture**: ASCII art conversion of the user's profile image (displayed on the right)
3. **Bio**: User's biography displayed on the left half of the screen
4. **GitHub Link**: User's GitHub profile URL (displayed on the right)
5. **Navigation Hints**: ASCII art instructions at the bottom

### Chat System

The chat interface provides:
- Color-coded messages (user messages in green, partner messages in purple)
- Timestamps for each message
- Message history loaded from PostgreSQL database
- Real-time message updates
- Special `/code` command to trigger coding challenges

### Coding Challenges

When a user types `/code` in chat:

1. A countdown animation starts (3 seconds by default)
2. A random challenge is selected from the database
3. The challenge has two parts - one for each user
4. Each user writes their code independently
5. Code is stored in the database
6. Both code snippets are combined and executed together
7. Success or failure is displayed based on execution results

Example challenge: One user writes a function, the other writes code that calls it.

### Database Integration

The application uses PostgreSQL to store:
- **User profiles**: username, bio, GitHub link, profile picture path, name font
- **Messages**: sender, receiver, message text, timestamp
- **Challenges**: challenge descriptions and prompts
- **Challenge answers**: user submissions for challenges

## Installation

### Prerequisites

- Python 3.7+
- PostgreSQL database
- Terminal with ANSI color support

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd terminally_dating
```

2. Install Python dependencies:
```bash
cd ascii_stuff
pip install -r requirements.txt
```

Dependencies include:
- `pyfiglet` - ASCII art text generation
- `ascii_magic` - Image to ASCII art conversion
- `psycopg2-binary` - PostgreSQL database adapter
- `websocket-client` - WebSocket support

3. Set up PostgreSQL database:
   - Configure database connection in `david_challenges/code_challenge.py`
   - Update host, database name, user, and password
   - Create required tables (see database schema in code comments)

4. Run the application:
```bash
python main.py
```

## Configuration

### Database Connection

Update the database connection details in:
- `david_challenges/code_challenge.py` (line 30-38)

```python
conn = psycopg2.connect(
    host="your_host",
    database="your_database",
    user="your_username",
    password="your_password",
    port=5432
)
```

### User Configuration

In [main.py](ascii_stuff/main.py), set your user ID:
```python
self.USER = 4  # Your user ID in the database
```

### Available Fonts

The application includes 25+ ASCII art fonts for username display:
- electronic, dos_rebel, def_leppard, sweet, bigmono9, lean
- georgi16, 3d-ascii, georgia11, banner3, new_asci, the_edge
- nscript, cybermedium, big_money-nw, starwars, pagga
- delta_corps_priest_1, rozzo, sub-zero, fraktur, nvscript
- and more!

## Color Scheme

The application uses a soft retro Gruvbox color palette:
- **Background**: Dark (#282828)
- **Foreground**: Warm beige (#D5C4A1)
- **Accents**: Subtle orange, aqua, blue, purple, yellow
- **Highlights**: Soft red, green for messages

## Technical Details

### Key Components

1. **UI Class** ([UI.py](ascii_stuff/UI.py)):
   - Handles profile rendering
   - Manages keyboard input capture
   - Provides profile editing interface
   - Uses `pyfiglet` for ASCII text art
   - Uses `ascii_magic` for image-to-ASCII conversion

2. **ChatUI Class** ([chat.py](ascii_stuff/chat.py)):
   - Renders chat interface
   - Manages message display and input
   - Stores/retrieves messages from database
   - Triggers coding challenges

3. **Code Challenge System** ([code_challenge.py](david_challenges/code_challenge.py)):
   - Fetches challenges from database
   - Coordinates user code submissions
   - Executes and validates combined code
   - Stores answers in database

4. **Animation System** ([animation.py](isaacs_challenge_stuff/animation.py)):
   - Countdown timer with ASCII art
   - Color-coded countdown (green → yellow → red)
   - "GO!" animation before challenges

### Security Notes

- User code execution uses `exec()` - only use in trusted environments
- No authentication system implemented (proof of concept)
- Database credentials are hardcoded (should use environment variables in production)

## Development Status

This is a proof-of-concept application demonstrating:
- Terminal-based UI design
- ASCII art rendering
- Real-time messaging
- Collaborative coding challenges
- PostgreSQL integration

### Future Improvements

The codebase includes extensive documentation for migrating to a full production system:
- User authentication and session management
- Connection pooling for database
- WebSocket support for real-time updates
- Secure code execution sandbox
- Profile picture upload system
- Matching algorithm implementation
- Message read receipts

See inline comments in [UI.py](ascii_stuff/UI.py), [chat.py](ascii_stuff/chat.py), and [main.py](ascii_stuff/main.py) for detailed migration guides.

## Contributing

This project was built as a collaborative effort. Key contributors:
- Profile UI and rendering system
- Chat interface and messaging
- Database integration
- Coding challenge system
- ASCII art and animations

## License

[Add your license here]

## Acknowledgments

- Built with [pyfiglet](https://github.com/pwaller/pyfiglet) for ASCII art text
- Uses the beautiful Gruvbox color scheme
- Inspired by the joy of terminal applications and developer culture

---

**Made with ❤️ and lots of escape sequences**
