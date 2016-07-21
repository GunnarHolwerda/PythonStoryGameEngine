"""
This file houses the class for the object representation of the dscript
"""

import json
from named_object import NamedObject

# TODO: Any dialog should inherit from some Script object that
# ensures there is a script property on the object


class TalkingPoint(NamedObject, object):

    def __init__(self, talking_point):
        """

        :rtype: TalkingPoint
        :type talking_point: dict
        """
        super(TalkingPoint, self).__init__(talking_point['title'])
        self._script = talking_point['script']

    @property
    def script(self):
        """
        :return: the script for the talking point
        :rtype: list
        """
        return self._script


class Dscript(object):
    """
    Object that is created by parsing a dscript
    """

    def __init__(self, filename):
        dscript = json.load(file('dialog_scripts/' + filename))
        self.intro = dscript['intro']
        self.talking_points = []
        for point in dscript['talking_points']:
            self.talking_points.append(TalkingPoint(point))
        self.reactions = dscript['reactions']

    def get_reaction_script_for_item(self, item):
        """
        Returns the reaction script for the item presented
        :param item: the item to get the reaction for
        :type item: Item
        :return: the script for the reaction
        :rtype: list
        """
        # TODO: Possibly create a class for the reactions, have DefaultReaction extend that class
        for reaction in self.reactions:
            if reaction['item_tag'] == item.tag:
                return reaction['script']

        # TODO: Figure out a better way to return the first item from the list
        return self.reactions.reverse()[0]['default_script']

    def get_talking_points(self):
        """
        Returns a list of the titles of the talking points in the dscript

        :return titles of each dscript
        :rtype: list
        """
        # List comprehension to create a list of all of the titles of each
        # talking point
        return self.talking_points

    def get_intro(self):
        """
        Returns the script for the info sequence from the dscript

        :return dialog script for intro
        :rtype list
        """
        return self.intro
