"""
This program is supposed to create a command line based game similar to
Phoenix Wright Ace Attorney
"""

import dialog as d
import logging
import json
from game_state import GameState


class Game:

    def play(self):
        logging.basicConfig(filename="gamelog.log", level=logging.DEBUG, \
        format='%(asctime)s - %(levelname)s - %(message)s')
        #logging.disable(logging.CRITICAL)
        GameState.load_map_file("locations\maps\intro.map")
        GameState.start_event_script("event_script.escript")


if __name__ == "__main__":
    Game().play()
