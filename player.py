"""
File that holds the class that represents the player
"""

from item import Item


class Player(object):
    """
    Class representing the player
    """

    def __init__(self):
        self.inventory = []

    def add_item(self, item):
        """
        Adds an item to the player's inventory

        :param item: the item to add
        :type item: Item
        """
        assert isinstance(item, Item)
        self.inventory.append(item)

    def remove_item(self, item):
        """
        Removes an item from the player's inventory

        :param item: the item to remove
        :type item: Item

        :return the success of the removal. True if successful, False otherwise
        :rtype: bool
        """
        for index in xrange(0, len(self.inventory)):
            if self.inventory[index] == item:
                del self.inventory[index]
                return True

        return False

