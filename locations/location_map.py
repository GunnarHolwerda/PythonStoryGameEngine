"""
Class representing all possible locations for the current story
"""

import json
import logging
import pprint
from location import Location

class Map:
    """
    Class that will create a graph of locations to be used for
    navigation within the game
    """

    def __init__(self):
        self.locations = {}
        self.edges = []
        self.current_location = None

    def load_map_file(self, filename):
        """
        Loads a JSON file that details the map of locations. Then
        creates the graph of locations to show where you can move from each location

        :param filname: str, the name of the map file to be loaded
        """
        # Loads in file as JSON
        map_dict = json.load(file("locations\\maps\\" + filename))

        # Parses over the locations array in the file and adds each one
        for location in map_dict['locations']:
            self.add_location(Location(location))

        # Parses over the edges array in the file and adds each edge
        for edge in map_dict['edges']:
            self.add_edge(edge['start'], edge['end'])

        logging.debug("Loaded map file from " + filename)

    def add_location(self, location):
        """
        Adds a location to the graph

        :param location: Location, the location object to add
        """
        if not isinstance(location, Location):
            raise Exception("Non location was added to Map")
        if location.id in self.locations.keys():
            raise Exception("Attempted to add location that already exists %s" % location.name)
        self.locations[location.id] = location

    def add_edge(self, location_start_id, location_end_id):
        """
        Adds an edge to the graph

        :param location_start_id: str, the id for the starting location
        :param location_end_id: str, the id for the end location
        """
        if location_start_id == location_end_id:
            raise Exception("Attemted to add an Edge between the same location")
        self.edges.append(
            Edge(self.load_location(location_start_id), self.load_location(location_end_id)))

    def get_destinations_for_location(self, location_id):
        """
            Returns array of possible destinations for the location given

            :param location_id: str, the location_id to find destinations for
            :return: list of locations
        """
        destinations = []
        location = self.load_location(location_id)
        # Iterate over each edge
        for edge in self.edges:
            # Check if the edge contains the location and add to destinations
            if edge.contains(location) == 1:
                destinations.append(edge.end)
            elif edge.contains(location) == 2:
                destinations.append(edge.start)

        logging.debug(pprint.pformat(destinations))

        return destinations

    def load_location(self, location_id):
        """
        Get the location object for the map using the location_id

        :param location_id: str, the id of the location you want to load
        """
        if location_id not in self.locations.keys():
            raise Exception("Could not find location with id: %s" % location_id)
        return self.locations[location_id]


class Edge:
    """
    Represents an edge within the map from one location to another
    """

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def contains(self, location):
        """
        Checks if a location is within the edge

        :param location: Location, the location object to check for

        :return 1, if location is start, 2 if location is end, 0 if not found
        """
        if not self.is_active():
            return 0

        # Check if location exists based off of the name
        # TODO: Possibly overwrite some equivalency function on the objects
        # for a better comparison
        if self.start.name == location.name:
            return 1
        elif self.end.name == location.name:
            return 2
        else:
            return 0

    def is_active(self):
        """
        Returns true if the edge has two active locations, False otherwise
        """
        return self.start.is_active() and self.end.is_active()

    def __str__(self):
        return self.start.name + " -> " +  self.end.name
