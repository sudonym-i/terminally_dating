
from UI import UI



class Profile:
    def __init__(self, user_name, name_font):
        self.user_name = user_name
        self.name_font = name_font

        
if __name__ == "__main__":

    person = Profile("Bryan Holl", "starwars")
    ui = UI()

    ui.print_profile(person)
