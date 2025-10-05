import pyfiglet
import os
import time
import sys
import subprocess

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


def countdown(seconds, title="STARTS IN"):
    """
    Display a countdown timer in retro gruvbox style

    Args:
        seconds: number of seconds to count down from
        title: title text to display above the countdown
    """
    term_width = os.get_terminal_size().columns
    countdown_font = "fraktur"
    title_font = "banner3"

    for remaining in range(seconds, -1, -1):
        os.system('clear')


        # Title
        title_art = pyfiglet.figlet_format(title, font=title_font)
        title_lines = title_art.split('\n')
        for line in title_lines:
            if line.strip():
                # Center the line
                padding = (term_width - len(line)) // 2
                print(' ' * padding + Colors.ORANGE + line + Colors.RESET)

        print("\n"*2)

        # Countdown number
        countdown_art = pyfiglet.figlet_format(str(remaining), font=countdown_font)
        countdown_lines = countdown_art.split('\n')

        # Determine color based on time remaining
        if remaining <= 3:
            color = Colors.RED
        elif remaining <= 10:
            color = Colors.YELLOW
        else:
            color = Colors.GREEN

        for line in countdown_lines:
            if line.strip():
                # Center the line
                padding = (term_width - len(line)) // 2
                print(' ' * padding + color + line + Colors.RESET)

        # Bottom border

        if remaining > 0:
            time.sleep(1)

    # GO! message
    os.system('clear')

    go_art = pyfiglet.figlet_format("GO!", font="new_asci")
    go_lines = go_art.split('\n')
    for line in go_lines:
        if line.strip():
            padding = (term_width - len(line)) // 2
            print(' ' * padding  + line)

    time.sleep(1)


    os.system('clear')
    subprocess.run(['bash', 'code.sh'])


if __name__ == "__main__":
    # Default countdown from 10 seconds
    seconds = 3

    # Allow custom countdown time from command line
    if len(sys.argv) > 1:
        try:
            seconds = int(sys.argv[1])
        except ValueError:
            print(f"{Colors.RED}Invalid number. Using default: 10 seconds{Colors.RESET}")

    countdown(seconds)
