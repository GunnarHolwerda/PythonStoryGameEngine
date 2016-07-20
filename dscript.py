"""
This file houses the class for the object representation of the dscript
"""

import json

class Dscript(object):
    """
    Object that is created by parsing a dscript
    """

    def __init__(self, filename):
        dscript = json.load(file('dialog_scripts/' + filename))
        self.intro = dscript['intro']
        self.talking_points = dscript['talking_points']

    def get_talking_points(self):
        """
        Returns a list of the titles of the talking points in the dscript

        :return list, titles of each dscript
        """
        # List comprehension to create a list of all of the titles of each
        # talking point
        return [tp['title'] for tp in self.talking_points]

    def get_script_for_tp(self, talking_point_index):
        """
        Returns the dialog script for the talking point at the index specified

        :param talking_point_index: int, the index of the talking point

        :return list, the dialog script in list form
        """
        return self.talking_points[talking_point_index]['script']

    def get_intro(self):
        """
        Returns the script for the info sequence from the dscript

        :return list, dialog script for intro
        """
        return self.intro
