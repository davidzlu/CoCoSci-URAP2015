import random
import numpy as np
import ast

"""Token Key:
    0 = empty space
    1 = normal zombie
    2 = flaming zombie
    3 = flower bed
    4 = bomb
    5 = x2 (Multiplier)
    6 = pumpkin
    7 = Jasper
    8 = zombie + flower bed
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
    where digits represent tokens according to the token key"""
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

def count_pieces(board):
    state = board2state(board)
    zombieCount, fZombieCount, bombCount, multCount, pumpCount = 0
    for token in state:
        if token == '1':
            zombieCount += 1
        elif token == '8':
            zombieCount += 1
        elif token == '2':
            fZombieCount += 1
        elif token == '4':
            bombCount += 1
        elif token == '5':
            multCount += 1
        elif token == '6':
            pumpCount += 1
    return zombieCount, fZombieCount, bombCount, multCount, pumpCount

class GameState:
    """
    A GameState specifies the current state of the game in terms of:
      1) The arrangment of pieces on the board
      2) The number of each enemy piece left
      3) The number of pumpkins left
      4) The current wave

    """

    def __init__(self, board=create_board(), zombieCount=24, fZombieCount=8, bombCount=4, multCount=3, pumpCount=6, wave=1):
        self.board = board
        self.zombieCount = zombieCount
        self.fZombieCount = fZombieCount
        self.bombCount = bombCount
        self.multCount = multCount
        self.pumpCount = pumpCount
        self.wave = wave

    def getJasperPosition(self):
        """Returns (x, y) coordinate of Jasper.
        """
        y = 0
        for yPos in range(0, 6):
            if self.board[10, yPos] == 7:
                y = yPos
        return (10, y)
        
    def piecesLeft(self):
        """Return the number of pieces left in wave as a float.
        """
        return float(self.zombieCount + self.fZombieCount + self.bombCount + self.multCount)

    def pullPiece(self):
        """Return the next piece pulled from bag, assuming equal 
        probability of any piece being pulled. Does this by splitting
        the interval [0.0, 1.0) into 4 based on the probability of drawing
        a certain piece.
        """
        totalLeft = self.piecesLeft()
        if totalLeft == 0:
            return 0
        zombieRange = self.zombieCount/totalLeft
        fZombieRange = (self.zombieCount+self.fZombieCount)/totalLeft
        bombRange = (self.zombieCount+self.fZombieCount+self.bombCount)/totalLeft
        nextPiece = random.random() # Random number in [0.0, 1.0)
        if nextPiece < zombieRange:
            self.zombieCount -= 1
            return 1
        elif nextPiece < fZombieRange:
            self.fZombieCount -= 1
            return 2
        elif nextPiece < bombRange:
            self.bombCount -= 1
            return 4
        else:
            self.multCount -= 1
            return 5
    def put_piece(self, dice1, dice2):
        if self.wave == 1:
            if dice1 == 1:
                self.board[0][dice2 - 1] = self.pullPiece()
            elif dice1 == 2:
                piece1 = self.pullPiece()
                piece2 = self.pullPiece()
                if dice2 != 1 and dice2 != 6:
                    moves = [[piece1, piece2, dice2 - 1], [piece2, piece1, dice2 - 1], [piece1, piece2, dice2], [piece2, piece1, dice2]]
                elif dice2 == 1:
                    moves = [[piece1, piece2, 1], [piece2, piece1, 1]]
                else:
                    moves[[piece1, piece2, 5], [piece2, piece1, 5]]
                print("Your available moves are: ")
                print(moves)
                my_move = ast.literal_eval(input("Enter the move you'd like to make: "))
                while my_move not in moves:
                    my_move = ast.literal_eval(input("Please enter a valid move: "))
                self.board[0][my_move[2] - 1] = my_move[0]
                self.board[0][my_move[2]] = my_move[1]
            elif dice1 == 3:
                piece1 = self.pullPiece()
                piece2 = self.pullPiece()
                moves = [[piece1, piece2, dice2], [piece2, piece1, dice2]]
                print("Your available moves are: ")
                print(moves)
                my_move = ast.literal_eval(input("Enter the move you'd like to make: "))
                while my_move not in moves:
                    my_move = ast.literal_eval(input("Please enter a valid move: "))
                self.board[0][my_move[2] - 1] = my_move[0]
                self.board[1][my_move[2] - 1] = my_move[1]
            elif dice1 == 4:
                piece1 = self.pullPiece()
                piece2 = self.pullPiece()
                piece3 = self.pullPiece()
                if dice2 != 1 and dice2 != 6:
                    moves = [[piece1, piece2, piece3, dice2 - 1], [piece1, piece3, piece2, dice2 - 1], [piece2, piece1, piece3, dice2 - 1], [piece2, piece3, piece1, dice2 - 1], [piece3, piece1, piece2, dice2 - 1], [piece3, piece2, piece1, dice2 - 1], [piece1, piece2, piece3, dice2], [piece1, piece3, piece2, dice2], [piece2, piece1, piece3, dice2], [piece2, piece3, piece1, dice2], [piece3, piece1, piece2, dice2], [piece3, piece2, piece1, dice2]]
                elif dice2 == 1:
                    moves = [[piece1, piece2, piece3, 1], [piece1, piece3, piece2, 1], [piece2, piece1, piece3, 1], [piece2, piece3, piece1, 1], [piece3, piece1, piece2, 1], [piece3, piece2, piece1, 1]]
                else:
                    [piece1, piece2, piece3, 5], [piece1, piece3, piece2, 5], [piece2, piece1, piece3, 5], [piece2, piece3, piece1, 5], [piece3, piece1, piece2, 5], [piece3, piece2, piece1, 5]
                print("Your available moves are: ")
                print(moves)
                my_move = ast.literal_eval(input("Enter the move you'd like to make: "))
                while my_move not in moves:
                    my_move = ast.literal_eval(input("Please enter a valid move: "))
                self.board[0][my_move[2] - 1] = my_move[0]
                self.board[0][my_move[2]] = my_move[1]
                self.board[1][my_move[2] - 1] = my_move[2]
            elif dice1 == 5:
                piece1 = self.pullPiece()
                piece2 = self.pullPiece()
                piece3 = self.pullPiece()
                if dice2 != 1 and dice2 != 6:
                    moves = [[piece1, piece2, piece3, dice2 - 1], [piece1, piece3, piece2, dice2 - 1], [piece2, piece1, piece3, dice2 - 1], [piece2, piece3, piece1, dice2 - 1], [piece3, piece1, piece2, dice2 - 1], [piece3, piece2, piece1, dice2 - 1], [piece1, piece2, piece3, dice2], [piece1, piece3, piece2, dice2], [piece2, piece1, piece3, dice2], [piece2, piece3, piece1, dice2], [piece3, piece1, piece2, dice2], [piece3, piece2, piece1, dice2]]
                elif dice2 == 1:
                    moves = [[piece1, piece2, piece3, 1], [piece1, piece3, piece2, 1], [piece2, piece1, piece3, 1], [piece2, piece3, piece1, 1], [piece3, piece1, piece2, 1], [piece3, piece2, piece1, 1]]
                else:
                    [piece1, piece2, piece3, 5], [piece1, piece3, piece2, 5], [piece2, piece1, piece3, 5], [piece2, piece3, piece1, 5], [piece3, piece1, piece2, 5], [piece3, piece2, piece1, 5]
                print("Your available moves are: ")
                print(moves)
                my_move = ast.literal_eval(input("Enter the move you'd like to make: "))
                while my_move not in moves:
                    my_move = ast.literal_eval(input("Please enter a valid move: "))
                self.board[0][my_move[2] - 1] = my_move[0]
                self.board[0][my_move[2]] = my_move[1]
                self.board[1][my_move[2]] = my_move[2]
            elif dice1 == 6:
                piece1 = self.pullPiece()
                piece2 = self.pullPiece()
                piece3 = self.pullPiece()
                if dice2 != 1 and dice2 != 6:
                    moves = [[piece1, piece2, piece3, dice2 - 1], [piece1, piece3, piece2, dice2 - 1], [piece2, piece1, piece3, dice2 - 1], [piece2, piece3, piece1, dice2 - 1], [piece3, piece1, piece2, dice2 - 1], [piece3, piece2, piece1, dice2 - 1]]
                elif dice2 == 1:
                    moves = [[piece1, piece2, piece3, 1], [piece1, piece3, piece2, 1], [piece2, piece1, piece3, 1], [piece2, piece3, piece1, 1], [piece3, piece1, piece2, 1], [piece3, piece2, piece1, 1]]
                elif dice2 == 6:
                    moves = [[piece1, piece2, piece3, 5], [piece1, piece3, piece2, 5], [piece2, piece1, piece3, 5], [piece2, piece3, piece1, 5], [piece3, piece1, piece2, 5], [piece3, piece2, piece1, 5]]
                print("Your available moves are: ")
                print(moves)
                my_move = ast.literal_eval(input("Enter the move you'd like to make: "))
                while my_move not in moves:
                    my_move = ast.literal_eval(input("Please enter a valid move: "))
                self.board[0][my_move[2] - 1] = my_move[0]
                self.board[0][my_move[2]] = my_move[1]
                self.board[0][my_move[2] + 1] = my_move[2]
        elif self.wave == 2:
            if dice1 == 1:
                piece1 = self.pullPiece()
                piece2 = self.pullPiece()
                if dice2 != 1 and dice2 != 6:
                    moves = [[piece1, piece2, dice2 - 1], [piece2, piece1, dice2 - 1], [piece1, piece2, dice2], [piece2, piece1, dice2]]
                elif dice2 == 1:
                    moves = [[piece1, piece2, 1], [piece2, piece1, 1]]
                else:
                    moves[[piece1, piece2, 5], [piece2, piece1, 5]]
                print("Your available moves are: ")
                print(moves)
                my_move = ast.literal_eval(input("Enter the move you'd like to make: "))
                while my_move not in moves:
                    my_move = ast.literal_eval(input("Please enter a valid move: "))
                self.board[0][my_move[2] - 1] = my_move[0]
                self.board[1][my_move[2]] = my_move[1]
            elif dice1 == 2:
                piece1 = self.pullPiece()
                piece2 = self.pullPiece()
                if dice2 != 1 and dice2 != 6:
                    moves = [[piece1, piece2, dice2 - 1], [piece2, piece1, dice2 - 1]]
                elif dice2 == 1:
                    moves = [[piece1, piece2, 1], [piece2, piece1, 1]]
                else:
                    moves[[piece1, piece2, 5], [piece2, piece1, 5]]
                print("Your available moves are: ")
                print(moves)
                my_move = ast.literal_eval(input("Enter the move you'd like to make: "))
                while my_move not in moves:
                    my_move = ast.literal_eval(input("Please enter a valid move: "))
                self.board[0][my_move[2] - 1] = my_move[0]
                self.board[0][my_move[2] + 1] = my_move[1]
            elif dice1 == 3:
                piece1 = self.pullPiece()
                piece2 = self.pullPiece()
                if dice2 != 1 and dice2 != 6:
                    moves = [[piece1, piece2, dice2 - 1], [piece2, piece1, dice2 - 1], [piece1, piece2, dice2], [piece2, piece1, dice2]]
                elif dice2 == 1:
                    moves = [[piece1, piece2, 1], [piece2, piece1, 1]]
                else:
                    moves[[piece1, piece2, 5], [piece2, piece1, 5]]
                print("Your available moves are: ")
                print(moves)
                my_move = ast.literal_eval(input("Enter the move you'd like to make: "))
                while my_move not in moves:
                    my_move = ast.literal_eval(input("Please enter a valid move: "))
                self.board[1][my_move[2] - 1] = my_move[0]
                self.board[0][my_move[2]] = my_move[1]
            elif dice1 == 4:
                piece1 = self.pullPiece()
                piece2 = self.pullPiece()
                piece3 = self.pullPiece()
                if dice2 != 1 and dice2 != 6:
                    moves = [[piece1, piece2, piece3, dice2 - 1], [piece1, piece3, piece2, dice2 - 1], [piece2, piece1, piece3, dice2 - 1], [piece2, piece3, piece1, dice2 - 1], [piece3, piece1, piece2, dice2 - 1], [piece3, piece2, piece1, dice2 - 1]]
                elif dice2 == 1:
                    moves = [[piece1, piece2, piece3, 1], [piece1, piece3, piece2, 1], [piece2, piece1, piece3, 1], [piece2, piece3, piece1, 1], [piece3, piece1, piece2, 1], [piece3, piece2, piece1, 1]]
                elif dice2 == 6:
                    moves = [[piece1, piece2, piece3, 5], [piece1, piece3, piece2, 5], [piece2, piece1, piece3, 5], [piece2, piece3, piece1, 5], [piece3, piece1, piece2, 5], [piece3, piece2, piece1, 5]]
                print("Your available moves are: ")
                print(moves)
                my_move = ast.literal_eval(input("Enter the move you'd like to make: "))
                while my_move not in moves:
                    my_move = ast.literal_eval(input("Please enter a valid move: "))
                self.board[0][my_move[2] - 1] = my_move[0]
                self.board[1][my_move[2] - 1] = my_move[1]
                self.board[0][my_move[2] + 1] = my_move[2]
            elif dice1 == 5:
                piece1 = self.pullPiece()
                piece2 = self.pullPiece()
                piece3 = self.pullPiece()
                if dice2 != 1 and dice2 != 6:
                    moves = [[piece1, piece2, piece3, dice2 - 1], [piece1, piece3, piece2, dice2 - 1], [piece2, piece1, piece3, dice2 - 1], [piece2, piece3, piece1, dice2 - 1], [piece3, piece1, piece2, dice2 - 1], [piece3, piece2, piece1, dice2 - 1]]
                elif dice2 == 1:
                    moves = [[piece1, piece2, piece3, 1], [piece1, piece3, piece2, 1], [piece2, piece1, piece3, 1], [piece2, piece3, piece1, 1], [piece3, piece1, piece2, 1], [piece3, piece2, piece1, 1]]
                elif dice2 == 6:
                    moves = [[piece1, piece2, piece3, 5], [piece1, piece3, piece2, 5], [piece2, piece1, piece3, 5], [piece2, piece3, piece1, 5], [piece3, piece1, piece2, 5], [piece3, piece2, piece1, 5]]
                print("Your available moves are: ")
                print(moves)
                my_move = ast.literal_eval(input("Enter the move you'd like to make: "))
                while my_move not in moves:
                    my_move = ast.literal_eval(input("Please enter a valid move: "))
                self.board[0][my_move[2] - 1] = my_move[0]
                self.board[0][my_move[2] + 1] = my_move[1]
                self.board[1][my_move[2] + 1] = my_move[2]
            elif dice1 == 6:
                piece1 = self.pullPiece()
                piece2 = self.pullPiece()
                piece3 = self.pullPiece()
                if dice2 != 1 and dice2 != 6:
                    moves = [[piece1, piece2, piece3, dice2 - 1], [piece1, piece3, piece2, dice2 - 1], [piece2, piece1, piece3, dice2 - 1], [piece2, piece3, piece1, dice2 - 1], [piece3, piece1, piece2, dice2 - 1], [piece3, piece2, piece1, dice2 - 1]]
                elif dice2 == 1:
                    moves = [[piece1, piece2, piece3, 1], [piece1, piece3, piece2, 1], [piece2, piece1, piece3, 1], [piece2, piece3, piece1, 1], [piece3, piece1, piece2, 1], [piece3, piece2, piece1, 1]]
                elif dice2 == 6:
                    moves = [[piece1, piece2, piece3, 5], [piece1, piece3, piece2, 5], [piece2, piece1, piece3, 5], [piece2, piece3, piece1, 5], [piece3, piece1, piece2, 5], [piece3, piece2, piece1, 5]]
                print("Your available moves are: ")
                print(moves)
                my_move = ast.literal_eval(input("Enter the move you'd like to make: "))
                while my_move not in moves:
                    my_move = ast.literal_eval(input("Please enter a valid move: "))
                self.board[0][my_move[2] - 1] = my_move[0]
                self.board[1][my_move[2]] = my_move[1]
                self.board[0][my_move[2] + 1] = my_move[2]
