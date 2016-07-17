"""
This file holds functions used in the creation of dialog for the game
"""

import time
import sys
import json
import msvcrt as m
import threading
from pprint import pprint

def read_dialog_script(filename):
    """
    Reads in JSON array of dialog boxes to be spoken
    """
    dialog = json.load(file(filename))
    cur_character = ""
    for line in dialog:
        if line['character'] != cur_character:
            cur_character = line['character']
            sys.stdout.write(cur_character + "\n")
        speech_box(line['text'])

def speech_box(text, dismissable=True):
    """
    Prints text given to the console, erasing the any previous text from the console
    """
    clear_speech_box()
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
    typewriter("...", sleep_time=1, end="\r")
    sys.stdout.write("\033[J")

def list_box(title, items):
    """
    Displays text box with numbers next to each item in items, returns selected item
    """
    clear_speech_box()
    set_location_text(title)
    count = 1
    text = ""
    for i in items:
        text += str(count) + ". " + str(i) + "\n"
    sys.stdout.write(text)

    return get_selection(len(items))

def get_selection(num_items):
    valid = False
    while not valid:
        key = m.getch()
        if key in [str(x) for x in range(1, num_items + 1)]:
            return int(key)

def typewriter(text, sleep_time=0.06, end="\n"):
    for letter in text:
        sys.stdout.write(letter)
        time.sleep(i)
    sys.stdout.write(end)


def clear_speech_box():
    for _ in xrange(4):
        sys.stdout.write('\r')
        sys.stdout.write("\033[2J") # ANSI Escape code to clear terminal
        sys.stdout.write("\033[1;1H") # ANSI Escape code to set cursor to position 1,1 (top left)
        sys.stdout.flush()

def pause(seconds):
    time.sleep(seconds)

def set_location_text(location_text):
    print(location_text)

def wait(correct_key=""):
    """
    Waits for enter key
    """
    key = m.getch()
    if key.isspace():
        return
    wait()
