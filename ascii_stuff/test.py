
from UI import UI
from image_to_ascii_art import profile_picture

## mock profile class for testing


class Profile:
    def __init__(self, user_name, name_font):
        self.user_name = user_name
        self.name_font = name_font
        self.bio = "Hello! I'm " + user_name + ". I love coding, hiking, and exploring new technologies.  I am a prominent figure on the reinmann sum of nerds podcast, and enjoy misleading students in my plp sessions"
        self.github = "https://github.com/Exahilosys/surve"
        self.profile_pic = "profile.png"



        
if __name__ == "__main__":

    person = Profile("Bryan Holl", "delta_corps_priest_1")
    ui = UI()

    ui.print_profile(person)
    ui.capture_keypress()
