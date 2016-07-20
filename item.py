"""
File that holds the class that represents an item
"""

import json
import logging

class Item(object):
    """
    Class representing an item
    """

    ITEMS = {}

    def __init__(self, item_dict):
        self.name = item_dict['name']
        self.tag = item_dict['tag']
        self.desc = item_dict['desc']

    @staticmethod
    def load_items(filename):
        """
        Loads items from the specified file

        :param filename: str, filename of item_script
        """
        items = json.load(file("item_scripts\\" + filename))
        for item in items:
            Item.ITEMS[item['tag']] = Item(item)
