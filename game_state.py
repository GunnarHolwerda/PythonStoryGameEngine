"""
This class will be used to represent the curent state of the game
"""

import logging
import json
from locations import Map
from character import Character
from item import Item
from player import Player

# TODO: Implement save feature


class GameState(object):
    """
    This class represents the current state of the game. Keeps track of
    unlocked locations, manages current location, manages what events are
    occuring
    """
    #TODO: Maybe hold all loaded characters and items here? locations too?
    GAME_MAP = Map()
    CURRENT_LOCATION = None
    EVENTS = []
    PLAYER = None

    @staticmethod
    def update(changes):
        """
        Updates the gamestate using a dictionary passed in as the argument
        all dictionaries passed must contain the 'action' and 'type' keys
        to tell what sort of update must be completed

        :param changes: list of changes dictionaries
        :type changes: list
        """
        # TODO: Figure out a better what to handle this
        # IDEA: Create class for each change then have a strategy pattern to
        # execute the needed changes???
        for change in changes:
            if change['type'] == "location":
                logging.debug("Unlocking location %s.", change['id'])
                # Changes to a location must include a location id
                location = GameState.GAME_MAP.load_location(change['id'])
                if change['action'] == 'set_active':
                    location.set_active()

    @staticmethod
    def initialize_game(escript):
        """
        Loads in map, character_script, item_script and intializes player object.
        Also sets the starting location of the game

        :param escript: dictionary loaded from escript that specifies files
        :type escript: dict
        """
        # Load map, characters, items, and player
        GameState.GAME_MAP.load_map_file(escript['map'])
        Character.load_character_script(escript['character_script'])
        Item.load_item_script(escript['item_script'])
        GameState.PLAYER = Player()
        # TODO: Add starting items to player specified in escript from starting_items

        # Update current location
        GameState.CURRENT_LOCATION = GameState.GAME_MAP.load_location(escript['start_location'])

    @staticmethod
    def start_event_script(filename):
        """
        Initializes the current event script. One event script will be given for each campaign.
        Event scripts outline the complete story of the game and what conversations and actions
        unlock what events. They also specify the map and starting location

        :param filename: the filename of the eventscript in the event_scripts directory
        :type filename: str
        """
        logging.debug("Loading in event script " + filename)
        escript = json.load(file("event_scripts/" + filename))
        # Load map, characters, items, and player
        GameState.initialize_game(escript)

        # Initialize the first event
        GameState.EVENTS = escript['events']
        start_event = GameState.EVENTS[0]
        for loc in start_event['locations']:
            location = GameState.GAME_MAP.load_location(loc['id'])
            if loc['character']:
                location.set_character(Character.CHARACTERS[loc['character']])
            if loc['dscript']:
                location.set_dscript(loc['dscript'])

        GameState.CURRENT_LOCATION.start()

    @staticmethod
    def update_current_location(new_location):
        """
        Sets the current location to the specified location in new_location_id

        :param new_location: the location_id for the new current location
        :type new_location: str
        """
        GameState.CURRENT_LOCATION = new_location
        GameState.CURRENT_LOCATION.start()
