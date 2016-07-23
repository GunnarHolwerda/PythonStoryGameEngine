from unittest import TestCase

from locations import Location


class TestLocation(TestCase):
    def setUp(self):
        self.location = Location(
            {"id": "car", "name": "Carnival", "active": False}
        )

    def test_set_active(self):
        self.location.set_active()
        self.assertTrue(self.location.active)

    def test_is_active(self):
        self.assertFalse(self.location.is_active())
        self.location.active = True
        self.assertTrue(self.location.is_active())

    # TODO: all of the actions should be tested in the GameState test probably
