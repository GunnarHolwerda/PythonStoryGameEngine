from unittest import TestCase

from game_state import GameState
import json


class TestGameState(TestCase):

    # TODO: Fix the directory issue for loading using initialize game

    def test_update(self):
        # TODO: test this once I get it fleshed out
        pass

    def test_initialize_game(self):
        escript = TestGameState.initialize_game_with_test_escript()
        from locations.location_map import Map
        self.assertIsInstance(GameState.GAME_MAP, Map)

        from player import Player
        self.assertIsInstance(GameState.PLAYER, Player)

        self.assertEqual(GameState.CURRENT_LOCATION.tag, escript['start_location'])

    def test_update_current_location(self):
        escript = TestGameState.initialize_game_with_test_escript()
        GameState.update_current_location('car')
        self.assertEqual(GameState.CURRENT_LOCATION.tag, 'car')

    @staticmethod
    def initialize_game_with_test_escript():
        escript = json.load(file('../tests/test_event_scripts/test.escript'))
        GameState.initialize_game(escript)

        return escript

