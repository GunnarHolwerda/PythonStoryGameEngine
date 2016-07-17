"""
This file holds functions used in the creation of dialog for the game
"""

import time
import sys
import json
import msvcrt as m
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
    for letter in text:
        sys.stdout.write(letter)
        time.sleep(0.06)
    sys.stdout.flush()
    if dismissable:
        wait()

def clear_speech_box():
    for _ in xrange(4):
        sys.stdout.write('\r')
        sys.stdout.write("\033[2J") # ANSI Escape code to clear terminal
        sys.stdout.write("\033[1;1H") # ANSI Escape code to set cursor to position 1,1 (top letf)
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
    if not key.isspace():
        wait()
