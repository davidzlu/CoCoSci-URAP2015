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

    def __init__(self, board=create_board(), zombieCount=24, fZombieCount=8, bombCount=4, multCount=3, pumpCount=6, wave=1, phase=2, score=0):
        self.board = board
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

    def random_policy(self):
        actions = self.possible_actions()
        return random.choice(actions)

    def play(self, strategy):
        """the functon that runs the process of playing the game."""
        statesVisited = [] # Sequence of states visited during a game
        actionsTaken = [] # Sequential actions taken during a game
        rewardsGained = [] # Sequence of rewards obtained during a game
        while not self.checkWin() and not self.checkLose():
            if self.phase == 1:
                self.descend() # phase 1
            elif self.phase == 2:
                self.diceRoll() # roll dice for phase 2
                moves2 = self.possible_moves_2(self.dice1, self.dice2) #create possible moves
                mymove2 = strategy() #select move in possible moves
                self.phase_two(self.dice1, mymove2)
                actionsTaken.append(mymove2)
            elif self.phase == 3:
                moves3 = self.possible_moves_3() # generate possible moves for phase3
                mymove3 = strategy() #select move for phase 3
                prevScore = self.score
                self.move_and_shoot(mymove3) #execute phase 3
                actionsTaken.append(mymove3)
                rewardsGained.append(self.score - prevScore)
            elif self.phase == 4:
                moves4 = self.possible_moves_4()
                mymove4 = strategy()
                prevScore = self.score
                self.phase_four(mymove4)
                actionsTaken.append(mymove4)
                rewardsGained.append(self.score - prevScore)
            print("The current state is:")
            print(self.board)
            statesVisited.append(self.copy())
            self.phase = (self.phase % 4) + 1
        return (statesVisited, actionsTaken, rewardsGained)

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
            if nextState.checkWin():
                #add reward for destroying tokens?
                self.score += 100 # Reward for winning game
                return 100
        return 0 # No reward for losing

    def copy(self):
        """Returns a new state with same instance variables as self.
        """
        return GameState(self.board, self.zombieCount, self.fZombieCount, self.bombCount, self.multCount, self.pumpCount, self.wave, self.phase)
        
    def transition_prob_matrix(self, curState, action, nextState):
        """Returns transition probability given (s, a, s') if it exists in
        transition_prob_matrix. Otherwise calculates the probability, enters it
        into transition_prob_matrix and returns the probability.
        """
        if (curState, action, nextState) in GameState.tpm:
            return GameState.tpm[(curState, action, nextState)]
        else:
            prob = self.transition_prob(curState, action, nextState)
            GameState.tpm[(curState, action, nextState)] = prob
            return prob

    def next_states(self, action):
        states = []
        next_state = deepcopy(self)
        if self.phase == 1: #states after descend
            states.append(next_state.descend())
        elif self.phase == 0 or self.phase == 2: #states after rolling and placing
            for i in range(1, 7):
                for j in range(1, 7): #all possible combinations of dicerolls
                    next_state = deepcopy(self)
                    states.append(next_state.phase_two(i, j, action))
        elif self.phase == 3: #states after moving and spellcasting
            states.append(next_state.move_and_shoot(action))
        elif self.phase == 4: #states after smash
           states.append(next_state.phase_four(action))
        return states

    def transition_prob(self, action, nextState): #are self and curState not the same thing?? -Priyam
        """Returns probability of transitioning from curState to nextState given action.
        """
        nextPossible = self.next_states(action)
        if nextState in nextPossible:
            return 1.0/len(nextPossible)
        return 0.0

    def getMatrixRow(self, action):
        """Returns row of transition probability matrix, specified by curState and action.
        """
        matrixRow = []
        nextPossible = self.next_states(action)
        for nextState in nextPossible:
          index = (curState, action, nextState)
          if index not in GameState.tmp:
               GameState.tmp[index] = self.transition_prob(action, nextState)
               matrixRow.append(GameState.tmp[index])
        return matrixRow


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
        totalLeft = self.piecesLeft()
        if totalLeft == 0:
            return self.waveTransition()
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
        """Manages transitioning between wave 1 and 2.
        """
        if self.wave == 1 and self.piecesLeft() == 0 or self.wave == 1 and self.piecesLeft() > 0 and self.pumpCount < 6:
            zCount, fzCount, bCount, mCount, pCount = self.count_pieces()
            self.zombieCount = 24-zCount
            self.fZombieCount = 8-fzCount
            self.bombCount = 4-bCount
            self.multCount = 4-mCount
            self.pumpCount = 6-pCount
            self.wave = 2
            return self.pullPiece()
        return 0

    def checkWin(self):
        """Checks if current state is a win state.
        """
        def enemyOnBoard(self):
            zCount, fZCount, bCount, mCount, pCount = self.count_pieces()
            return zCount > 0 or fZCount > 0 or bCount > 0 or mCount > 0
        return self.wave == 2 and self.pumpCount > 0 and self.piecesLeft == 0 and self.enemyOnBoard()

    def checkLose(self):
        return self.pumpCount == 0 and self.wave == 2

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
            elif token_one_ahead == 0: #move forward one space
                self.board[new_row1, col] = token[2]
                self.board[old_pos] = 0
                token = (token[0] + 1, token[1], token[2])
            else:
                pass
        elif (new_row1 < 10): #token reaches magical barrier
            if token[2] == 4 or token[2] == 11:
                token = (new_row1, col, token[2])
                self.board[old_pos] = 0
                self.explode(token)
            elif token[2] == 5 or token[2] == 12: #multiplier disappears
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
                if self.board[9, one_left] == 3:
                    if token[2] == 2:
                        self.burn((token[0], one_left, 2))
                        self.move(token)
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
                if self.board[9, one_right] == 3:
                    if token[2] == 2:
                        self.burn((token[0], one_right, 2))
                        self.move(token)
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
        else:
            raise Exception('Whoops, something went wrong.')

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
        self.phase = 2


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
        #I think the code below belongs in a play function instead of in a phase function. - Priyam
        # print("Your available moves are:")
        # print(move_3)
        # my_move_3 = ast.literal_eval(input("Enter the move you'd like to make: "))
        # while my_move not in moves:
        #     my_move_3 = ast.literal_eval(input("Please enter a valid move: "))
        if my_move_3[0] == 0:#flower power
            for index in range(0, 4):
                row = 9 - index
                token_type = self.board[row][my_move_3[1]]
                if token_type == 1 or token_type == 2 or token_type == 4 or token_type == 5 or token_type == 8 or token_type == 11 or token_type == 12:
                    token = (row, my_move_3[1], token_type)
                    self.flower(token)
                    break
        elif my_move_3[0] == 1: #magic fire
            for index in range(0, 4):
                row = 9 - index
                token_type = self.board[row][my_move_3[1]]
                if token_type == 3 or token_type == 8 or token_type == 11 or token_type == 12:
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
                        if pump[0] is "nothing":
                            break
                        else:
                            self.board[pump[0][0]][pump[0][1]] = 0
                            self.score = self.score - 10
                    elif len(pump) == 2:
                        self.board[pump_chosen[0]][pump_chosen[1]] = 0
                        self.score = self.score - 10


    def smash(self):
        for row in range(8, 10):
            for column in range(0, 6):
                if self.board[row][column] == 1 or self.board[row][column] == 2:
                    adjacent = self.find_adjacent(row, column)
                    pump = []
                    for item in adjacent:
                        if item[2] == 6:
                            pump.append(item)
                    if len(pump) == 1:
                        self.board[pump[0][0]][pump[0][1]] = 0
                        self.score = self.score - 10
                    elif len(pump) == 2:
                        print("Your choices of pumpkin are:")
                        print(pump)
                        pump_chosen = ast.literal_eval(input("Enter the pumpkin to smash: "))
                        while pump_chosen not in pump:
                            pump_chosen = ast.literal_eval(input("Please enter an available pumpkin: "))
                        self.board[pump_chosen[0]][pump_chosen[1]] = 0
                        self.score = self.score - 10
                    #Code below may be unnecessary as it should be handled in descend function. Tokens don't move during smash anyway
                    # elif len(pump) == 0:
                    #     if row == 9:
                    #         if column == 0 or column == 1:
                    #             if self.board[row][column + 1] == 0:
                    #                 self.board[row][column + 1] = self.board[row][column]
                    #                 self.board[row][column] = 0
                    #         elif column == 5 or column == 4:
                    #             if self.board[row][column - 1] == 0:
                    #                 self.board[row][column - 1] = self.board[row][column]
                    #                 self.board[row][column] = 0
                    #         else:
                    #             token = (row, column, self.board[row][column])
                    #             direction = self.nearest_pumpkin(token)
                    #             if direction == 'left' and self.board[row][column - 1] == 0:
                    #                 self.board[row][column - 1] = self.board[row][column]
                    #                 self.board[row][column] = 0
                    #             elif direction == 'right' and self.board[row][column + 1] == 0:
                    #                 self.board[row][column + 1] = self.board[row][column]
                    #                 self.board[row][column] = 0


    def possible_moves_2(self, dice1, dice2):
        """takes in state and two dices, return all possible moves"""
        if self.wave == 1:
            if dice1 == 1:
                return [[self.pullPiece()], dice2 - 1]
            elif dice1 == 2:
                piece1 = self.pullPiece()
                piece2 = self.pullPiece()

                if dice2 != 1 and dice2 != 6:
                    return [[[piece1, piece2], dice2 - 1], [[piece2, piece1], dice2 - 1], [[piece1, piece2], dice2], [[piece2, piece1], dice2]]
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
                    return [[[piece1, piece2, piece3], dice2 - 1], [[piece1, piece3, piece2], dice2 - 1], [[piece2, piece1, piece3], dice2 - 1], [[piece2, piece3, piece1], dice2 - 1], [[piece3, piece1, piece2], dice2 - 1], [[piece3, piece2, piece1], dice2 - 1], [[piece1, piece2, piece3], dice2], [[piece1, piece3, piece2], dice2], [[piece2, piece1, piece3], dice2], [[piece2, piece3, piece1], dice2], [[piece3, piece1, piece2], dice2], [[piece3, piece2, piece1], dice2]]
                elif dice2 == 1:
                    return [[[piece1, piece2, piece3], 1], [[piece1, piece3, piece2], 1], [[piece2, piece1, piece3], 1], [[piece2, piece3, piece1], 1], [[piece3, piece1, piece2], 1], [[piece3, piece2, piece1], 1]]
                else:
                    return [[[piece1, piece2, piece3], 5], [[piece1, piece3, piece2], 5], [[piece2, piece1, piece3], 5], [[piece2, piece3, piece1], 5], [[piece3, piece1, piece2], 5], [[piece3, piece2, piece1], 5]]
            elif dice1 == 5:
                piece1 = self.pullPiece()
                piece2 = self.pullPiece()
                piece3 = self.pullPiece()
                if dice2 != 1 and dice2 != 6:
                    return [[[piece1, piece2, piece3], dice2 - 1], [[piece1, piece3, piece2], dice2 - 1], [[piece2, piece1, piece3], dice2 - 1], [[piece2, piece3, piece1], dice2 - 1], [[piece3, piece1, piece2], dice2 - 1], [[piece3, piece2, piece1], dice2 - 1], [[piece1, piece2, piece3], dice2], [[piece1, piece3, piece2], dice2], [[piece2, piece1, piece3], dice2], [[piece2, piece3, piece1], dice2], [[piece3, piece1, piece2], dice2], [[piece3, piece2, piece1], dice2]]
                elif dice2 == 1:
                    return [[[piece1, piece2, piece3], 1], [[piece1, piece3, piece2], 1], [[piece2, piece1, piece3], 1], [[piece2, piece3, piece1], 1], [[piece3, piece1, piece2], 1], [[piece3, piece2, piece1], 1]]
                else:
                    return [[[piece1, piece2, piece3], 5], [[piece1, piece3, piece2], 5], [[piece2, piece1, piece3], 5], [[piece2, piece3, piece1], 5], [[piece3, piece1, piece2], 5], [[piece3, piece2, piece1], 5]]
            elif dice1 == 6:
                piece1 = self.pullPiece()
                piece2 = self.pullPiece()
                piece3 = self.pullPiece()
                if dice2 != 1 and dice2 != 6:
                    return [[[piece1, piece2, piece3], dice2 - 1], [[piece1, piece3, piece2], dice2 - 1], [[piece2, piece1, piece3], dice2 - 1], [[piece2, piece3, piece1], dice2 - 1], [[piece3, piece1, piece2], dice2 - 1], [[piece3, piece2, piece1], dice2 - 1], [[piece1, piece2, piece3], dice2], [[piece1, piece3, piece2], dice2], [[piece2, piece1, piece3], dice2], [[piece2, piece3, piece1], dice2], [[piece3, piece1, piece2], dice2], [[piece3, piece2, piece1], dice2]]
                elif dice2 == 1:
                    return [[[piece1, piece2, piece3], 1], [[piece1, piece3, piece2], 1], [[piece2, piece1, piece3], 1], [[piece2, piece3, piece1], 1], [[piece3, piece1, piece2], 1], [[piece3, piece2, piece1], 1]]
                else:
                    return [[[piece1, piece2, piece3], 5], [[piece1, piece3, piece2], 5], [[piece2, piece1, piece3], 5], [[piece2, piece3, piece1], 5], [[piece3, piece1, piece2], 5], [[piece3, piece2, piece1], 5]]
        elif self.wave == 2:
            if dice1 == 1:
                piece1 = self.pullPiece()
                piece2 = self.pullPiece()
                if dice2 != 1 and dice2 != 6:
                    return [[[piece1, piece2], dice2 - 1], [[piece2, piece1], dice2 - 1], [[piece1, piece2], dice2], [[piece2, piece1], dice2]]
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
                    return [[[piece1, piece2], 5], [[piece2, piece1], 5]]
            elif dice1 == 3:
                piece1 = self.pullPiece()
                piece2 = self.pullPiece()
                if dice2 != 1 and dice2 != 6:
                    return [[[piece1, piece2], dice2 - 1], [[piece2, piece1], dice2 - 1], [[piece1, piece2], dice2], [[piece2, piece1], dice2]]
                elif dice2 == 1:
                    return [[[piece1, piece2], 1], [[piece2, piece1], 1]]
                else:
                    return [[[piece1, piece2], 5], [[piece2, piece1], 5]]
            elif dice1 == 4:
                piece1 = self.pullPiece()
                piece2 = self.pullPiece()
                piece3 = self.pullPiece()
                if dice2 != 1 and dice2 != 6:
                    return [[[piece1, piece2, piece3], dice2 - 1], [[piece1, piece3, piece2], dice2 - 1], [[piece2, piece1, piece3], dice2 - 1], [[piece2, piece3, piece1], dice2 - 1], [[piece3, piece1, piece2], dice2 - 1], [[piece3, piece2, piece1], dice2 - 1], [[piece1, piece2, piece3], dice2], [[piece1, piece3, piece2], dice2], [[piece2, piece1, piece3], dice2], [[piece2, piece3, piece1], dice2], [[piece3, piece1, piece2], dice2], [[piece3, piece2, piece1], dice2]]
                elif dice2 == 1:
                    return [[[piece1, piece2, piece3], 1], [[piece1, piece3, piece2], 1], [[piece2, piece1, piece3], 1], [[piece2, piece3, piece1], 1], [[piece3, piece1, piece2], 1], [[piece3, piece2, piece1], 1]]
                else:
                    return [[[piece1, piece2, piece3], 5], [[piece1, piece3, piece2], 5], [[piece2, piece1, piece3], 5], [[piece2, piece3, piece1], 5], [[piece3, piece1, piece2], 5], [[piece3, piece2, piece1], 5]]
            elif dice1 == 5:
                piece1 = self.pullPiece()
                piece2 = self.pullPiece()
                piece3 = self.pullPiece()
                if dice2 != 1 and dice2 != 6:
                    return [[[piece1, piece2, piece3], dice2 - 1], [[piece1, piece3, piece2], dice2 - 1], [[piece2, piece1, piece3], dice2 - 1], [[piece2, piece3, piece1], dice2 - 1], [[piece3, piece1, piece2], dice2 - 1], [[piece3, piece2, piece1], dice2 - 1], [[piece1, piece2, piece3], dice2], [[piece1, piece3, piece2], dice2], [[piece2, piece1, piece3], dice2], [[piece2, piece3, piece1], dice2], [[piece3, piece1, piece2], dice2], [[piece3, piece2, piece1], dice2]]
                elif dice2 == 1:
                    return [[[piece1, piece2, piece3], 1], [[piece1, piece3, piece2], 1], [[piece2, piece1, piece3], 1], [[piece2, piece3, piece1], 1], [[piece3, piece1, piece2], 1], [[piece3, piece2, piece1], 1]]
                else:
                    return [[[piece1, piece2, piece3], 5], [[piece1, piece3, piece2], 5], [[piece2, piece1, piece3], 5], [[piece2, piece3, piece1], 5], [[piece3, piece1, piece2], 5], [[piece3, piece2, piece1], 5]]
            elif dice1 == 6:
                piece1 = self.pullPiece()
                piece2 = self.pullPiece()
                piece3 = self.pullPiece()
                if dice2 != 1 and dice2 != 6:
                    return [[[piece1, piece2, piece3], dice2 - 1], [[piece1, piece3, piece2], dice2 - 1], [[piece2, piece1, piece3], dice2 - 1], [[piece2, piece3, piece1], dice2 - 1], [[piece3, piece1, piece2], dice2 - 1], [[piece3, piece2, piece1], dice2 - 1], [[piece1, piece2, piece3], dice2], [[piece1, piece3, piece2], dice2], [[piece2, piece1, piece3], dice2], [[piece2, piece3, piece1], dice2], [[piece3, piece1, piece2], dice2], [[piece3, piece2, piece1], dice2]]
                elif dice2 == 1:
                    return [[[piece1, piece2, piece3], 1], [[piece1, piece3, piece2], 1], [[piece2, piece1, piece3], 1], [[piece2, piece3, piece1], 1], [[piece3, piece1, piece2], 1], [[piece3, piece2, piece1], 1]]
                else:
                    return [[[piece1, piece2, piece3], 5], [[piece1, piece3, piece2], 5], [[piece2, piece1, piece3], 5], [[piece2, piece3, piece1], 5], [[piece3, piece1, piece2], 5], [[piece3, piece2, piece1], 5]]

    def possible_moves_3(self):
        moves = []
        jasper_x = self.getJasperPosition()[1]
        for spell in range(0, 3): #1.flower 2.fire 3.do nothing
            for column in range(max(0, jasper_x - 3), min(jasper_x + 3, 5)):
                moves.append([spell, column])
        return moves

    def possible_moves_4(self):
        for row in range(8, 10):
            for column in range(0, 6):
                if self.board[row][column] == 1 or self.board[row][column] == 2:
                    adjacent = self.find_adjacent(row, column)
                    pump = []
                    for item in adjacent:
                        if item[2] == 6:
                            pump.append(item)
        if len(pump) == 0:
            pump.append("nothing")
        return pump

    def possible_actions(self):
        if self.phase == 2:
            return possible_moves_2(self, self.dice1, self.dice2)
        elif self.phase == 3:
            return possible_moves_3(self)
        elif self.phase == 4:
            return possible_moves_4(self)
        else:
            return []



    ########################################
    # Helper methods for transition matrix #
    ########################################

    def __eq__(self, other):
        return self.board == other.board \
               and self.zombieCount == other.zombieCount \
               and self.fZombieCount == other.fZombieCount \
               and self.bombCount == other.bombCount \
               and self.multCount == other.multCount \
               and self.pumpCount == other.pumpCount \
               and self.wave == other.wave \
               and self.phase == other.phase

    def __hash__(self):
        return hash((self.board, \
                     self.zombieCount, \
                     self.fZombieCount, \
                     self.bombCount, \
                     self.multCount, \
                     self.pumpCount, \
                     self.wave, \
                     self.phase))


