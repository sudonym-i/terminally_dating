import pyfiglet
import os
from datetime import datetime


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
    def __init__(self, user_name, chat_partner):
        self.user_name = user_name
        self.chat_partner = chat_partner
        self.messages = []  # List of tuples: (sender, message, timestamp)

    def push_message(self, sender, message):
        """Add a message to the chat"""
        timestamp = datetime.now().strftime("%H:%M")
        self.messages.append((sender, message, timestamp))

    def render_chat(self):
        """Render the chat UI"""
        os.system('clear')
        print('\033[H', end='')
        term_width = os.get_terminal_size().columns
        term_height = os.get_terminal_size().lines

        # Top border
        print( Colors.AQUA + "/"*term_width + Colors.RESET)
        print( Colors.AQUA + "_-"* (term_width//2) + Colors.RESET + "\n")

        # Chat header with partner name
        header = pyfiglet.figlet_format(f"Chat: {self.chat_partner}", font="pagga")
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
        """Render user's message (right-aligned)"""
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
        """Render partner's message (left-aligned)"""
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
        """Wrap text to fit within max_width"""
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
        """Request input from user and return the message"""
        self.render_chat()
        try:
            message = input()
            return message.strip()
        except (KeyboardInterrupt, EOFError):
            return None
