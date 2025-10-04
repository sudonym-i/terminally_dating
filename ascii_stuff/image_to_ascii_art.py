
from ascii_magic import AsciiArt

class profile_picture:
    def __init__(self, image_path):
        self.image_path = image_path

    def to_ascii(self, columns=40):
        art = AsciiArt.from_image(self.image_path)
        return art.to_ascii(columns=columns, width_ratio=2.0)
