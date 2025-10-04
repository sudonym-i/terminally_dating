import pyfiglet
import os


fonts = { "electronic", "dos_rebel", "def_leppard", "sweet", "5lineoblique", "bigmono9", "lean", 
             "georgi16", "3d-ascii", "georgia11", "banner3", "new_asci", "the_edge", "nscript",
             "cybermedium", "big_money-nw", "starwars", "pagga", "delta_corps_priest_1", "rozzo", "sub-zero",
             "this", "amc_aaa01", "fraktur", "nvscript"}


class UI:
    def __init__(self):

        os.system('clear')
        print("\n\n")

        self.fonts = { "electronic", "dos_rebel", "def_leppard", "sweet", "5lineoblique", "bigmono9", "lean", 
             "georgi16", "3d-ascii", "georgia11", "banner3", "new_asci", "the_edge", "nscript",
             "cybermedium", "big_money-nw", "starwars", "pagga", "delta_corps_priest_1", "rozzo", "sub-zero",
             "this", "amc_aaa01", "fraktur", "nvscript"}


    def print_profile( self, profile):


        # Print profile NAME and PICTURE
        f =  pyfiglet.figlet_format( profile.user_name , font=profile.name_font)
        figlet_lines = f.split('\n')

        term_width = os.get_terminal_size().columns
        left_margin = 5
        right_margin = 5

        # Print figlet and square side by side

        for i in range(max(len(figlet_lines), 18)):
            # Print left margin
            print(' ' * left_margin, end='')

            # Print figlet line (or empty if exhausted)
            if i < len(figlet_lines):
                figlet_line = figlet_lines[i]
                print(figlet_line, end='')
                spacing = term_width - left_margin - len(figlet_line) - 46 - right_margin
            else:
                spacing = term_width - left_margin - 46 - right_margin

            # Print square line on the same row
            if i < 18:
                print(' ' * spacing + '█' * 46)
            else:
                print()


        # Print description/bio and other info

        print("\n" + "/"*term_width + "\n")


        return
    # 
    def print_square(self):
            term_width = os.get_terminal_size().columns
            right_margin = term_width - 46
            for i in range(18):
                print(' ' * right_margin + '█' * 46)



    