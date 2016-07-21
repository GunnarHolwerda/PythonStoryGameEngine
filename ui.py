"""
This file holds functions used in the creation of dialog for the game
"""

import time
import sys
import threading
import pprint
import logging
import msvcrt as m
from character import Character
from named_object import NamedObject


"""
TODO: Does this function need location and character when it can access character
from location. Or even the current location (which is the only location this should be
called on) from the GameState
"""


def display_actions(location, character):
    """
    Is used to display the actions that a player can make at a location
    :param location: The current location
    :type location: Location
    :param character: The character at the current location
    :type character: Character
    :return: The action to perform
    :rtype: str
    """
    clear_speech_box()
    if character:
        set_title_bar(location.name, description=character.name + " is in front of you")
    else:
        set_title_bar(location.name)

    actions = ["1. Examine", "2. Move"]
    if character:
        actions.append("3. Talk")
        actions.append("4. Present")

    for action in actions:
        sys.stdout.write(action + "\n")

    """
    TODO: Possibly rework any display (display_actions, inventory_view, etc.) not to
    return the selected action and instead set up some sort of listener instead
    """
    selected_action = get_selection(actions)
    # Player pressed 0, the exit key
    if not selected_action:
        return "Exit"
    return selected_action


def inventory_view(inventory):
    """
    Displays the inventory view for the inventory given

    :param inventory: the inventory of the player
    :type: list(Item)

    :return the selected item
    :rtype: Item
    """
    set_title_bar("Items")
    count = 1
    text = ""
    for item in inventory:
        assert isinstance(item, NamedObject)
        text += str(count) + ". " + item.name + "\n"
        count += 1
    text += "0. Back\n"
    sys.stdout.write(text)

    selection = get_selection(inventory)

    return selection


def read_dialog_script(dialog):
    """
    Reads in JSON array of dialog boxes to be spoken
    """
    if not dialog:
        # Return if no dialog given (i.e. no intro script)
        return

    logging.debug(pprint.pformat(dialog))
    for line in dialog:
        char = Character.load_character(line['character'])
        speech_box(line['text'], speaker=char.name)
        if 'unlocks' in line:
            from game_state import GameState
            GameState.update(line['unlocks'])


def speech_box(text, dismissable=True, speaker=""):
    """
    Displays the text given, if speaker is specified will state the speaker before the text is written

    :param text: the text to be written in the speech box
    :type text: str
    :param dismissable: if True requires enter to be pressed to move forward
    :type dismissable: bool
    :param speaker: the name of the character who is talking
    :type speaker: str
    """
    clear_speech_box()
    if speaker:
        text = speaker + ": " + text
    typewriter(text)
    sys.stdout.flush()
    if dismissable:
        wait_thread = threading.Thread(target=wait)
        wait_thread.start()
        while wait_thread.isAlive():
            # TODO: Figure out way to make it so that the whole display_wait function doesn't play
            # if the thread ends. Maybe some sort of thread that always listens for button presses
            # and notifies to anything that subscribes to that thread if a press has occurred
            display_wait()


def display_wait():
    """
    Displays three dots appearing from left to right
    """
    typewriter("...", sleep_time=0.18, end="\r")
    sys.stdout.write("\033[J")


def list_box(title, items):
    """
    Displays text box with numbers next to each item in items

    :param title: str, the title for the list_box
    :type title: str
    :param items: the list of objects to be displayed by name
    :type items: List(NamedObject)

    :return if object is selected from list, None to return the Back selection
    :rtype: NamedObject
    """
    clear_speech_box()
    set_title_bar(title)
    count = 1
    text = ""
    for i in items:
        assert isinstance(i, NamedObject)
        text += str(count) + ". " + i.name + "\n"
        count += 1
    text += "0. Back\n"
    sys.stdout.write(text)

    selection = get_selection(items)
    return selection


def get_selection(items):
    """
    Waits for selection input from a list and returns the selection number

    :param items: list of NamedObjects, the list to get the selection from
    :type items: List(NamedObject)

    :return if found selected, None to return the Back selection
    :rtype: Any
    """
    # TODO: Rework to work with more generic parameter types
    valid = False
    while not valid:
        key = m.getch()
        if key in [str(x) for x in range(1, len(items) + 1)]:
            return items[int(key) - 1]
        elif key == "0":
            return None


def typewriter(text, sleep_time=0.03, end="\n"):
    """
    Prints the text given in typewriter format (one letter at a time)

    :param text: the text to be printed
    :type text: str

    :param sleep_time: the time to sleep between printing each letter (D: 0.06)
    :type sleep_time: float

    :param end: the end of the string (D: "\n")
    :type end: str
    """
    # TODO: Figure out a better way to create the type writer so that a button press can complete the phrase immediately
    for letter in text:
        sys.stdout.write(letter)
        time.sleep(sleep_time)
    sys.stdout.write(end)


def clear_speech_box():
    """
    Clears the whole terminal to a blank screen and places cursor in top left
    """
    for _ in xrange(4):
        sys.stdout.write('\r')
        sys.stdout.write("\033[2J") # ANSI Escape code to clear terminal
        sys.stdout.write("\033[1;1H") # ANSI Escape code to set cursor to position 1,1 (top left)
        sys.stdout.flush()


def pause(seconds):
    """
    Sleeps for the specified number of seconds

    :param seconds: num of seconds to sleep for
    :type seconds: float
    """
    time.sleep(seconds)


def set_title_bar(title, description=""):
    """
    Sets the title bar and description if specified

    :param title: str, the string to display on the top line
    :param description: str, the string to display on the second line (D: "")
    """
    sys.stdout.write(title + "\n")
    if description:
        sys.stdout.write(description + "\n")


def wait(correct_key=""):
    """
    Waits for enter key or spacebar

    :param correct_key: the specific key being waited on (D: "")
    :type correct_key: str
    """
    key = m.getch()
    if key.isspace():
        return
    wait()
