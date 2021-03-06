from UtopiaEngine import *
import numpy as np
from itertools import permutations, combinations_with_replacement, combinations
from copy import deepcopy
import unittest
import random


def create_mini_game(row, column):
    """create empty board for minigames"""
    board = np.zeros((row, column))
    return board.astype(int)

# def create_mini_game(row, column):
# 	"""create empty board for minigames"""
# 	board = np.zeros([row, column])
# 	return board


def roll_dice(n):
    """roll n dices at once"""
    result = []
    for i in range(0, n):
        roll = random.randint(1, 6)
        result.append(roll)
    return result


def randomPolicy(actions):
    return random.choice(actions)


class Minigame:
    """An abstract class for the minigames of Utopia Engine"""
    def __init__(self, row, column):
        """initial state for minigame"""
        self.board = create_mini_game(row, column)
        self.tpm = {}

    def roll_dice_get_number(self, n):
        """get number for each step"""
        return roll_dice(n)

    def check_full(self):
        """check if the minigame board is full"""
        numrows = self.board.shape[0]
        numcols = self.board.shape[1]
        for row in range(numrows):
            for col in range(numcols):
                if self.board[(row, col)] == 0:
                    return False
        return True
        # return np.count_nonzero(self.board) == self.board.size

    def play(self, policy):
        raise NotImplementedError

    def check_final_range(self):
        if self.check_full():
            return 0

    def put_number(self, num, row, column):
        assert row < self.board.shape[0] and column < self.board.shape[1]
        self.board[row][column] = num

    def transition_prob_matrix(self):
        return self.tpm

    def transition_prob_vector(self, action, nrows, ncols):
        """ Method for finding transition probabilities of all next states
        given current state (self) and an action.
        """
        vector = []
        states = self.next_states(action, nrows, ncols)
        for next_state in states:
            vector.append( self.transition_prob(action, next_state) )
        return vector

    def transition_prob(self, action, next_state):
        """ Returns probability of transitioning from current state to
        next_state by taking action.
        """
        if (self, action, next_state) in self.tpm:
            return self.tpm[(self, action, next_state)]
        states = self.next_states(action)
        if next_state in states:
            self.tpm[(self, action, next_state)] = 1.0/np.long(len(states))
            return 1.0 / np.long(len(states))
        return 0.0

    def next_states(self, action, numrows, numcols):
        """ Returns all possible next states given current state and an action.
        """
        states = []
        if action in self.legal_actions(numrows, numcols):
            for roll1 in range(1, 7):
                for roll2 in range(1, 7):
                    states.append( self.simulate_action(action, roll1, roll2) )
        return states

    def simulate_action(self, action, roll1, roll2):
        """Takes in a legal action and returns a copy of the state after taking that action.
           Does not change current state.
        """
        next_state = deepcopy(self)
        next_state.board[action[0]] = roll1
        next_state.board[action[1]] = roll2
        return next_state

    def legal_actions(self, numrows, numcols):
        """Returns list of ways a pair of numbers can be placed on the board.
            If no empty spaces, moves represented as tuple of form:
                ((row, column) where 1st number goes, (row, column) where 2nd number goes)
        """
        emptySpaces = []
        for row in range(numrows):
            for col in range(numcols):
                if self.board[(row, col)] == 0:
                    emptySpaces.append( (row, col) )

        # List of all pairs of spaces with repeats
        # e.g. permutations([1, 2, 3], 2) returns [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]
        actions = tuple(permutations(emptySpaces, 2))
        #print("Actions: ", actions)
        return actions

    # def __hash__(self):
    # 	return

    # def __eq__(self, other):
    # 	return


