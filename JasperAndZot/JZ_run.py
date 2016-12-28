from JasperAndZot import *
from DeckBuilding import *

class JasperAndZot(DeckBuilding):

    def setup_environment(self):
        jz = GameState()
        self.game = jz
        self.board = jz.board
        self.turn = jz.phase

    def setup_friendly_units(self, policy):
        pass

    def setup_enemy_units(self):
        pass

    def roll_to_location(self, roll):
        moves = self.game.possible_moves_2(roll[0], roll[1])
        return moves

    def turn_setup(self, policy):
        self.turn = (self.turn % 4) + 1

    def turn_setup_done(self):
        return True

    def game_loop_done(self):
        pass

    def is_win_state(self):
        return self.board.isWinState()

    def is_lose_state(self):
        return self.board.isLoseState()
