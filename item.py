"""
File that holds the class that represents an item
"""

import json
import logging
from named_object import NamedObject, ValueComparison


class Item(NamedObject, ValueComparison, object):
    """
    Class representing an item
    """

    ITEMS = {}

    # TODO: Refactor out the tag and just use the item name, don't forget to change it in the dscript
    def __init__(self, item_dict):
        super(Item, self).__init__(item_dict['name'])
        self.tag = item_dict['tag']
        self.desc = item_dict['desc']

    @staticmethod
    def load_item(tag):
        """
        Returns the item matching the tag

        :param tag: the string tag for the item to be loaded
        :type tag: str
        """
        if tag not in Item.ITEMS.keys():
            raise Exception("Could not find item: " + tag)
        return Item.ITEMS[tag]

    @staticmethod
    def load_item_script(filename):
        """
        Loads items from the specified file

        :param filename: filename of item_script
        :type filename: str
        """
        items = json.load(file("item_scripts\\" + filename))
        for item in items:
            Item.ITEMS[item['tag']] = Item(item)
