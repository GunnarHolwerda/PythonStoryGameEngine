"""
Represents a character in the game
"""

import json
import logging
from named_object import NamedObject, ValueComparison


class Character(NamedObject, ValueComparison, object):
    """
    Represents a Character in the game, also keeps track of all
    characters in the campaign in Character.CHARACTERS
    """

    # Dictionary of all characters in current campaign, key is the character id
    CHARACTERS = {}

    def __init__(self, name, identifier):
        super(Character, self).__init__(name)
        self.id = identifier

    @staticmethod
    def load_character_script(filename):
        """
        Loads the character script and populates Character.CHARACTERS

        :param filename: the filename of the characterscript (ends in cscript)
        :type filename: str
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

        :param identifier: the id of the character to load
        :type identifier: str

        :return the character object
        :rtype: Character
        """
        if identifier in Character.CHARACTERS:
            return Character.CHARACTERS[identifier]
        else:
            raise Exception("Character " + identifier + " could not be found")
