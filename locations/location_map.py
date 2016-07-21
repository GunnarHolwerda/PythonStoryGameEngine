"""
Class representing all possible locations for the current story
"""

import json
import logging
import pprint
from location import Location


class Map(object):
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

        :param filename: the name of the map file to be loaded
        :type filename: str
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

        :param location: the location object to add
        :type location: Location
        """
        if not isinstance(location, Location):
            raise Exception("Non location was added to Map")
        if location.tag in self.locations.keys():
            raise Exception("Attempted to add location that already exists %s" % location.name)
        self.locations[location.tag] = location

    def add_edge(self, location_start_tag, location_end_tag):
        """
        Adds an edge to the graph

        :param location_start_tag: str, the tag for the starting location
        :param location_end_tag: str, the tag for the end location
        """
        if location_start_tag == location_end_tag:
            raise Exception("Attemted to add an Edge between the same location")
        self.edges.append(
            Edge(self.load_location(location_start_tag), self.load_location(location_end_tag)))

    def get_destinations_for_location(self, location_tag):
        """
            Returns array of possible destinations for the location given

            :param location_tag: str, the location_tag to find destinations for
            :return: list of locations
        """
        destinations = []
        location = self.load_location(location_tag)
        # Iterate over each edge
        for edge in self.edges:
            destination = edge.get_destination_from_location(location)
            # If a destination was found add it, otherwise don't
            if destination:
                destinations.append(destination)
        return destinations

    def load_location(self, location_tag):
        """
        Get the location object for the map using the location_tag

        :param location_tag: str, the tag of the location you want to load
        """
        if location_tag not in self.locations.keys():
            raise Exception("Could not find location with tag: %s" % location_tag)
        return self.locations[location_tag]


class Edge(object):
    """
    Represents an edge within the map from one location to another
    """

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def get_destination_from_location(self, location):
        """
        Checks if a location is within the edge

        :param location: Location, the location object to check for

        :return the opposite end of the edge if the location is found, None if not found
        """
        if not self.is_active():
            return None

        if self.start == location:
            return self.end
        elif self.end == location:
            return self.start
        else:
            return None

    def is_active(self):
        """
        Returns true if the edge has two active locations, False otherwise
        """
        return self.start.is_active() and self.end.is_active()

    def __str__(self):
        return self.start.name + " -> " +  self.end.name
