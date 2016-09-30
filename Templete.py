import JasperAndZot as jz
import unittest
import random

class Templete:
	"""An attempt to construct a Templete for future military games."""

	def __init__(self, game_class_played):
		"""Initialize the game by the passed-in game class"""
		self.game = game_class_played()

	def roll_before_start(self, possible_outcomes):
		"""perform the state-changing roll before a game cycle starts. 
		Assuming all possible outcomes have equal opportunity to be chosen"""
		return random.choice(possible_outcomes)
	

class TestMethods(unittest.TestCase):
	def test_init_jz(self):
		test = Templete(jz.GameState)
		test.game.board.shape = (11, 6)

if __name__ == '__main__':
	unittest.main()