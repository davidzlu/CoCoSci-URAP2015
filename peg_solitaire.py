import numpy as np
import ast
from Game import Game
import random

#spaces which don't usually exist on a standard English Peg Solitaire board
illegal_spaces = [(0, 0), (1, 0), (5, 0), (6, 0), (0, 1), (1, 1), (5, 1), (6, 1), (0, 5), (0, 6), (1, 5), (1, 6), (5, 5), (5, 6), (6, 5), (6, 6)]


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
    board = np.zeros(49).astype(int)
    for i in range(len(state)):
        board[i] = state[i]
    return board.reshape((7,7))

lose_state = board2state(np.zeros((7,7)).astype(int))

def next_states(state):
    """ Returns the next immediately possible legal states given the current state."""
    states = []
    board = state2board(state)
    for i in range(len(board)):
        for j in range(len(board)):
            if board[(i, j)] == 0:
                if (i, j) not in illegal_spaces:
                    #start checking viable directions
                    if (i-2 >= 0) and (board[(i-2, j)] == 1) and (board[(i-1, j)] == 1): #up
                        states.append(board2state(take_action(board.copy(), i, j, 3)))
                    if (i+2 < 7) and (board[(i+2, j)] == 1) and (board[(i+1, j)] == 1): #down
                        states.append(board2state(take_action(board.copy(), i, j, 1)))
                    if (j-2 >=0) and (board[(i, j-2)] ==1) and (board[(i, j-1)] == 1): #left
                        states.append(board2state(take_action(board.copy(), i, j, 2))) 
                    if (j+2 < 7) and (board[(i, j+2)] == 1) and (board[(i, j+1)] == 1): #right
                        states.append(board2state(take_action(board.copy(), i, j, 4)))
    return states

def possible_actions(board):
    """
    Returns list of all possible actions that can be taken from the current game state.
    Includes illegal moves. """
    actions = []
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 0:
                actions.append((i, j, 1))
                actions.append((i, j, 2))
                actions.append((i, j, 3))
                actions.append((i, j, 4))
    return actions

def legal_actions(board):
    """
    Returns list of legal actions that can be taken in board.
    """
    def space_check(space):
        """
        Helper method for legal_actions. Returns list of legal actions
        that can be taken using space (i, j) as destination.
        """
        i = space[0]
        j = space[1]
        spaces = []
        if i-2 >= 0: # up
            if board[(i-2, j)] == 1 and board[(i-1, j)] == 1:
                spaces.append((i, j, 3))
        if j-2 >= 0: # left
            if board[(i, j-2)] == 1 and board[(i, j-1)] == 1:
                spaces.append((i, j, 2))
        if i+2 < 7: # down
            if board[(i+2, j)] == 1 and board[(i+1, j)] == 1:
                spaces.append((i, j, 1))
        if j+2 < 7: # right
            if board[(i, j+2)] == 1 and board[(i, j+1)] == 1:
                spaces.append((i, j, 4))
        return spaces

    legal_moves = []
    for i in range(len(board)):
        for j in range(len(board)):
            space = (i, j)
            if space not in illegal_spaces and board[space] == 0:
                legal_moves += space_check(space)
    return legal_moves

def state_transition(state, action):
    """ 
    Returns state agent would enter if takes action in state.
    If no legal actions in state, or if action is not legal,
    return lose state.
    """
    legal_moves = legal_actions(state2board(state))
    if legal_moves == [] or action not in legal_moves:
        return lose_state
    return board2state(take_action(state2board(state), action[0], action[1], action[2]))

def transition_prob(next_state, cur_state, action):
    """ Return probability of transitioning into next_state from
    cur_state and action."""
    moves = legal_actions(state2board(cur_state))
    if action in moves:
        if state_transition(cur_state, action) == next_state:
            return 1
    return 0

def transition_prob_matrix(board):
    """
    Creates a transition probability matrix for the board passed in 
    for which transition_prob_matrix[i, j, k] refers to 
    [current state, next state, action].

    """
    actions = possible_actions(board)
    cur_state = board2state(board)
    states = next_states(cur_state)
    array_list = []
    for move in actions:
        test_state = state_transition(cur_state, move)
        if test_state in states:
            array_list.append(transition_prob(test_state, cur_state, move))
        else:
            array_list.append(0)
    matrix = np.array(array_list[0])
    for array in array_list[1:]:
        matrix = np.dstack((matrix, np.array(array)))
    return matrix


