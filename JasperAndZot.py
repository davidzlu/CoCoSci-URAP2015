import random

def diceRoll():
    """Returns a tuple of random integers between 1 and 6 inclusive.
    """
    roll1 = random.randint(1, 6)
    roll2 = random.randint(1, 6)
    return (roll1, roll2)

class GameState:

    def __init__(self, board, wave=1, zombieCount=24, fZombieCount, bombCount, multCount):
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