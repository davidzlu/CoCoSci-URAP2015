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
    """Initializes starting game board with 6 pumpkins and Jasper"""
    board = np.zeros((11, 6))
    board[9, :] = 6
    board[10, 3] = 7
    return board.astype(int)

def board2state(board):
    """ Takes in the board and returns a binary string 
    where 0 represents a hole and 1 represents a peg"""
    state = ''
    for row in range(len(board)):
        state += ''.join(map(str, board[row, :]))
    return state

def state2board(state):
    """ Takes in a binary string state representation
    and returns the board equivalent """
    board = np.zeros(66).astype(int)
    for i in range(len(state)):
        board[i] = state[i]
    return board.reshape((11,6))

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