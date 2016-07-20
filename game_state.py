"""
This class will be used to represent the curent state of the game
"""

import logging
import json
from locations import Map
from character import Character

class GameState(object):
    """
    This class represents the current state of the game. Keeps track of
    unlocked locations, manages current location, manages what events are
    occuring
    """

    GAME_MAP = Map()
    CURRENT_LOCATION = None
    EVENTS = []

    @staticmethod
    def update(changes):
        """
        Updates the gamestate using a dictionary passed in as the argument
        all dictionaries passed must contain the 'action' and 'type' keys
        to tell what sort of update must be completed

        :param changes: list, list of changes dictionaries
        """
        # TODO: Figure out a better what to handle this
        # TODO: Create class for each change then have a strategy pattern to
        # execute the needed changes???
        for change in changes:
            if change['type'] == "location":
                logging.debug("Unlocking location %s.", change['id'])
                # Changes to a location must include a location id
                location = GameState.GAME_MAP.load_location(change['id'])
                if change['action'] == 'set_active':
                    location.set_active()


    @staticmethod
    def load_map_file(filename):
        """
        Designates the loading of the map file to the actual Map class
        """
        # TODO: Possibly refactor this so that it isn't just a passthrough
        GameState.GAME_MAP.load_map_file(filename)

    @staticmethod
    def start_event_script(filename):
        """
        Initializes the current event script. One event script will be given for each campaign.
        Event scripts outline the complete story of the game and what conversations and actions
        unlock what events. They also specify the map and starting location

        :param filename: str, the filename of the eventscript in the event_scripts directory
        """
        # TODO: Event script should also specify map file at some point
        logging.debug("Loading in event script " + filename)
        escript = json.load(file("event_scripts/" + filename))
        # Load map
        GameState.load_map_file(escript['map'])
        # Update current location
        GameState.CURRENT_LOCATION = GameState.GAME_MAP.load_location(escript['start_location'])
        # Load characters
        Character.load_character_script(escript['character_script'])

        # Initialize the first event
        GameState.EVENTS = escript['events']
        start_event = GameState.EVENTS[0]
        for loc in start_event['locations']:
            location = GameState.GAME_MAP.load_location(loc['id'])
            if loc['character']:
                location.set_character(Character.CHARACTERS[loc['character']])
            if loc['dscript']:
                location.set_dscript(loc['dscript'])

        logging.debug("Start location is " + GameState.CURRENT_LOCATION.name)
        GameState.CURRENT_LOCATION.start()

    @staticmethod
    def update_current_location(new_location_id):
        """
        Sets the current location to the specified location in new_location_id

        :param new_location_id: str, the location_id for the new curent location
        """
        GameState.CURRENT_LOCATION = GameState.GAME_MAP.load_location(new_location_id)
        GameState.CURRENT_LOCATION.start()
