"""
Class representing talk action
"""

from actions import Action

class TalkAction(Action):

    def invoke(self):
        raise NotImplementedError
