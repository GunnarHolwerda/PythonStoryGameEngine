"""
Represents a character in the game
"""

import json
import logging

class Character(object):
    """
    Reperesents a Character in the game, also keeps track of all
    characters in the campagin in Character.CHARACTERS
    """

    # Dictionary of all characters in current campaign, key is the character id
    CHARACTERS = {}

    def __init__(self, name, identifier):
        self.name = name
        self.id = identifier

    @staticmethod
    def load_character_script(filename):
        """
        Loads the character script and populates Character.CHARACTERS

        :param filename: str, the filename of the characterscript (ends in cscript)
        """
        logging.debug("Loading in cscript " + filename)
        cscript = json.load(file("character_scripts/" + filename))
        for character in cscript:
            Character.CHARACTERS[character['id']] = \
                Character(character['name'], character['id'])

    @staticmethod
    def load_character(identifier):
        """
        Loads the Character object using the identifier given

        :param identifier: str, the id of the character to load

        :return Character, the character object
        """
        if identifier in Character.CHARACTERS:
            return Character.CHARACTERS[identifier]
        else:
            raise Exception("Character " + identifier + " could not be found")
