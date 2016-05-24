import random
import numpy as np
import ast
from copy import deepcopy
from Game import Game

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
    """ Takes in a binary string state representation of
    the game board and returns the board equivalent """
    board = np.zeros(66).astype(int)
    for i in range(len(state)):
        board[i] = state[i]
    return board.reshape((11,6))

class GameState(Game):
    """
    A GameState specifies the current state of the game in terms of:
      1) The arrangment of pieces on the board
      2) The number of each enemy piece left
      3) The number of pumpkins left
      4) The current wave

    """
    tpm = {} # Maps (curState, action, nextState) to transition probability

    def __init__(self, zombieCount=24, fZombieCount=8, bombCount=4, multCount=3, pumpCount=6, wave=1, phase=2, score=0):
        self.board = create_board()
        self.zombieCount = zombieCount
        self.fZombieCount = fZombieCount
        self.bombCount = bombCount
        self.multCount = multCount
        self.pumpCount = pumpCount
        self.wave = wave
        self.phase = phase
        self.score = score
        self.dice1 = 0
        self.dice2 = 0
        self.transitionToWave2 = False

    def diceRoll(self):
        """Returns a tuple of random integers between 1 and 6 inclusive.
        """
        roll1 = random.randint(1, 6)
        roll2 = random.randint(1, 6)
        self.dice1 = roll1
        self.dice2 = roll2
        return (roll1, roll2)

    def getJasperPosition(self):
        """Returns (row, column) coordinate of Jasper.
        """
        column = 0
        for i in range(0, 6):
            if self.board[10, i] == 7:
                column = i
        return (10, column)

    def reward(self, action, nextState):
        """Return reward for transition from taking action in current state and moving
        to nextState.
        """
        nextPossible = self.next_states(action)
        if nextState in nextPossible:
            if nextState.isWinState():
                #add reward for destroying tokens?
                self.score += 100 # Reward for winning game = 100
                return 100
        return 0
        
    def lookup_transition_prob_matrix(self, action, nextState):
        """Returns transition probability given (s, a, s') if it exists in
        transition_prob_matrix. Otherwise calculates the probability, enters it
        into transition_prob_matrix and returns the probability.
        """
        curState = deepcopy(self)
        action = tuple(action)
        if (curState, action, nextState) in GameState.tpm:
            return GameState.tpm[(curState, action, nextState)]
        else:
            prob = self.transition_prob(curState, action, nextState)
            GameState.tpm[(curState, action, nextState)] = prob
            return prob

    def transition_prob_matrix(self):
        return self.tpm

    def next_states(self, action):
        states = []
        next_state = deepcopy(self)
        if self.phase == 1: #states after descend
            states.append(next_state.descend())
        elif self.phase == 0 or self.phase == 2: #states after rolling and placing
            for i in range(1, 7):
                try:
                    # Need to get all possible ways to pull pieces onto board
                    # given that you know the formation
                    next_state = deepcopy(self)
                    next_state.dice1 = i
                    next_state.phase_two(i, action)
                    states.append(next_state)
                except IndexError:
                    continue
        elif self.phase == 3: #states after moving and spellcasting
            next_state.move_and_shoot(action)
            states.append(next_state)
        elif self.phase == 4: #states after smash
            next_state.phase_four(action)
            states.append(next_state)
        return states

    def transition_prob(self, action, nextState):
        """Returns probability of transitioning from curState (self) to nextState given action.
        """
        nextPossible = self.next_states(action)
        if nextState in nextPossible:
            return 1.0/float(len(nextPossible))
        return 0.0

    def getMatrixRow(self, action):
        """Returns row of transition probability matrix, specified by curState (self) and action.
        """
        matrixRow = []
        nextPossible = self.next_states(action)
        curState = deepcopy(self)
        for nextState in nextPossible:
            index = (curState, action, nextState)
            if index not in GameState.tpm:
                GameState.tpm[index] = self.transition_prob(action, nextState)
            matrixRow.append(GameState.tpm[index])
        return matrixRow

    def count_pieces(self):
        """Counts number of enemy pieces and pumpkins are currently on board.
        """
        state = board2state(self.board)
        zombieCount, fZombieCount, bombCount, multCount, pumpCount = [0] * 5
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
        a certain piece. Also accounts for wave transition when out of pieces.
        """
        self.waveTransition()
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

    def waveTransition(self):
        """Manages transitioning between wave 1 and 2. Returns 0 if not changing waves.
        Returns True and adds pieces for wave 2 back into the state if changing from
        wave 1 to wave 2. Changing self.wave occurs in phase_two
        """
        if self.wave == 1 and self.piecesLeft() == 0 or self.wave == 1 and self.piecesLeft() > 0 and self.pumpCount < 6:
            zCount, fzCount, bCount, mCount, pCount = self.count_pieces()
            self.zombieCount = 24-zCount
            self.fZombieCount = 8-fzCount
            self.bombCount = 4-bCount
            self.multCount = 4-mCount
            self.pumpCount = 6-pCount
            self.transitionToWave2 = True
            return True
        return False

    def pumpkinCount(self):
        """Counts pumpkins still on board.
        """
        pCount = 0
        for space in self.board[9]:
            if space == 6:
                pCount += 1
        return pCount

    def isWinState(self):

        def enemyOnBoard():
            """Checks if any enemy pieces still on board.
            """
            zCount, fZCount, bCount, mCount, pCount = self.count_pieces()
            return zCount > 0 or fZCount > 0 or bCount > 0 or mCount > 0
        return self.wave == 2 and self.pumpkinCount() > 0 and self.piecesLeft() == 0 and enemyOnBoard()

    def isLoseState(self):
        return self.pumpkinCount() <= 0 

    def phase_two(self, dice1, my_move):
        if self.wave == 1:
            if dice1 == 1:
                self.board[0][my_move[1]] = my_move[0][0] #needs to be specified so that next_states works properly
            elif dice1 == 2:
                self.board[0][my_move[1] - 1] = my_move[0][0]
                self.board[0][my_move[1]] = my_move[0][1]
            elif dice1 == 3:
                self.board[0][my_move[1] - 1] = my_move[0][0]
                self.board[1][my_move[1] - 1] = my_move[0][1]
            elif dice1 == 4:
                self.board[0][my_move[1] - 1] = my_move[0][0]
                self.board[0][my_move[1]] = my_move[0][1]
                self.board[1][my_move[1] - 1] = my_move[0][2]
            elif dice1 == 5:
                self.board[0][my_move[1] - 1] = my_move[0][0]
                self.board[0][my_move[1]] = my_move[0][1]
                self.board[1][my_move[1]] = my_move[0][2]
            elif dice1 == 6:
                self.board[0][my_move[1] - 1] = my_move[0][0]
                self.board[0][my_move[1]] = my_move[0][1]
                self.board[0][my_move[1] + 1] = my_move[0][2]
        elif self.wave == 2:
            if dice1 == 1:
                self.board[0][my_move[1] - 1] = my_move[0][0]
                self.board[1][my_move[1]] = my_move[0][1]
            elif dice1 == 2:
                self.board[0][my_move[1] - 1] = my_move[0][0]
                self.board[0][my_move[1] + 1] = my_move[0][1]
            elif dice1 == 3:
                self.board[1][my_move[1] - 1] = my_move[0][0]
                self.board[0][my_move[1]] = my_move[0][1]
            elif dice1 == 4:
                self.board[0][my_move[1] - 1] = my_move[0][0]
                self.board[1][my_move[1] - 1] = my_move[0][1]
                self.board[0][my_move[1] + 1] = my_move[0][2]
            elif dice1 == 5:
                self.board[0][my_move[1] - 1] = my_move[0][0]
                self.board[0][my_move[1] + 1] = my_move[0][1]
                self.board[1][my_move[1] + 1] = my_move[0][2]
            elif dice1 == 6:
                self.board[0][my_move[1] - 1] = my_move[0][0]
                self.board[1][my_move[1]] = my_move[0][1]
                self.board[0][my_move[1] + 1] = my_move[0][2]

        if self.transitionToWave2:
            self.wave = 2
            self.transitionToWave2 = False

    """Helper method for descend() which takens in a token in the format (row, column, type). Moves only one token,
    unless there are tokens obstructing its movement, in which case those other tokens move as well."""
    def move(self, token):
        old_pos = (token[0], token[1])
        new_row1 = token[0] + 1
        new_row2 = token[0] + 2
        col = token[1]
        if (new_row2 < 10):
            token_one_ahead = self.board[token[0] + 1, token[1]]
            token_two_ahead = self.board[token[0] + 2, token[1]]
            if (token_one_ahead != 0) and (token_one_ahead != 6) and (token_one_ahead != 3) and (token[0] + 1 != 10):
                self.move((token[0] + 1, token[1], token_one_ahead))
            elif (token_one_ahead == 0) and (token_two_ahead != 0) and (token_two_ahead != 6) and (token_two_ahead != 3):
                self.move((token[0] + 2, token[1], token_two_ahead))
            token_one_ahead = self.board[token[0] + 1, token[1]]
            token_two_ahead = self.board[token[0] + 2, token[1]]        
            if token_one_ahead == 0 and token_two_ahead == 0 and (token[2] < 6 and token[2] != 3): #move two spaces
                self.board[new_row2, col] = token[2]
                self.board[old_pos] = 0
                token = (token[0] + 2, token[1], token[2])
                token_one_ahead = self.board[token[0] + 1, token[1]]
                if token[2] == 4 and token_one_ahead == 6:
                    self.explode(token)
                elif token[2] == 4 and token[0] == 9:
                    self.explode(token)
            elif (token_one_ahead == 3 or token_one_ahead > 7) and token[2] == 2: #flaming zombies come thru
                self.burn((new_row1, token[1], token[2]))
                self.board[new_row1, token[1]] = token[2]
                self.board[old_pos] = 0
            elif (token_one_ahead == 0) and (token_two_ahead == 3) and (token[2] == 2):
                self.burn((new_row2, token[1], token[2]))
                self.board[new_row2, token[1]] = token[2]
                self.board[old_pos] = 0
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
            elif token_one_ahead == 0: #move forward one space
                self.board[new_row1, col] = token[2]
                self.board[old_pos] = 0
                token = (token[0] + 1, token[1], token[2])
            else:
                pass
        elif (new_row1 < 10): #token reaches magical barrier
            token_one_ahead = self.board[token[0] + 1, token[1]]
            token_two_ahead = self.board[token[0] + 2, token[1]]
            if (token_one_ahead != 0) and (token_one_ahead != 6) and (token_one_ahead != 3) and (token[0] + 1 != 10):
                self.move((token[0] + 1, token[1], token_one_ahead))
                if token_one_ahead > 7:
                    token_one_ahead = 3
                else:
                    token_one_ahead = 0
            if token[2] == 4 or token[2] == 11:
                token = (new_row1, col, token[2])
                self.board[old_pos] = 0
                self.explode(token)
            elif (token[2] == 5 or token[2] == 12) and token_one_ahead == 0: #multiplier disappears
                if token[2] == 12:
                    self.board[old_pos] = 3
                else:
                    self.board[old_pos] = 0
            elif token[2] != 3 and self.board[new_row1, col] != 6: 
                if self.board[new_row1, col] == 3:
                    if token[2] == 2:
                        self.burn((new_row1, col, 2))
                        self.board[new_row1, col] = 2
                        self.board[old_pos] = 0
                    else:
                        self.board[new_row1, col] = 8
                        if token[2] == 8:
                            self.board[old_pos] = 3
                        else:
                            self.board[old_pos] = 0
                elif token[2] == 8:
                    self.board[new_row1, col] = 1
                    self.board[old_pos] = 3
                else:
                    self.board[new_row1, col] = token[2]
                    self.board[old_pos] = 0
            else: #token is probably a flower bed
                pass
        elif (token[0] == 9) and token[2] != 3 and token[2] != 6: #zombies move to nearest pumpkin
            one_left = token[1] - 1
            two_left = token[1] - 2
            one_right = token[1] + 1
            two_right = token[1] + 2
            old_pos = (token[0], token[1])
            #First determine which direction the zombie will move
            direction = self.nearest_pumpkin(token)
            #Then move
            if (direction == 'left'):
                token_one_left = self.board[9, one_left]
                dir_one_left = self.nearest_pumpkin((9, one_left, token_one_left))
                token_two_left = self.board[9, two_left]
                dir_two_left = self.nearest_pumpkin((9, two_left, token_two_left))
                if token_one_left != 0 or token_one_left != 6 or token_one_left != 3:
                    if dir_one_left == 'left':
                        self.move((9, one_left, token_one_left))
                elif token_two_left != 0 or token_two_left != 6 or token_two_left != 3:
                    if dir_two_left == 'left':
                        self.move((9, two_left, token_two_left))
                token_one_left = self.board[9, one_left]
                token_two_left = self.board[9, two_left]
                if token_one_left == 3:
                    if token[2] == 2:
                        self.burn((token[0], one_left, 2))
                        if self.board[9, two_left] == 0:
                            self.board[9, two_left] = 2
                        else:
                            self.board[9, one_left] = 2
                        self.board[old_pos] = 0
                    else:
                        self.board[9, one_left] = 8
                        if token[2] == 8:
                            self.board[old_pos] = 3
                        else:
                            self.board[old_pos] = 0
                        token = (9, one_left, 8)
                elif token[2] == 8:
                    if self.board[9, one_left] == 0:
                        self.board[9, one_left] = 1
                        self.board[old_pos] = 3
                        token = (9, one_left, 1)
                elif self.board[9, two_left] == 0 and self.board[9, one_left] == 0:
                    self.board[9, two_left] = token[2]
                    self.board[old_pos] = 0
                    token = (token, two_left, token[2])
                elif self.board[9, one_left] == 0:
                    self.board[9, one_left] = token[2]
                    self.board[old_pos] = 0
                    token = (9, one_left, token[2])
                else:
                    pass
            elif (direction == 'right'):
                token_one_right = self.board[9, one_right]
                dir_one_right = self.nearest_pumpkin((9, one_right, token_one_right))
                token_two_right = self.board[9, two_right]
                dif_two_right = self.nearest_pumpkin((9, two_right, token_two_right))
                if token_one_right != 0 or token_one_right != 6 or token_one_right != 3:
                    if dir_one_right == 'right':
                        self.move((9, one_right, token_one_right))
                elif token_two_right != 0 or token_two_right != 6 or token_two_right != 3:
                    if dif_two_right == 'right':
                        self.move((9, two_right, token_two_right))
                token_one_right = self.board[9, one_right]
                token_two_right = self.board[9, two_right]
                if self.board[9, one_right] == 3:
                    if token[2] == 2:
                        self.burn((token[0], one_right, 2))
                        if self.board[9, two_right] == 0:
                            self.board[9, two_right] = 2
                        else:
                            self.board[9, one_right] = 2
                        self.board[old_pos] = 0
                    else:
                        self.board[9, one_right] = 8
                        if token[2] == 8:
                            self.board[old_pos] = 3
                        else:
                            self.board[old_pos] = 0
                        token = (9, one_right, 8)
                elif token[2] == 8:
                    if self.board[9, one_right] == 0:
                        self.board[9, one_right] = 1
                        self.board[old_pos] = 3
                        token = (9, one_right, 1)
                elif self.board[9, two_right] == 0 and self.board[9, one_right] == 0:
                    self.board[9, two_right] = token[2]
                    self.board[old_pos] = 0
                    token = (token, two_right, token[2])
                elif self.board[9, one_right] == 0:
                    self.board[9, one_right] = token[2]
                    self.board[old_pos] = 0
                    token = (9, one_right, token[2])
                else: #don't move!
                    pass
            else: #don't move!
                pass

    """Phase 1 of the game"""
    def descend(self):
        moving_pieces = []
        exclude = []
        for j in range(6):
            for i in range(10):
                if (self.board[i, j] != 0) and (self.board[i, j] != 3) and (self.board[i, j] != 6):
                    if (i + 1 < 10):
                        if self.board[i + 1, j] != 0 and self.board[i + 1, j] != 3 and self.board[i + 1, j] != 6:
                            exclude.append((i + 1, j, self.board[i + 1, j]))
                    if (i + 2 < 10):
                        if self.board[i + 2, j] != 0 and self.board[i + 2, j] != 3 and self.board[i + 2, j] != 6:
                            exclude.append((i + 2, j, self.board[i + 2, j]))
                    token = (i, j, self.board[i, j])
                    if token not in exclude:
                        moving_pieces.append(token)
        for token in moving_pieces:
            self.move(token)


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

    """Action for bombs"""
    def explode(self, token):
        immediate = self.find_adjacent(token[0], token[1])
        for item in immediate:
            self.board[item[0], item[1]] = 0
            if item[2] == 6:
                self.score -= 10
                self.pumpCount -= 1
            if item[2] == 4: #exploding bombs set off other bombs
                self.explode(item)
        self.board[token[0], token[1]] = 0

    """Action for the flaming zombie"""
    def burn(self, token):
        immediate = self.find_adjacent(token[0], token[1])
        for item in immediate:
            if item[2] == 3:
                self.board[item[0], item[1]] = 0
                self.burn(item)
            if item[2] > 7: #flower beds get burned, but tokens on top do not disappear
                self.board[item[0], item[1]] = item[2] - 7
                self.burn(item)

    """Helper method for move; sets direction for zombies to move when in pumpkin patch"""
    def nearest_pumpkin(self, token):
        one_left = token[1] - 1
        two_left = token[1] - 2
        one_right = token[1] + 1
        two_right = token[1] + 2
        direction = 'stop'
        if token[1] == 0:
            direction = 'right'
        elif token[1] == 5:
            direction = 'left'
        elif token[1] == 1:
            if self.board[9, one_left] != 6:
                direction = 'right'
            else:
                direction = 'stop'
        elif token[1] == 4:
            if self.board[9, one_right] != 6:
                direction = 'left'
            else:
                direction = 'stop'
        elif self.board[9, two_left] == 6 and self.board[9, two_right] == 6:
            direction = random.choice(['left', 'right'])
        elif self.board[9, two_right] == 6 and self.board[9, one_left] != 6:
            direction = 'right'
            if self.board[9, one_right] != 0 and self.board[9, one_right] != 3:
                direction = 'stop'
        elif self.board[9, two_left] == 6 and self.board[9, one_right] != 6:
            direction = 'left'
            if self.board[9, one_left] != 0 and self.board[9, one_left] != 3:
                direction = 'stop'
        else: #two spaces on either side show no signs of pumpkins
            if token[1] == 2:
                direction = 'right'
            else:
                direction = 'left'
        return direction

    
    def flower(self, token):
        immediate = self.find_adjacent(token[0], token[1])
        if token[2] == 1 or token[2] == 2 or token[2] == 5 or token[2] == 8 or token[2] == 12:
            self.board[token[0]][token[1]] = 3
            for item in immediate:
                if item[2] == 1 or item[2] == 2 or item[2] == 5 or item[2] == 8 or item[2] == 12 or token[2] == 4 or token[2] == 11:
                    self.flower(item)
        elif token[2] == 4 or token[2] == 11:
            self.explode(token)

    def fire(self, token):
        immediate = self.find_adjacent(token[0], token[1])
        score = 0
        multiplier = 0
        if token[2] == 1 or token[2] == 2:
            self.board[token[0]][token[1]] = 0
            score = score + 2
            for item in immediate:
                if item[2] == 1 or item[2] == 2 or item[2] == 3 or item[2] == 5 or item[2] == 8 or item[2] == 12 or token[2] == 4 or token[2] == 11:
                    score = score + self.fire(item)[0]
                    multiplier = multiplier + self.fire(item)[1]
        elif token[2] == 8:
            self.board[token[0]][token[1]] = 0
            score = score + 3
            for item in immediate:
                if item[2] == 1 or item[2] == 2 or item[2] == 3 or item[2] == 5 or item[2] == 8 or item[2] == 12 or token[2] == 4 or token[2] == 11:
                    score = score + self.fire(item)[0]
                    multiplier = multiplier + self.fire(item)[1]
        elif token[2] == 3:
            self.board[token[0]][token[1]] = 0
            score = score + 1
            for item in immediate:
                if item[2] == 1 or item[2] == 2 or item[2] == 3 or item[2] == 5 or item[2] == 8 or item[2] == 12 or token[2] == 4 or token[2] == 11:
                    score = score + self.fire(item)[0]
                    multiplier = multiplier + self.fire(item)[1]
        elif token[2] == 4 or token[2] == 11:
            self.explode(token)
        elif token[2] == 5:
            self.board[token[0]][token[1]] = 0
            multiplier = multiplier + 1
            for item in immediate:
                if item[2] == 1 or item[2] == 2 or item[2] == 3 or item[2] == 5 or item[2] == 8 or item[2] == 12 or token[2] == 4 or token[2] == 11:
                    score = score + self.fire(item)[0]
                    multiplier = multiplier + self.fire(item)[1]
        elif token[2] == 12:
            self.board[token[0]][token[1]] = 0
            score = score + 1
            multiplier = multiplier + 1
            for item in immediate:
                if item[2] == 1 or item[2] == 2 or item[2] == 3 or item[2] == 5 or item[2] == 8 or item[2] == 12 or token[2] == 4 or token[2] == 11:
                    score = score + self.fire(item)[0]
                    multiplier = multiplier + self.fire(item)[1]
        return (score, multiplier)


    move_3 = []
    def move_and_shoot(self, my_move_3):
        jasper_x = self.getJasperPosition()[1]
        for spell in range(0, 3): #1.flower 2.fire 3.do nothing
            for column in range(max(0, jasper_x - 3), min(jasper_x + 3, 5)):
                GameState.move_3.append([spell, column])
        self.board[10, jasper_x] = 0
        self.board[10, my_move_3[1]] = 7
        if my_move_3[0] == 0:#flower power
            for index in range(0, 4):
                row = 9 - index
                token_type = self.board[row][my_move_3[1]]
                if token_type == 1 or token_type == 2 or token_type == 4 or token_type == 5 or token_type > 7:
                    token = (row, my_move_3[1], token_type)
                    self.flower(token)
                    break
        elif my_move_3[0] == 1: #magic fire
            for index in range(0, 4):
                row = 9 - index
                token_type = self.board[row][my_move_3[1]]
                if token_type == 3 or token_type > 7:
                    token = (row, my_move_3[1], token_type)
                    self.score = self.fire(token)[0] * (2 ** self.fire(token)[1]) + self.score
                    break


    def phase_four(self, pump_chosen):
        for row in range(8, 10):
            for column in range(0, 6):
                if self.board[row][column] == 1 or self.board[row][column] == 2:
                    adjacent = self.find_adjacent(row, column)
                    pump = []
                    for item in adjacent:
                        if item[2] == 6:
                            pump.append(item)
                    if len(pump) == 1:
                        if pump[0] is None:
                            break
                        else:
                            self.board[pump[0][0]][pump[0][1]] = 0
                            self.score = self.score - 10
                            self.pumpCount -= 1
                    elif len(pump) == 2:
                        self.board[pump_chosen[0]][pump_chosen[1]] = 0
                        self.score = self.score - 10
                        self.pumpCount -= 1

    def possible_moves_2(self, dice1, dice2):
        """takes in state and two dices, return all possible moves and a boolean called transition
        that marks if the game needs to transition to wave 2 in phase_two"""
        if self.wave == 1:
            if dice1 == 1:
                piece1 = self.pullPiece()
                return [[[piece1], dice2 - 1]]
            elif dice1 == 2:
                piece1 = self.pullPiece()
                piece2 = self.pullPiece()
                
                if dice2 != 1 and dice2 != 6:
                    return [[[piece1, piece2], dice2 - 1], [[piece2, piece1], dice2 - 1],
                            [[piece1, piece2], dice2], [[piece2, piece1], dice2]]
                elif dice2 == 1:
                    return [[[piece1, piece2], 1], [[piece2, piece1], 1]]
                else:
                    return [[[piece1, piece2], 5], [[piece2, piece1], 5]]
            elif dice1 == 3:
                piece1 = self.pullPiece()
                piece2 = self.pullPiece()
                
                return [[[piece1, piece2], dice2], [[piece2, piece1], dice2]]
            elif dice1 == 4:
                piece1 = self.pullPiece()
                piece2 = self.pullPiece()
                piece3 = self.pullPiece()

                if dice2 != 1 and dice2 != 6:
                    return [[[piece1, piece2, piece3], dice2 - 1], [[piece1, piece3, piece2], dice2 - 1],
                            [[piece2, piece1, piece3], dice2 - 1], [[piece2, piece3, piece1], dice2 - 1],
                            [[piece3, piece1, piece2], dice2 - 1], [[piece3, piece2, piece1], dice2 - 1],
                            [[piece1, piece2, piece3], dice2], [[piece1, piece3, piece2], dice2],
                            [[piece2, piece1, piece3], dice2], [[piece2, piece3, piece1], dice2],
                            [[piece3, piece1, piece2], dice2], [[piece3, piece2, piece1], dice2]]
                elif dice2 == 1:
                    return [[[piece1, piece2, piece3], 1], [[piece1, piece3, piece2], 1],
                            [[piece2, piece1, piece3], 1], [[piece2, piece3, piece1], 1],
                            [[piece3, piece1, piece2], 1], [[piece3, piece2, piece1], 1]]
                else:
                    return [[[piece1, piece2, piece3], 5], [[piece1, piece3, piece2], 5],
                            [[piece2, piece1, piece3], 5], [[piece2, piece3, piece1], 5],
                            [[piece3, piece1, piece2], 5], [[piece3, piece2, piece1], 5]]
            elif dice1 == 5:
                piece1 = self.pullPiece()
                piece2 = self.pullPiece()
                piece3 = self.pullPiece()
                if dice2 != 1 and dice2 != 6:
                    return [[[piece1, piece2, piece3], dice2 - 1], [[piece1, piece3, piece2], dice2 - 1],
                            [[piece2, piece1, piece3], dice2 - 1], [[piece2, piece3, piece1], dice2 - 1],
                            [[piece3, piece1, piece2], dice2 - 1], [[piece3, piece2, piece1], dice2 - 1],
                            [[piece1, piece2, piece3], dice2], [[piece1, piece3, piece2], dice2],
                            [[piece2, piece1, piece3], dice2], [[piece2, piece3, piece1], dice2],
                            [[piece3, piece1, piece2], dice2], [[piece3, piece2, piece1], dice2]]
                elif dice2 == 1:
                    return [[[piece1, piece2, piece3], 1], [[piece1, piece3, piece2], 1],
                            [[piece2, piece1, piece3], 1], [[piece2, piece3, piece1], 1],
                            [[piece3, piece1, piece2], 1], [[piece3, piece2, piece1], 1]]
                else:
                    return [[[piece1, piece2, piece3], 5], [[piece1, piece3, piece2], 5],
                            [[piece2, piece1, piece3], 5], [[piece2, piece3, piece1], 5],
                            [[piece3, piece1, piece2], 5], [[piece3, piece2, piece1], 5]]
            elif dice1 == 6:
                piece1 = self.pullPiece()
                piece2 = self.pullPiece()
                piece3 = self.pullPiece()

                if dice2 != 1 and dice2 < 5:
                    return [[[piece1, piece2, piece3], dice2 - 1], [[piece1, piece3, piece2], dice2 - 1],
                            [[piece2, piece1, piece3], dice2 - 1], [[piece2, piece3, piece1], dice2 - 1],
                            [[piece3, piece1, piece2], dice2 - 1], [[piece3, piece2, piece1], dice2 - 1],
                            [[piece1, piece2, piece3], dice2], [[piece1, piece3, piece2], dice2],
                            [[piece2, piece1, piece3], dice2], [[piece2, piece3, piece1], dice2],
                            [[piece3, piece1, piece2], dice2], [[piece3, piece2, piece1], dice2]]
                elif dice2 == 1:
                    return [[[piece1, piece2, piece3], 1], [[piece1, piece3, piece2], 1],
                            [[piece2, piece1, piece3], 1], [[piece2, piece3, piece1], 1],
                            [[piece3, piece1, piece2], 1], [[piece3, piece2, piece1], 1]]
                else:
                    return [[[piece1, piece2, piece3], 4], [[piece1, piece3, piece2], 4],
                            [[piece2, piece1, piece3], 4], [[piece2, piece3, piece1], 4],
                            [[piece3, piece1, piece2], 4], [[piece3, piece2, piece1], 4]]
        elif self.wave == 2:
            if dice1 == 1:
                piece1 = self.pullPiece()
                piece2 = self.pullPiece()
                
                if dice2 != 1 and dice2 != 6:
                    return [[[piece1, piece2], dice2 - 1], [[piece2, piece1], dice2 - 1],
                            [[piece1, piece2], dice2], [[piece2, piece1], dice2]]
                elif dice2 == 1:
                    return [[[piece1, piece2], 1], [[piece2, piece1], 1]]
                else:
                    return [[[piece1, piece2], 5], [[piece2, piece1], 5]]
            elif dice1 == 2:
                piece1 = self.pullPiece()
                piece2 = self.pullPiece()
                
                if dice2 != 1 and dice2 != 6:
                    return [[[piece1, piece2], dice2 - 1], [[piece2, piece1], dice2 - 1]]
                elif dice2 == 1:
                    return [[[piece1, piece2], 1], [[piece2, piece1], 1]]
                else:
                    return [[[piece1, piece2], 4], [[piece2, piece1], 4]]
            elif dice1 == 3:
                piece1 = self.pullPiece()
                piece2 = self.pullPiece()
                
                if dice2 != 1 and dice2 != 6:
                    return [[[piece1, piece2], dice2 - 1], [[piece2, piece1], dice2 - 1],
                            [[piece1, piece2], dice2], [[piece2, piece1], dice2]]
                elif dice2 == 1:
                    return [[[piece1, piece2], 1], [[piece2, piece1], 1]]
                else:
                    return [[[piece1, piece2], 5], [[piece2, piece1], 5]]
            elif dice1 == 4:
                piece1 = self.pullPiece()
                piece2 = self.pullPiece()
                piece3 = self.pullPiece()
                
                if dice2 != 1 and dice2 < 5:
                    return [[[piece1, piece2, piece3], dice2 - 1], [[piece1, piece3, piece2], dice2 - 1],
                            [[piece2, piece1, piece3], dice2 - 1], [[piece2, piece3, piece1], dice2 - 1],
                            [[piece3, piece1, piece2], dice2 - 1], [[piece3, piece2, piece1], dice2 - 1],
                            [[piece1, piece2, piece3], dice2], [[piece1, piece3, piece2], dice2],
                            [[piece2, piece1, piece3], dice2], [[piece2, piece3, piece1], dice2],
                            [[piece3, piece1, piece2], dice2], [[piece3, piece2, piece1], dice2]]
                elif dice2 == 1:
                    return [[[piece1, piece2, piece3], 1], [[piece1, piece3, piece2], 1],
                            [[piece2, piece1, piece3], 1], [[piece2, piece3, piece1], 1],
                            [[piece3, piece1, piece2], 1], [[piece3, piece2, piece1], 1]]
                else:
                    return [[[piece1, piece2, piece3], 4], [[piece1, piece3, piece2], 4],
                            [[piece2, piece1, piece3], 4], [[piece2, piece3, piece1], 4],
                            [[piece3, piece1, piece2], 4], [[piece3, piece2, piece1], 4]]
            elif dice1 == 5:
                piece1 = self.pullPiece()
                piece2 = self.pullPiece()
                piece3 = self.pullPiece()
                
                if dice2 != 1 and dice2 < 5:
                    return [[[piece1, piece2, piece3], dice2 - 1], [[piece1, piece3, piece2], dice2 - 1],
                            [[piece2, piece1, piece3], dice2 - 1], [[piece2, piece3, piece1], dice2 - 1],
                            [[piece3, piece1, piece2], dice2 - 1], [[piece3, piece2, piece1], dice2 - 1],
                            [[piece1, piece2, piece3], dice2], [[piece1, piece3, piece2], dice2],
                            [[piece2, piece1, piece3], dice2], [[piece2, piece3, piece1], dice2],
                            [[piece3, piece1, piece2], dice2], [[piece3, piece2, piece1], dice2]]
                elif dice2 == 1:
                    return [[[piece1, piece2, piece3], 1], [[piece1, piece3, piece2], 1],
                            [[piece2, piece1, piece3], 1], [[piece2, piece3, piece1], 1],
                            [[piece3, piece1, piece2], 1], [[piece3, piece2, piece1], 1]]
                else:
                    return [[[piece1, piece2, piece3], 4], [[piece1, piece3, piece2], 4],
                            [[piece2, piece1, piece3], 4], [[piece2, piece3, piece1], 4],
                            [[piece3, piece1, piece2], 4], [[piece3, piece2, piece1], 4]]
            elif dice1 == 6:
                piece1 = self.pullPiece()
                piece2 = self.pullPiece()
                piece3 = self.pullPiece()
                
                if dice2 != 1 and dice2 < 5:
                    return [[[piece1, piece2, piece3], dice2 - 1], [[piece1, piece3, piece2], dice2 - 1],
                            [[piece2, piece1, piece3], dice2 - 1], [[piece2, piece3, piece1], dice2 - 1],
                            [[piece3, piece1, piece2], dice2 - 1], [[piece3, piece2, piece1], dice2 - 1],
                            [[piece1, piece2, piece3], dice2], [[piece1, piece3, piece2], dice2],
                            [[piece2, piece1, piece3], dice2], [[piece2, piece3, piece1], dice2],
                            [[piece3, piece1, piece2], dice2], [[piece3, piece2, piece1], dice2]]
                elif dice2 == 1:
                    return [[[piece1, piece2, piece3], 1], [[piece1, piece3, piece2], 1],
                            [[piece2, piece1, piece3], 1], [[piece2, piece3, piece1], 1],
                            [[piece3, piece1, piece2], 1], [[piece3, piece2, piece1], 1]]
                else:
                    return [[[piece1, piece2, piece3], 4], [[piece1, piece3, piece2], 4],
                            [[piece2, piece1, piece3], 4], [[piece2, piece3, piece1], 4],
                            [[piece3, piece1, piece2], 4], [[piece3, piece2, piece1], 4]]

    def possible_moves_3(self):
        moves = []
        jasper_x = self.getJasperPosition()[1]
        for spell in range(0, 3): #1.flower 2.fire 3.do nothing
            for column in range(max(0, jasper_x - 3), min(jasper_x + 3, 5)):
                moves.append([spell, column])
        return moves

    def possible_moves_4(self):
        pump = []
        for row in range(8, 10):
            for column in range(0, 6):
                if self.board[row][column] == 1 or self.board[row][column] == 2:
                    adjacent = self.find_adjacent(row, column)
                    for item in adjacent:
                        if item[2] == 6:
                            pump.append(item)
        if len(pump) == 0:
            pump.append( (None,) )
        return pump

    def possible_actions(self, state):
        """Returns list of all possible actions one could take in any phase.
        """
        phase1 = GameState(phase=1)
        phase2 = GameState(phase=2)
        phase3 = GameState(phase=3)
        phase4 = GameState(phase=4)

        phase2Acts = phase2.legal_actions()
        phase3Acts = phase3.legal_actions()
        phase4Acts = phase4.legal_actions()

        return phase2Acts + phase3Acts + phase4Acts


    def legal_actions(self):
        """Returns list of legal actions that agent can take in current state.
        """
        if self.phase == 2:
            self.diceRoll()
            return self.possible_moves_2(self.dice1, self.dice2)
        elif self.phase == 3:
            return self.possible_moves_3()
        elif self.phase == 4:
            return self.possible_moves_4()
        else:
            return []

    def random_policy(self):
        actions = self.legal_actions()
        return random.choice(actions)

    def human_player(self):
        if self.phase == 2:
            moves = self.possible_moves_2(self.dice1, self.dice2)
        elif self.phase == 3:
            moves = self.possible_moves_3()
        elif self.phase == 4:
            moves = self.possible_moves_4()
        print("Your available moves are: ")
        print(moves)
        response = input("Enter the move you'd like to make: ")
        my_move = ast.literal_eval(response)
        while my_move not in moves:
            my_move = ast.literal_eval(input("Please enter a valid move: "))
        return my_move


    def play(self, strategy):
        """the functon that runs the process of playing the game."""
        statesVisited = [] # Sequence of states visited during a game
        actionsTaken = [] # Sequential actions taken during a game
        rewardsGained = [] # Sequence of rewards obtained during a game
        legalActions = []
        print("The game has started")
        print(self.board)

        while not self.isWinState() and not self.isLoseState():
            if self.phase == 1:
                self.descend() # phase 1
            elif self.phase == 2:
                self.diceRoll() # roll dice for phase 2
                mymove2 = strategy() #select move in possible moves
                hashableMove = tuple(map(lambda x : tuple(x) if type(x) is list else x, mymove2))
                self.getMatrixRow(hashableMove)
                legalActions.append(hashableMove)
                self.phase_two(self.dice1, mymove2)
                actionsTaken.append(mymove2)
            elif self.phase == 3:
                mymove3 = strategy() #select move for phase 3
                hashableMove = tuple(map(lambda x : tuple(x) if type(x) is list else x, mymove3))
                self.getMatrixRow(hashableMove)
                legalActions.append(hashableMove)
                prevScore = self.score
                self.move_and_shoot(mymove3) #execute phase 3
                actionsTaken.append(mymove3)
                rewardsGained.append(self.score - prevScore)
            elif self.phase == 4:
                mymove4 = strategy()
                hashableMove = tuple(map(lambda x : tuple(x) if type(x) is list else x, mymove4))
                self.getMatrixRow(hashableMove)
                legalActions.append(hashableMove)
                prevScore = self.score
                self.phase_four(mymove4)
                actionsTaken.append(mymove4)
                rewardsGained.append(self.score - prevScore)
            print("Current phase:", self.phase)
            print("The current state is:")
            print(self.board)
            statesVisited.append(deepcopy(self))
            self.phase = (self.phase % 4) + 1

        return (statesVisited, actionsTaken, rewardsGained, self.isWinState(), legalActions)

    ##########################
    # Helper methods for tpm #
    ##########################

    def __eq__(self, other):
        return np.array_equal(self.board, other.board) \
               and self.zombieCount == other.zombieCount \
               and self.fZombieCount == other.fZombieCount \
               and self.bombCount == other.bombCount \
               and self.multCount == other.multCount \
               and self.pumpCount == other.pumpCount \
               and self.wave == other.wave \
               and self.phase == other.phase \
               and self.score == other.score \
               and self.dice1 == other.dice1 \
               and self.dice2 == other.dice2 \


    # If getting not hashable error, try uncommenting below function
    def __hash__(self):
        return id(self)

# if __name__ == '__main__':
#     gs = GameState()
#     print(gs.play(gs.random_policy))

