from unittest import TestCase
from locations import Map, Location
from locations.location_map import Edge


class TestMap(TestCase):
    def setUp(self):
        self.map = Map()
        self.map.load_map_file("test.map", directory="..\\tests\\test_map_files\\")

    def test_load_map_file(self):
        locations_dict = {
            "law": Location({"id": "law", "name": "Law Office", "active": True}),
            "det": Location({"id": "det", "name": "Detention Center", "active": True}),
            "car": Location({"id": "car", "name": "Carnival", "active": False}),
            "spo": Location({"id": "spo", "name": "Spot", "active": False})
        }
        self.assertDictEqual(self.map.locations, locations_dict)

        edges_list = [
            Edge(locations_dict['law'], locations_dict['det']),
            Edge(locations_dict['law'], locations_dict['car']),
            Edge(locations_dict['det'], locations_dict['car'])
        ]

        self.assertListEqual(self.map.edges, edges_list)

    def test_add_location(self):
        """ Tests adding a proper location to the map """
        test_location = Location({"id": "test", "name": "Test", "active": True})
        self.map.add_location(test_location)
        self.assertIn(test_location, self.map.locations.values())

    def test_add_edge(self):
        test_edge = Edge(self.map.locations['spo'], self.map.locations['law'])
        self.map.add_edge('spo', 'law')
        self.assertIn(test_edge, self.map.edges)

    def test_get_destinations_for_location(self):
        expected = [self.map.load_location('det')]
        destinations = self.map.get_destinations_for_location("law")
        self.assertListEqual(destinations, expected)

    def test_load_location(self):
        self.assertEqual(self.map.locations['law'], self.map.load_location('law'))

    def test_new_active_location_can_be_found(self):
        # Set an inactive location to active
        self.map.load_location("car").set_active()
        expected = [
            self.map.load_location('det'),
            self.map.load_location('car')
        ]
        destinations = self.map.get_destinations_for_location("law")
        self.assertListEqual(destinations, expected)