class Activation(Minigame):
    tpm = {}

    def __init__(self):
        """create a 2*4 board"""
        Minigame.__init__(self, 2, 4)

    # def roll_dice_get_number(self):
    # 	Minigame.roll_dice_get_number(2)

    def check_final_range(self):
        energy_point = 0
        damage_take = 0
        if self.check_full():
            for i in range(0, 4):
                diff = self.board[0][i] - self.board[1][i]
                if diff == 5:
                    energy_point += 2
                elif diff == 4:
                    energy_point += 1
                elif diff < 1:
                    damage_take += 1
        return energy_point, damage_take

    def next_states(self, action):
        return Minigame.next_states(self, action, 2, 4)

    def legal_actions(self):
        return Minigame.legal_actions(self, 2, 4)

    def check_reroll(self):
        """Helper function for play. Checks if reroll necessary. If yes, resets boxes to 0,
           otherwise does nothing.
        """
        for i in range(0, 4):
            if self.board[0][i] - self.board[1][i] == 0:
                self.board[0][i] = 0
                self.board[1][i] = 0

    def play(self, strategy, energy_point):
        statesVisited = [deepcopy(self)] # Sequence of states visited during a game
        actionsTaken = [] # Sequential actions taken during a game
        rewardsGained = [] # Sequence of rewards obtained during a game
        legalActions = []
        print("Activation started:")

        while not self.check_full() or len(self.legal_actions()) < 2:
            numbers = self.roll_dice_get_number(2)
            print("These are numbers you can put in the board:")
            print(numbers)
            moves = strategy(self.legal_actions())
            # print("actions chosen:")
            # print(moves)
            actionsTaken.append(moves)
            self.put_number(numbers[0], moves[0][0], moves[0][1])
            self.put_number(numbers[1], moves[1][0], moves[1][1])
            statesVisited.append(deepcopy(self))
            self.check_reroll()
            print("This is the current state of the board:")
            print(self.board)
            for i in range(0, 4):
                if self.board[0][i] - self.board[1][i] == 0 and self.board[0][i] != 0:
                    self.put_number(0, 0, i)
                    self.put_number(0, 1, i)
                    print("difference = 0: reset")
                    continue
                    # numbers = self.roll_dice_get_number(2)
                    # print("These are numbers you can put in the board:")
                    # print(numbers)
                    # moves = strategy(self.legalActions(2, 4), True)
                    # print("actions chosen:")
                    # print(moves)
                    # self.put_number(numbers[0], moves[0][0], moves[0][1])
        damage_taken = self.check_final_range()[1]
        energy_point = energy_point + self.check_final_range()[0]
        if energy_point % 100 >= 4:
            return [999, damage_taken], [statesVisited, actionsTaken, rewardsGained, legalActions]
        else:
            return [energy_point, damage_taken], [statesVisited, actionsTaken, rewardsGained, legalActions]

class Connection(Minigame): 
    """A class that simulates the Connection part of the game
        The UtopiaEngine class should check that there are
        sufficient components available before creating an instance
        of this class."""

    tpm = {}

    def __init__(self, gamestate):
        Minigame.__init__(self, 2, 3)
        self.roll = []
        self.gamestate = gamestate  # the bigger board

    def next_states(self, action):
        return Minigame.next_states(self, action, 2, 3)

    def legal_actions(self):
        actions = Minigame.legal_actions(self, 2, 3)
        actions.append('keep')
        if len(self.gamestate.wastebasket) < 10:
            actions.append('toss')
        return actions

    def states(self):
        """Returns each state as a set of 3 2x1 arrays."""
        subset = []
        for i in range(1, 7):
            for j in range(1, 7):
                subset.append(np.array([[i], [j]]))
        allstates = list(combinations_with_replacement(subset, 3))
        return allstates

    def possible_actions(self):
        positions = []
        for i in range(3):
            for j in range(3):
                positions.append((i, j))
        unique_moves = []
        for n in range(1, 7):
            for position in positions:
                unique_moves.append(n, position)
        return list(combinations(unique_moves, 2))

    def state2board(self, state):
        return np.hstack((state[0], state[1], state[2]))

    def board2state(self, board):
        return np.hsplit(board, 3)

    def roll_dice_get_number(self):
        self.roll = Minigame.roll_dice_get_number(self, 2)
        return self.roll

    def toss(self, num):
        if (len(self.gamestate.wastebasket) < 10):
            self.gamestate.wastebasket.append(num)
            self.roll.remove(num)
            new_num = Minigame.roll_dice_get_number(1)
            self.roll.append(new_num)
        return self.roll

    def play(self, strategy):
        statesVisited = [] # Sequence of states visited during a game
        actionsTaken = [] # Sequential actions taken during a game
        rewardsGained = [] # Sequence of rewards obtained during a game
        legalActions = []

        while not self.check_full():
            statesVisited.append(deepcopy(self))
            result = self.roll_dice_get_number()
            for number in result:
                decision = strategy(['keep', 'toss'])
                actionsTaken.append(decision)
                if decision is 'toss':
                    statesVisited.append(deepcopy(self))
                    self.toss(number)
            moves = strategy(self.legal_actions(2, 3))
            actionsTaken.append(moves)
            for move in moves:
                num = strategy(result)
                result.remove(num) #prevents the number from being used again
                row = move[0]
                col = move[1]

        state = self.board2state(self.board)
        link = 0
        for pair in state:
            diff = np.subtract(pair[0], pair[1])[0]
            if diff < 0:
                self.gamestate.hit -= 1
                decision = strategy(['continue', 'stop']) #determines whether to spend another component
                actionsTaken.append(decision)
                if decision == 'continue':
                    link += 2
                else:
                    return -1
                statesVisited.append(deepcopy(self))
            else:
                link += diff
        return link, [statesVisited, actionsTaken, rewardsGained, legalActions]

