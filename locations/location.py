"""
Class to represent a location in the game
"""

import dialog as d
import msvcrt as m
from actions import TalkAction, PresentAction, MoveAction, ExamineAction

class Location:

    def  __init__(self, dict):
        self.name = dict['name']
        self.active = dict['active']
        # Add ability to include examine text and change over time or use a dscript
        self.examine_text = "placeholder examine text"
        self.character = None
        self.has_changed = True

    def get_examine_text(self):
        return self.examine_text

    def is_active(self):
        return self.active

    def set_character(self, character):
        self.character = character
        self.has_changed = True

    def display_actions(self):
        d.clear_speech_box()
        d.set_location_text(self.name)

        print "1. Examine"
        print "2. Move"
        if self.character:
            print "3. Talk"
            print "4. Present"

        self.determine_action()
        self.display_actions()

    def determine_action(self):
        valid_input = False
        while not valid_input:
            key = m.getch()
            if key == '1':
                ExamineAction(self).invoke()
                valid_input = True
            elif key == '2':
                MoveAction(self).invoke()
                valid_input = True
            elif key == '3' and self.character:
                TalkAction().invoke()
                valid_input = True
            elif key == '4' and self.character:
                PresentAction().invoke()
                valid_input = True
            elif key == '0':
                exit()

    def start(self):
        if self.has_changed:
            d.speech_box(self.examine_text, dismissable=False)
            d.pause(3)
            d.clear_speech_box()
        d.set_location_text(self.name)
        self.display_actions()

    def __str__(self):
        return self.name + ": " + str(self.is_active())
