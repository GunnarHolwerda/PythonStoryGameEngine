"""
Class to represent a location in the game
"""

import logging
import dialog as d
import msvcrt as m
from dscript import Dscript

class Location:
    """
    Represents a location in the game
    """

    def  __init__(self, mscript):
        self.name = mscript['name']
        self.active = mscript['active']
        self.id = mscript['id']
        # Add ability to include examine text and change over time or use a dscript
        self.examine_text = "You are now in the " + self.name
        self.dscript = None
        self.character = None
        self.has_changed = True

    def get_examine_text(self):
        """
        Returns the examine text for the current location
        """
        return self.examine_text

    def set_active(self):
        """
        Sets the location to be active so that it can be discovered as a destination
        """
        self.active = True

    def is_active(self):
        """
        Returns true if location is active, False otherwise
        """
        return self.active

    def set_dscript(self, dscript):
        """
        Sets the dscript (dialog script) for the location

        :param dscript: str, filename for dscript to be loaded
        """
        self.dscript = Dscript(dscript)
        self.has_changed = True

    def set_character(self, character):
        """
        Sets the current character in the location, sets location to having changed

        :param character: Character, the Character object that is in the location
        """
        self.character = character
        self.has_changed = True

    def display_actions(self):
        """
        Displays actions that can be taken at the current location
        """
        # TOOD: Possibly rework this into Dialog and just pass the location as a parameter
        # into the function
        d.clear_speech_box()
        self.display_title_bar()

        print "1. Examine"
        print "2. Move"
        if self.character:
            print "3. Talk"
            print "4. Present"

        self.determine_action()
        self.display_actions()

    def determine_action(self):
        """
        Waits for the keypress to determine what action is going to be taken
        """
        # TODO: Like display actions, possibly rework this into dialog
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
        """
        Initiates move.
        """
        # TODO: Display some sort of back button to go back to actions
        from game_state import GameState
        # Load destinations for the current location from the current GAME_MAP
        destinations = GameState.GAME_MAP.get_destinations_for_location(self.id)
        # Display list box for the possible destinations
        selection = d.list_box("Move to...", destinations)
        # Updates the current location in the GameState
        GameState.update_current_location(destinations[selection].id)

    def examine(self):
        """
        Examines the current location, currently only displays the examine text
        """
        d.speech_box(self.examine_text)

    def talk(self):
        """
        Handles all logic for the taking action
        """
        #TODO: Display talking points outlined in characters dscript
        talking_points = self.dscript.get_talking_points()
        import pprint
        logging.debug(pprint.pformat(talking_points))
        index = d.list_box("Talk about", talking_points)
        script = self.dscript.get_script_for_tp(index)
        d.read_dialog_script(script)

        # TODO: Show that a talking point has been clicked on, once it has
        # been read by the player

    def present(self):
        #TODO: Create player object that has inventory
        pass

    def start(self):
        """
        Starts the dscript for the current location.
        This method is called everytime the player moves to the location.
        """
        if self.has_changed:
            # If the location has changed since last visit, display examine text and run new
            # intro sequence if exists
            # TODO: Change from displaying examine text to a time printout like in PW:AA
            d.speech_box(self.examine_text, dismissable=False)
            d.pause(3)
            d.clear_speech_box()

            # This allows you to have an intro where the player talks to
            # themself, but no other character is present
            if self.dscript:
                d.read_dialog_script(self.dscript.get_intro())
            self.has_changed = False

        self.display_actions()

    def display_title_bar(self):
        """
        Sets the title bar for the current location
        """
        # TODO: Move this to dialog and combine the set_location_text and set_description_text
        # functions
        d.set_location_text(self.name)
        if self.character:
            d.set_description_text(self.character.name + " is in front of you")

    def __str__(self):
        return self.name
