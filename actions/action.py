"""
Class that represents actions the player can do
"""

class Action:
    """ Class the represents an Action the player can take """
    def invoke(self):
        raise NotImplementedError
