"""
Class representing all possible locations for the current story
"""

from location import Location
import json
import logging
from pprint import pprint

class Map:

    def __init__(self):
        self.locations = {}
        self.edges = []
        self.current_location = None

    def load_map_file(self, filename):
        map_dict = json.load(file(filename))
        for location in map_dict['locations']:
            self.add_location(Location(location))

        for edge in map_dict['edges']:
            self.add_edge(edge['start'], edge['end'])

        logging.debug("Loaded map file from " + filename)

        return self.load_location(map_dict['start_location'])

    def add_location(self, location):
        if type(location) is Location:
            raise Exception("Non location was added to Map")
        if location.name in self.locations.keys():
            raise Exception("Attempted to add location that already exists %s" % location.name)
        self.locations[location.id] = location

    def add_edge(self, location_start_id, location_end_id):
        if location_start_id == location_end_id:
            raise Exception("Attemted to add an Edge between the same location")
        self.edges.append(Edge(self.load_location(location_start_id), self.load_location(location_end_id)))

    def get_destinations_for_location(self, location_id):
        """
            Returns array of possible destinations for the location given

            :param location_id: str,  the location_id to find destinations for
            :return: list of locations
        """
        destinations = []
        location = self.load_location(location_id)
        for edge in self.edges:
            if edge.contains(location) == 1:
                destinations.append(edge.end)
            elif edge.contains(location) == 2:
                destinations.append(edge.start)

        return destinations

    def load_location(self, location_id):
        if location_id not in self.locations.keys():
            raise Exception("Could not find location with id: %s" % location_id)
        return self.locations[location_id]


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
