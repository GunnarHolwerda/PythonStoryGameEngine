from unittest import TestCase
from locations import Map, Location
from locations.location_map import Edge


class TestMap(TestCase):
    def setUp(self):
        self.Map = Map()
        self.Map.load_map_file("test.map", directory="..\\tests\\test_map_files\\")

    def test_load_map_file(self):
        locations_dict = {
            "law": Location({"id": "law", "name": "Law Office", "active": True}),
            "det": Location({"id": "det", "name": "Detention Center", "active": True}),
            "car": Location({"id": "car", "name": "Carnival", "active": False}),
            "spo": Location({"id": "spo", "name": "Spot", "active": False})
        }
        self.assertDictEqual(self.Map.locations, locations_dict)

        edges_list = [
            Edge(locations_dict['law'], locations_dict['det']),
            Edge(locations_dict['law'], locations_dict['car']),
            Edge(locations_dict['det'], locations_dict['car'])
        ]

        self.assertListEqual(self.Map.edges, edges_list)

    def test_add_location(self):
        """ Tests adding a proper location to the map """
        test_location = Location({"id": "test", "name": "Test", "active": True})
        self.Map.add_location(test_location)
        self.assertIn(test_location, self.Map.locations.values())

    def test_add_edge(self):
        test_edge = Edge(self.Map.locations['spo'], self.Map.locations['law'])
        self.Map.add_edge('spo', 'law')
        self.assertIn(test_edge, self.Map.edges)

    def test_get_destinations_for_location(self):
        expected = [self.Map.load_location('det')]
        destinations = self.Map.get_destinations_for_location("law")
        self.assertListEqual(destinations, expected)

    def test_load_location(self):
        self.assertEqual(self.Map.locations['law'], self.Map.load_location('law'))
