"""
This program is supposed to create a command line based game similar to
Phoenix Wright Ace Attorney
"""

import logging
from game_state import GameState

# TODO: ADD TESTING


class Game(object):
    """
    The class the runs the actual game. play() is essentially main
    """

    @staticmethod
    def menu():
        """
        Will be used to display the main menu of the game which will
        then call play to start a campaign
        """
        pass

    @staticmethod
    def play():
        """
        The main method that starts the game. Will be used to start different
        campaigns.
        """
        # Initialize the logging for the game
        logging.basicConfig(
            filename="gamelog.log", level=logging.DEBUG, format='%(levelname)s - %(message)s')
        #logging.disable(logging.CRITICAL) # Disables logging of messages below the level specified
        GameState.start_event_script("event_script.escript")


if __name__ == "__main__":
    Game.play()
