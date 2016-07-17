"""
Class representing all possible locations for the current story
"""

from location import Location
import json
from pprint import pprint

LOCATIONS = {}
EDGES = []
CURRENT_LOCATION = None

def load_map_file(filename):
    map = json.load(file(filename))
    for location in map['locations']:
        add_location(Location(location))

    for edge in map['edges']:
        add_edge(edge['start'], edge['end'])

    set_current_location(map['start_location'])

def add_location(location):
    if type(location) is Location:
        raise Exception("Non location was added to Map")
    if location.name in LOCATIONS.keys():
        raise Exception("Attempted to add location that already exists %s" % location.name)
    LOCATIONS[location.name] = location

def add_edge(location_start_id, location_end_id):
    start = load_location(location_start_id)
    end = load_location(location_end_id)
    EDGES.append(Edge(start, end))

def move(new_location):
    if new_location not in get_destinations_for_location(CURRENT_LOCATION):
        raise Exception("Attempted to move to location with no path")

    set_current_location(new_location)

def set_current_location(location_id):
    location = load_location(location_id)

    if not location.is_active():
        raise Exception("Tried to set current location to not active location")

    CURRENT_LOCATION = location
    CURRENT_LOCATION.start()

def get_destinations_for_location(location):
    """
        Returns array of possible destinations for the location given

        :param : location, the location to find destinations for
        :return: list of locations
    """
    destinations = []
    for edge in EDGES:
        if edge.contains(location) == 1:
            destinations.append(edge.end)
        elif edge.contains(location) == 2:
            destinations.append(edge.start)

    return destinations

def load_location(location_id):
    if location_id not in LOCATIONS.keys():
        raise Exception("Could not find location with id: %s" % location_id)
    return LOCATIONS[location_id]


class Edge:

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def contains(self, location):
        if not self.is_active():
            return 0

        if self.start.name == location.name:
            return 1
        elif self.end.name == location.name:
            return 2
        else:
            return 0

    def is_active(self):
        return self.start.is_active() and self.end.is_active()

    def __str__(self):
        return self.start.name + " -> " +  self.end.name