def reward(cur_state, action, next_state):
    """
    Returns 1 if taking action in state is legal, state transitions
    to next_state using action, and next_state is a win state.
    Returns -100 if taking action in state is not legal, or state
    does not transition to next_state using action. Return 0 otherwise.
    """
    if action in legal_actions(state2board(cur_state)):
        if check_win(state2board(next_state)):
            return 1
    #     elif next_state != lose_state:
    #         return 0
    # return -100
        else:
            return 0
    return -1


#def opt_avf(cur_state, cur_action, d, e):
#    value = 0
#    while d >= e:
#        possible_states = next_states(cur_state)
#        for next_state in possible_states:
#            for action in possible_actions([[0,0],[0,0]]):
#                next_value = transition_prob(next_state, cur_state, action) * (reward(cur_state, action, next_state)
#                 + opt_avf(next_state, action, d, e))
#                value = max(value, next_value)
#                d = min(d, abs(value-next_value))
#                print(d)
#    return value

# seen = {}
# def opt_avf(cur_state, cur_action):
#     """
#   Calculates Q(cur_state, cur_action)
#     """
#     following_state = state_transition(cur_state, cur_action)
#    value = 0
#     for action in legal_actions(state2board(next_state)):
#        if (next_state, action) not in seen:
#             seen[(next_state, action)] = 0
#        else:
#            tProb = transition_prob(following_state, cur_state, action)
#            r = reward(following_state, cur_state, cur_action)
#             value = max(value, tProb * (r + seen[(next_state, action)]) )
#     seen[(next_state, action)] = value
#     seen[(cur_state, cur_action)] = value
#     return value

Q = {}
def opt_avf(cur_state, cur_action, d, e):
    # have to handle the case where next_states(state) = [] and exit the infinite loop
    following_state = state_transition(cur_state, cur_action)
    states = allstates(following_state)
    while d >= e:
        next_value = 0
        for next_state in states:
            for action in legal_actions(state2board(next_state)):
                if (next_state, action) in Q:
                    next_value = transition_prob(following_state, cur_state, action) * (reward(following_state, cur_state, cur_action) \
                    + Q[(next_state, action)])
                else:
                    Q[(next_state, action)] = 0
                Q[(next_state, action)] = max(next_value, Q[(next_state, action)])
                d = abs(Q[(next_state, action)] - next_value)
        Q[(cur_state, cur_action)] = next_value
    return Q[(cur_state, cur_action)]

def allstates(cur_state):
    """
    Helper method for opt_avf
    """
    states = next_states(cur_state)
    for state in states:
        states += next_states(state)
    return states




def create_board():
    """
    Initializes the standard English peg solitaire game board with 
    the center hole vacant.
    """
    board = np.ones((7,7))
    board[0:2, 0:2] = 0
    board[0:2, 5:] = 0
    board[5: , 0:2] = 0
    board[5: , 5: ] = 0
    board[3, 3] = 0
    return board.astype(int)

def take_action(board, endrow, endcolumn, direction):
    """Takes in the board and the target location, where direction is 
    the starting location of the peg relative to the target.
     1 = down 2 = left 3 = up 4 = right"""
    assert direction == 1 or direction == 2 or direction == 3 or direction == 4
    x = board[:][:]
    x[endrow][endcolumn] = 1
    if direction == 1:
        x[endrow + 1][endcolumn] = 0
        x[endrow + 2][endcolumn] = 0
    elif direction == 2:
        x[endrow][endcolumn - 1] = 0
        x[endrow][endcolumn - 2] = 0
    elif direction == 3:
        x[endrow - 1][endcolumn] = 0
        x[endrow - 2][endcolumn] = 0
    elif direction == 4:
        x[endrow][endcolumn + 1] = 0
        x[endrow][endcolumn + 2] = 0
    return x

def check_win(board):
    """
    Checks if the player has won or not by counting the number of pegs left.
    Returns True if the game has been won.
    """
    num_pegs = 0
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 1:
                num_pegs += 1
            if num_pegs > 1:
                return False
    if num_pegs == 1:
        return True

