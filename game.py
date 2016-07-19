"""
This program is supposed to create a command line based game similar to
Phoenix Wright Ace Attorney
"""

import logging
from game_state import GameState


class Game:
    """
    The class the runs the actual game. play() is essentially main
    """
    def __init__(self):
        pass

    def menu(self):
        """
        Will be used to display the main menu of the game which will
        then call play to start a campaign
        """
        pass

    def play(self):
        """
        The main method that starts the game. Will be used to start different
        campaigns.
        """
        # Initialize the logging for the game
        logging.basicConfig(filename="gamelog.log", level=logging.DEBUG, \
        format='%(asctime)s - %(levelname)s - %(message)s')
        #logging.disable(logging.CRITICAL) # Disables logging of messages below the level specified

        # Load the map to create the graph of locations for the game
        GameState.load_map_file("intro.map")
        GameState.start_event_script("event_script.escript")


if __name__ == "__main__":
    Game().play()
