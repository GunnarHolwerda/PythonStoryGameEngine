"""
Represents a character in the game
"""

import json
import logging

class Character:

    CHARACTERS = {}

    def __init__(self, name, identifier):
        self.name = name
        self.id = identifier

    @staticmethod
    def load_character_script(filename):
        logging.debug("Loading in cscript " + filename)
        cscript = json.load(file("character_scripts/" + filename))
        for character in cscript:
            Character.CHARACTERS[character['id']] = \
                Character(character['name'], character['id'])

    @staticmethod
    def load_character(identifier):
        if identifier in Character.CHARACTERS:
            return Character.CHARACTERS[identifier]
        else:
            raise Exception("Character " + identifier + " could not be found")
