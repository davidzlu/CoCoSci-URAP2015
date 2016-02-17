import random
import numpy as np

"""Key for Tokens:
    0 = empty space
    1 = normal zombie
    2 = flaming zombie
    3 = flower bed
    4 = bomb
    5 = x2 (Multiplier)
    6 = pumpkin
    7 = Jasper
    """

def diceRoll():
    """Returns a tuple of random integers between 1 and 6 inclusive.
    """
    roll1 = random.randint(1, 6)
    roll2 = random.randint(1, 6)
    return (roll1, roll2)

def create_board():
    board = np.zeros((11, 6))
    board[9, :] = 6
    board[10, 3] = 7
    return board.astype(int)


class GameState:

    def __init__(self, board, fZombieCount, bombCount, multCountwave=1, zombieCount=24):
        self.board = board
        self.wave = wave
        self.zombieCount = zombieCount
        self.fZombieCount = fZombieCount
        self.bombCount = bombCount
        self.multCount = multCount

    def piecesLeft(self, state):
        """Return the number of pieces left in wave.
        """
        return state.zombieCount + state.fZombieCount + state.bombCount + state.multCount

    def pullPiece(self, state):
        """Return the next piece pulled from bag, assuming equal 
        probability of any piece being pulled.
        """
        totalLeft = self.piecesLeft(state)

        return 0

# Dictionary of game pieces
# TODO: fill out with number:piece pairing
gamePieces = {}