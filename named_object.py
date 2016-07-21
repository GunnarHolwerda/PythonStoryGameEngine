"""
This file holds the abstract class NamedObject
"""

# TODO: Do a proper definition of an abstract class using that abc module


class NamedObject(object):
    """
    An abstract class to be inherited by another class to add a name
    to the object
    """

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        """
        :return: The name for the object
        :rtype: str
        """
        return self._name

    """
        Code necessary for checking if two locations are equal to another
        Found at: http://bit.ly/29sdPnH
    """
    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        """Define a non-equality test"""
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def __hash__(self):
        """Override the default hash behavior (that returns the id or the object)"""
        return hash(tuple(sorted(self.__dict__.items())))

