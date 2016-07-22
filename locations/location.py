"""
Class to represent a location in the game
"""

import logging
import ui
import msvcrt as m
from dscript import Dscript
from named_object import NamedObject, ValueComparison


class Location(NamedObject, ValueComparison, object):
    """
    Represents a location in the game
    """

    def  __init__(self, mscript):
        super(Location, self).__init__(mscript['name'])
        self.active = mscript['active']
        self.tag = mscript['id']
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

    def determine_action(self, action):
        """
        Waits for the keypress to determine what action is going to be taken
        """
        # TODO: Refactor
        if action == "1. Examine":
            self.examine()
        elif action == "2. Move":
            self.move()
        elif action == "3. Talk":
            self.talk()
        elif action == "4. Present":
            self.present()
        elif action == "Exit":
            exit()
        else:
            logging.debug("Unknown action attempted")
            raise Exception("Unknown action attempted " + action)

    def move(self):
        """
        Initiates move.
        """
        from game_state import GameState
        # Load destinations for the current location from the current GAME_MAP
        destinations = GameState.GAME_MAP.get_destinations_for_location(self.tag)
        # Display list box for the possible destinations
        selection = ui.list_box("Move to...", destinations)

        # If selection is None then we go back
        if not selection:
            return

        # Updates the current location in the GameState
        GameState.update_current_location(selection)

    def examine(self):
        """
        Examines the current location, currently only displays the examine text
        """
        ui.speech_box(self.examine_text)

    def talk(self):
        """
        Handles all logic for the talking action
        """
        talking_points = self.dscript.get_talking_points()
        talking_point = ui.list_box("Talk about", talking_points)
        # If talking_point is None then we go back
        if not talking_point:
            return

        # TODO: Show that a talking point has been clicked on, once it has been read by the player
        # TODO: Fix that script is not a guaranteed
        ui.read_dialog_script(talking_point.script)

    def present(self):
        """
        Handles the logic for the present action
        """
        from game_state import GameState
        item_selected = ui.inventory_view(GameState.PLAYER.inventory)
        # If selection is None then we go back
        if not item_selected:
            return

        reaction_script = self.dscript.get_reaction_script_for_item(item_selected)
        ui.read_dialog_script(reaction_script)

    def start(self):
        """
        Starts the dscript for the current location.
        This method is called everytime the player moves to the location.
        """
        if self.has_changed:
            # If the location has changed since last visit, display examine text and run new
            # intro sequence if exists
            # TODO: Change from displaying examine text to a time printout like in PW:AA
            ui.speech_box(self.examine_text, dismissable=False)
            ui.pause(3)
            ui.clear_speech_box()

            # This allows you to have an intro where the player talks to
            # themself, but no other character is present
            if self.dscript:
                ui.read_dialog_script(self.dscript.get_intro())
            self.has_changed = False

        action = ui.display_actions(self, self.character)
        self.determine_action(action)
        # endlessly start this location until we move
        self.start()

    def __str__(self):
        return self.name