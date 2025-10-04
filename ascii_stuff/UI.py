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
    def __init__(self):

        self.fonts = { "electronic", "dos_rebel", "def_leppard", "sweet", "5lineoblique", "bigmono9", "lean", 
             "georgi16", "3d-ascii", "georgia11", "banner3", "new_asci", "the_edge", "nscript",
             "cybermedium", "big_money-nw", "starwars", "pagga", "delta_corps_priest_1", "rozzo", "sub-zero",
             "this", "amc_aaa01", "fraktur", "nvscript"}


    def print_profile( self, profile):

        os.system('clear')
        term_width = os.get_terminal_size().columns
        print("\n\n")
        print("\n\n" + Colors.AQUA + "\\"*term_width + Colors.RESET + "\n\n")


        # Print profile NAME and PICTURE


        # Print PROFILE 
        f =  pyfiglet.figlet_format( profile.user_name , font=profile.name_font)

        figlet_lines = f.split('\n')

        left_margin = 5
        right_margin = 5

        # Get ASCII art lines
        ascii_art = profile_picture(profile.profile_pic).to_ascii(columns=46)
        ascii_lines = ascii_art.split('\n')

        # Print figlet and ASCII art side by side
        for i in range(max(len(figlet_lines), len(ascii_lines))):
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
            if i < len(ascii_lines):
                print(' ' * spacing + ascii_lines[i] + Colors.RESET)
            else:
                print()


        # Print description/bio and other info

        print("\n\n" + Colors.AQUA + "/"*term_width + Colors.RESET + "\n\n")


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
        print(f"{' ' * spacing}{Colors.ORANGE}GITHUB: {github_text}{Colors.RESET}")


        print("\n\n" + Colors.AQUA + "\\"*term_width + Colors.RESET + "\n\n")
        
        return
    # 
    def print_square(self):
            term_width = os.get_terminal_size().columns
            right_margin = term_width - 46
            for i in range(18):
                print(' ' * right_margin + '█' * 46)


    def capture_keypress(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
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
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)



    