def human_player(board):
    """
    A strategy for use with play().
    When passed into play(), an interactive game of Peg Solitaire begins
    This function allows players to input moves into the terminal.
    """
    cur_state = board2state(board)
    moves = legal_actions(board)
    states = next_states(cur_state)
    print("Your available moves are: ")
    print(moves)
    response = input("Enter the move you'd like to make: ")
    my_move = ast.literal_eval(response)
    while my_move not in possible_actions(board):
        my_move = ast.literal_eval(input("Please enter a valid move: "))
    next_state = state_transition(cur_state, my_move)
    expected_reward = reward(cur_state, my_move, next_state)
    print("The result of that move is: ")
    print(state2board(next_state))
    print("Your expected reward for that move is: ")
    print(expected_reward)
    response2 = input("Would you like to change your move? y/n: ")
    if (response2 == 'n') | (response2 == 'no'):
        return my_move
    else:
        return human_player(board)


# def play(strategy=human_player):
# 	"""
# 	The main function for running a game of PegSolitaire. Default is set to
# 	human_player phase but this function also accepts any algorithm which returns a move.
# 	"""
# 	statesVisited = [] # Sequence of states visited during a game
# 	actionsTaken = [] # Sequential actions taken during a game
# 	rewardsGained = [] # Sequence of rewards obtained during a game
# 	ps = PegSolitaire()
# 	board = ps.board
# 	# print("The game has begun. The current board state is ")
# 	# print(board)
# 	while not check_win(board):
# 		cur_state = board2state(board)
# 		statesVisited.append(cur_state)
# 		moves = legal_actions(board)
# 		move = strategy(ps.board)
# 		actionsTaken.append(move)
# 		if move not in moves:
# 			break
# 		row, column, direction = move[0], move[1], move[2]
# 		ps.board = take_action(ps.board, row, column, direction)
# 		reward = 0
# 		rewardsGained.append(reward)
# 		# print("The turn has ended. The current board state is ")
# 		# print(board)
# 	if check_win(board):
# 		# print('The player has won the game!')
# 		reward = 1
# 	else:
# 		# print('An illegal move was made. The player has lost the game.')
# 		reward = -1
# 	rewardsGained.append(reward)
# 	return (statesVisited, actionsTaken, rewardsGained, check_win(ps.board))

def play(strategy=human_player):
    """
    The main function for running a game of PegSolitaire. Default is set to
    human_player phase but this function also accepts any algorithm which returns a move.
    """
    statesVisited = [] # Sequence of states visited during a game
    actionsTaken = [] # Sequential actions taken during a game
    rewardsGained = [] # Sequence of rewards obtained during a game
    legalActions = []
    ps = PegSolitaire()
    board = ps.board
    # print("The game has begun. The current board state is ")
    # print(board)
    while not check_win(board):
        cur_state = board2state(board)
        statesVisited.append(cur_state)
        moves = legal_actions(board)
        legalActions.append(moves)
        move = strategy(ps.board)
        actionsTaken.append(move)
        if move not in moves:
            break
        row, column, direction = move[0], move[1], move[2]
        ps.board = take_action(ps.board, row, column, direction)
        reward = 0
        rewardsGained.append(reward)
        # print("The turn has ended. The current board state is ")
        # print(board)
    if check_win(board):
        # print('The player has won the game!')
        reward = 1
    else:
        # print('An illegal move was made. The player has lost the game.')
        reward = -1
    rewardsGained.append(reward)
    return (statesVisited, actionsTaken, rewardsGained, check_win(ps.board), legalActions)
	

def best_policy(board):
   actions = legal_actions(board)
   curr_state = board2state(board)
   possible_actions_q = {}
   for act in actions:
       key = opt_avf(curr_state, act, 2, 0.5)
       value = key
       entry = act
       possible_actions_q[key] = entry
   best_q = max(possible_actions_q.keys())
   return possible_actions_q[best_q]

#board state 6 jumps from winning: '0000000001000000100000101000001010000010000000000'

def random_policy(board):
    actions = legal_actions(board)
    if len(actions) == 0:
        return random.choice(possible_actions(board))
    return random.choice(actions)

class PegSolitaire(Game):

    def __init__(self):
        self.board = create_board()

    def possible_actions(self, state):
        board = state2board(state)
        return legal_actions(board)

    def random_policy(self):
        return random_policy

    def transition_prob_matrix(self):
        return transition_prob_matrix(self.board)

    def next_states(self):
        state = board2state(self.board)
        return next_states(state)

    def play(self, strategy):
        return play(strategy)

    def isLoseState(self):
        return check_win(self.board)

    def isWinState(self):
        return check_win(self.board)

# if __name__ == '__main__':
#     print('Subclass:', issubclass(PegSolitaire, Game))
