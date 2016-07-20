"""
File that holds the class that represents the player
"""

class Player(object):
    """
    Class representing the player
    """

    def __init__(self):
        self.inventory = {}

    def add_item(self, item):
        """
        Adds an item to the player's inventory

        :param item: Item, the item to add
        """
        if item.tag in self.inventory.keys():
            raise Exception("Attempted to add item already in inventory")
        self.inventory[item.tag] = item

    def remove_item(self, item):
        """
        Removes an item from the player's inventory

        :param item: Item, the item to remove
        """
        if item.tag not in self.inventory.keys():
            raise Exception("Attempted to remove item not in inventory")
        del self.inventory[item.tag]

    def get_inventory_item_names(self):
        """
        Returns a list of names from all items in the player's inventory

        :return list, the list of names for the items in the inventory
        """
        return [item.name for item in self.inventory]
