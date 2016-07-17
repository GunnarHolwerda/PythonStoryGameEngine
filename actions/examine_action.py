"""
Action class that allows you to examine the current location
"""
from actions import Action
import dialog as d

class ExamineAction(Action):

    def __init__(self, location):
        self.location = location

    def invoke(self):
        d.speech_box(self.location.get_examine_text())
