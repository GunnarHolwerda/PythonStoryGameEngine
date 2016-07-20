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
    Prints text given to the console, erasing the any previous text from the console

    :param text: str, the text to be written in the speechbox
    :param dismissable: bool, if True requires enter to be pressed to move forward
        (D:True)
    :param speaker: str, the name of the character who is talking (D: "")
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
    :param items: list, the list of items to be displayed

    :returns the 0 based index selection, -1 to move back
    """
    clear_speech_box()
    set_title_bar(title)
    count = 1
    text = ""
    for i in items:
        text += str(count) + ". " + str(i) + "\n"
        count += 1
    text += "0. Back\n"
    sys.stdout.write(text)

    return get_selection(len(items))

def get_selection(num_items):
    """
    Waits for selection input from a list and returns the selection number

    :param num_items: int, the total number of items that are being displayed

    :return int, 1 based index of the list for the selection
    """
    valid = False
    while not valid:
        key = m.getch()
        if key in [str(x) for x in range(0, num_items + 1)]:
            return int(key) - 1

def typewriter(text, sleep_time=0.03, end="\n"):
    """
    Prints the text given in typewriter format (one letter at a time)

    :param text: str, the text to be printed
    :param sleep_time: float, the time to sleep between printing each letter (D: 0.06)
    :param end: str, the end of the string (D: "\n")
    """
    #TODO: Figure out a better way to create the type writer so that a button press can
    # complete the phrase immediately
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

    :param seconds: float, num of seconds to sleep for
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

    :param correct_key: str, the specific key being waited on (D: "")
    """
    key = m.getch()
    if key.isspace():
        return
    wait()
