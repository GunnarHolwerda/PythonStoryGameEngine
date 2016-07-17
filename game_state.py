"""
This class will be used to represent the curent state of the game
"""

from locations import Map

class GameState:

	GAME_MAP = Map()
	CURRENT_LOCATION = None

	@staticmethod
	def load_map_file(filename):
		GameState.CURRENT_LOCATION = GameState.GAME_MAP.load_map_file(filename)

	@staticmethod
	def move(new_location_id):
		# TODO: Create check to make sure not making illegal move to impossible location
		GameState.CURRENT_LOCATION = GameState.GAME_MAP.load_location(new_location_id)
		print GameState.CURRENT_LOCATION
		GameState.CURRENT_LOCATION.start()
