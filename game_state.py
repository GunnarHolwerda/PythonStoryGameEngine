"""
This class will be used to represent the curent state of the game
"""

import logging
import json
from locations import Map
from character import Character

class GameState:

    GAME_MAP = Map()
    CURRENT_LOCATION = None
    EVENTS = []

    @staticmethod
    def load_map_file(filename):
        GameState.GAME_MAP.load_map_file(filename)

    @staticmethod
    def start_event_script(filename):
        # TODO: Event script should also specify map file at some point
        logging.debug("Loading in event script " + filename)
        escript = json.load(file("event_scripts/" + filename))
        GameState.CURRENT_LOCATION = GameState.GAME_MAP.load_location(escript['start_location'])
        Character.load_character_script(escript['character_script'])

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
    def move(new_location_id):
        # TODO: Create check to make sure not making illegal move to impossible location
        GameState.CURRENT_LOCATION = GameState.GAME_MAP.load_location(new_location_id)
        print GameState.CURRENT_LOCATION
        GameState.CURRENT_LOCATION.start()
