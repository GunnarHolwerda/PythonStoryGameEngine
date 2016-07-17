"""
Action class representing the Move action
"""
from actions import Action
import msvcrt as m
import locations
from pprint import pprint


class MoveAction(Action):

    def __init__(self, location):
        self.location = location
        self.destinations = locations.get_destinations_for_location(self.location)

    def invoke(self):
        count = 1
        for dest in self.destinations:
            print str(count) + ". " +  dest.name
            count += 1
        self.select_location()

    def select_location(self):
        valid_input = False
        while not valid_input:
            key = m.getch()

            if int(key) in range(1, len(self.destinations) + 1):
                print "Valid input found"
                locations.move(self.destinations[int(key) - 1])
                valid_input = True

            # TODO: Need some sort of back function