class Search(Minigame):
    """Class for search minigame.
    """

    def __init__(self):
        Minigame.__init__(self, 2, 3)
        self.tpm = {}

    def play(self, policy):
        """Play through one search round. Returns final difference after filling in board, along
            with list of form [statesVisited, actionsTaken, rewardsGained, legalActions].
            Arguments:
                policy: a function that takes in the current state and returns a legal action
        """
        statesVisited = [] # Sequence of states visited during a game
        actionsTaken = [] # Sequential actions taken during a game
        rewardsGained = [] # Sequence of rewards obtained during a game
        legalActions = []
        while not self.check_full():
            print("Current board: ")
            print(self.board)
            statesVisited.append(deepcopy(self))
            roll1, roll2 = self.roll_dice_get_number(2)
            print("You rolled: ")
            print([roll1, roll2])
            action = policy(self.legal_actions())
            actionsTaken.append(action)
            self = self.simulate_action(action, roll1, roll2)

        print("Current board: ")
        print(self.board)
        val1 = self.board[0][0]*100 + self.board[0][1]*10 + self.board[0][2]
        val2 = self.board[1][0]*100 + self.board[1][1]*10 + self.board[1][2]
        print("Your search result: ", val1-val2)
        return val1 - val2, [statesVisited, actionsTaken, rewardsGained, legalActions]

    def next_states(self, action, rows=2, cols=3):
        """Returns list of next possible states given current state and action.
        """
        return Minigame.next_states(self, action, 2, 3)

    def legal_actions(self, rows=2, cols=3):
        return Minigame.legal_actions(self, 2, 3)

class FinalActivation:

    def __init__(self, finalActivationDifficulty, hitpoints):
        self.actNum = finalActivationDifficulty
        self.rolls = hitpoints + 1
        self.activated = False
        self.hitpoints = hitpoints
        self.tpm = {}

    def play(self, policy):
        statesVisited = [deepcopy(self)] # Sequence of states visited during a game
        actionsTaken = [] # Sequential actions taken during a game
        rewardsGained = [] # Sequence of rewards obtained during a game
        legalActions = []
        playerSum = np.sum(roll_dice(2))
        actionsTaken.append('roll')
        if playerSum >= self.actNum:
            self.activated = True
            statesVisited.append(deepcopy(self))
            return True, [statesVisited, actionsTaken, rewardsGained, legalActions]
        else:
            self.hitpoints -= 1
            statesVisited.append(deepcopy(self))
            return False, [statesVisited, actionsTaken, rewardsGained, legalActions]

    def next_states(self, action):
        states = [deepcopy(self)]
        if not self.activated:
            activated_state = deepcopy(self)
            activated_state.activated = True
            states.append(activated_state)
        return states

    def legal_actions(self):
        return 'roll'

    def transition_prob_matrix(self):
        return self.tpm

    def transition_prob_vector(self, action):
        """ Method for finding transition probabilities of all next states
        given current state (self) and an action.
        """
        vector = []
        states = self.next_states(action)
        for next_state in states:
            vector.append( self.transition_prob(action, next_state) )
        return vector

    def transition_prob(self, action, next_state):
        """ Returns pobability of transitioning from current state to
        next_state by taking action.
        """
        if (self, action, next_state) in self.tpm:
            return self.tpm[(self, action, next_state)]
        prob_succeed_first_roll = self.dice_prob_distr(self.actNum)
        prob_fail = 1 - prob_succeed_first_roll
        prob_succeed = 1 - prob_fail**self.rolls
        self.tpm[(self, action, next_state)] = prob_succeed
        return prob_succeed

    def dice_prob_distr(self, target_roll):
        """Helper function for transition_prob. Returns probability of rolling two dice
           and getting a result greater than or equal to target_roll.
        """
        dice_prob_table = {2: 1.0/36.0,
                           3: 2.0/36.0,
                           4: 3.0/36.0,
                           5: 4.0/36.0,
                           6: 5.0/36.0,
                           7: 6.0/36.0,
                           8: 5.0/36.0,
                           9: 4.0/36.0,
                           10: 3.0/36.0,
                           11: 2.0/36.0,
                           12: 1.0/36.0}

        query_prob = 0.0
        while target_roll < 13:
            query_prob += dice_prob_table[target_roll]
            target_roll += 1
        return query_prob


class TestMethods(unittest.TestCase):

    def test_activation(self):
        for i in range(0, 100):
            activation = Activation()
            result = activation.play(randomPolicy, 0)
            self.assertTrue(0 <= result[0][0] <= 999 or result[0][0] in range(0, 5))

    def test_connection(self):
        for i in range(0, 100):
            gameboard = GameBoard()
            connection = Connection(gameboard)
            result = connection.play(randomPolicy)
            self.assertTrue(result < 7)
    
    def test_search(self):
        for i in range(0, 100):
            search = Search()
            result = search.play(randomPolicy)

    def test_check_full(self):
        test = Minigame(2, 4)
        test.put_number(1, 0, 0)
        test.put_number(1, 0, 1)
        test.put_number(1, 0, 2)
        test.put_number(1, 0, 3)
        test.put_number(1, 1, 0)
        test.put_number(1, 1, 1)
        test.put_number(1, 1, 2)
        test.put_number(1, 1, 3)
        self.assertTrue(test.check_full())
        test.put_number(0, 0, 0)
        test.put_number(0, 1, 0)
        self.assertTrue(not test.check_full())
        test.put_number(1, 0, 0)
        test.put_number(1, 1, 0)
        self.assertTrue(test.check_full())


if __name__ == '__main__':
    unittest.main()

