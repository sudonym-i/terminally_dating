class profile:
    """
    Class to store user profile information.
    """
    def __init__(self, picture: str, age: int, first_name: str, last_name: str, interests: list, languages_spoken: list):
        self.picture = picture
        self.age = age
        self.first_name = first_name
        self.last_name = last_name
        self.interests = interests
        self.languages_spoken = languages_spoken

    def display_profile(self):
        return f"Name: {self.name}, Age: {self.age}, Bio: {self.bio}"
    