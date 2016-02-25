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
    11 = bomb + flower bed
    12 = multiplier + flower bed
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
        
    def count_pieces(self):
        state = board2state(self.board)
        zombieCount, fZombieCount, bombCount, multCount, pumpCount = 0
        for token in state:
            if token == '1' or token == '8':
                zombieCount += 1
            elif token == '2':
                fZombieCount += 1
            elif token == '4' or token == '11':
                bombCount += 1
            elif token == '5' or token == '12':
                multCount += 1
            elif token == '6':
                pumpCount += 1
        return zombieCount, fZombieCount, bombCount, multCount, pumpCount

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

    def move(self, token):
        old_pos = (token[0], token[1])
        new_row1 = token[0] + 1
        new_row2 = token[0] + 2
        col = token[1]
        if (new_row2 < 11):
            token_one_ahead = self.board[token[0] + 1, token[1]]
            token_two_ahead = self.board[token[0] + 2, token[1]]
            if (token_one_ahead != 0) and (token_one_ahead != 6) and (token_one_ahead != 3) and (token[0] + 1 != 10):
                self.move((token[0] + 1, token[1], token_one_ahead))
                if token_one_ahead > 7:
                    token_one_ahead = 3
                else:
                    token_one_ahead = 0
            elif (token_one_ahead == 0) and (token_two_ahead != 0) and (token_two_ahead != 6) and (token_two_ahead != 3):
                self.move((token[0] + 2, token[1], token_two_ahead))
                if token_two_ahead > 7:
                    token_two_ahead = 3
                else:
                    token_two_ahead = 0
            if token_one_ahead == 0 and token_two_ahead == 0 and (token[2] < 6 and token[2] != 3): #move two spaces
                self.board[new_row2, col] = token[2]
                self.board[old_pos] = 0
                token = (token[0] + 2, token[1], token[2])
            elif (token_one_ahead == 3 or token_one_ahead > 7) and token[2] == 2: #flaming zombies come thru
                self.burn(token)
                self.move(token)
            elif token_one_ahead == 3 and token[2] != 2: #move into a flower bed
                self.board[new_row1, col] = token[2] + 7
                if self.board[old_pos] > 7: #incase last position was in a flower bed
                    self.board[old_pos] = 3
                    self.board[new_row1, col] = token[2]
                else:
                    self.board[old_pos] = 0
                token = (token[0] + 1, token[1], token[2] + 7)
            elif token_one_ahead == 0 and token[2] > 7: #move out of a flower bed
                self.board[new_row1, col] = token[2] - 7
                self.board[old_pos] = 3
                token = (token[0] + 1, token[1], token[2] - 7)
            elif token[2] == 4 and token_one_ahead == 6: #bomb hits pumpkin
                self.explode(token)
            else:
                self.board[new_row1, col] = token[2]
                self.board[old_pos] = 0
                token = (token[0] + 1, token[1], token[2])
        elif (token[0] + 1 == 10): #token reaches magical barrier
            if token[2] == 4:
                self.explode(token)
            elif token[2] == 5: #multiplier disappears
                self.board[old_pos] = 0
            else: #zombies move to nearest pumpkin
                pass
        else:
            self.board[old_pos] = 0
            #throw an error probably


    # def descend(self):
    #     #!!!be careful not to touch pieces that have already been moved!!!
    #     moving_pieces = []
    #     for j in range(6):
    #         for i in range(10):
    #             if (self.board[i, j] != 0) and (self.board[i, j] != 3) and (self.board[i, j] != 6):
    #                 moving_pieces.append((i, j, self.board[i, j]))
    #     for token in moving_pieces:
    #         self.move(token)


    def find_adjacent(self, row, column):
        """Takes in position of token and returns a list of all tokens immediately adjacent (row, column, token type)"""
        adjacent = []
        if row < 10 and column < 6:
            if column - 1 >= 0 and self.board[row, column - 1] != 0:
                adjacent.append((row, column - 1, self.board[row, column - 1]))
            if column + 1 < 6 and self.board[row, column + 1] != 0:
                adjacent.append((row, column + 1, self.board[row, column + 1]))
            if row - 1 >= 0 and self.board[row - 1, column] != 0:
                adjacent.append((row - 1, column, self.board[row - 1, column]))
            if row + 1 < 10 and self.board[row + 1, column] != 0:
                adjacent.append((row + 1, column, self.board[row + 1, column]))
        return adjacent

    def explode(self, token):
        immediate = self.find_adjacent(token[0], token[1])
        for item in immediate:
            self.board[item[0], item[1]] = 0
            if item[2] == 6:
                self.pumpCount -= 1
            if item[2] == 4: #exploding bombs set off other bombs
                self.explode(item)
        self.board[token[0], token[1]] = 0

    def burn(self, token):
        immediate = self.find_adjacent(token[0], token[1])
        for item in immediate:
            if item[2] == 3:
                self.board[item[0], item[1]] = 0
                self.burn(item)
            if item[2] > 7: #flower beds get burned, but tokens on top do not disappear
                self.board[item[0], item[1]] = item[2] - 7
                self.burn(item)


    # This is code that can be used to get rid of chains of things; lightly tested
    # def destroy_chain(self, token):
    #     immediate = self.find_adjacent(token[0], token[1])
    #     for item in immediate:
    #         self.board[item[0], item[1]] = 0
    #         self.explode(item)
            


if __name__ == '__main__':
    gs = GameState()
    gs.board[0, 0] = 1
    gs.board[0, 1] = 1
    gs.board[0, 2] = 1
    gs.board[2, 0] = 3
    gs.board[1, 0] = 3
    gs.board[1, 1] = 3

