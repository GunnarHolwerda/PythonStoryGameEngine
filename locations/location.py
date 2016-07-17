"""
Class to represent a location in the game
"""

import json
import dialog as d
import msvcrt as m

class Location:

    def  __init__(self, dict):
        self.name = dict['name']
        self.active = dict['active']
        self.id = dict['id']
        # Add ability to include examine text and change over time or use a dscript
        self.examine_text = "You are now in the " + self.name
        self.dscript = None
        self.character = None
        self.has_changed = True

    def get_examine_text(self):
        return self.examine_text

    def is_active(self):
        return self.active

    def set_dscript(self, dscript):
        self.dscript = json.load(file('dialog_scripts/' + dscript))

    def set_character(self, character):
        self.character = character
        self.has_changed = True

    def display_actions(self):
        d.clear_speech_box()
        d.set_location_text(self.name)
        if self.character:
            d.set_description_text(self.character.name + " is in front of you")

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
                self.examine()
                valid_input = True
            elif key == '2':
                self.move()
                valid_input = True
            elif key == '3' and self.character:
                self.talk()
                valid_input = True
            elif key == '4' and self.character:
                self.present()
                valid_input = True
            elif key == '0':
                exit()

    def move(self):
        from game_state import GameState
        destinations = GameState.GAME_MAP.get_destinations_for_location(self.id)
        selection = d.list_box("Move to...", destinations)

        GameState.move(destinations[selection - 1].id)

    def examine(self):
        d.speech_box(self.examine_text)

    def talk(self):
        #TODO: Display talking points outlined in characters dscript
        pass

    def present(self):
        #TODO: Create player object that has inventory
        pass

    def start(self):
        if self.has_changed:
            d.speech_box(self.examine_text, dismissable=False)
            d.pause(3)
            d.clear_speech_box()
            # This allows you to have an intro where the player talks to
            # themself, but no other character is present
            if self.dscript:
                d.read_dialog_script(self.dscript['intro'])
            self.has_changed = False

        d.set_location_text(self.name)
        self.display_actions()

    def __str__(self):
        return self.name
