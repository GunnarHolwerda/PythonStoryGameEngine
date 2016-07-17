"""
This program is supposed to create a command line based game similar to
Phoenix Wright Ace Attorney
"""

import dialog as d
from locations import load_map_file

class Game:

    def play(self):
        load_map_file("locations\maps\intro.map")


Game().play()
