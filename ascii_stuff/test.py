from chat import ChatUI
from UI import UI
import os

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
    ui.print_profile(person, "Bryan Holl")

    if ( ui.capture_keypress() == 3):

        chat = ChatUI("Bryan Holl", "Isaac")
        chat.render_chat()
        chat.push_message("Isaac", "Hey Bryan! How's it going?")
        chat.push_message("Bryan Holl", "Hey Isaac! I'm doing well, thanks for asking. How about you?")
        chat.push_message("Isaac", "I'm good too! Just working on some projects.")

        chat.request_message()
    elif (ui.capture_keypress() == 1):
        ui.edit_profile(person)