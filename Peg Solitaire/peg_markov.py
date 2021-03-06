import numpy as np
from peg_solitaire import *

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


if __name__ == '__main__':
    init_state = board2state(create_board())
    move = (3, 3, 3)
    d, e = 2, 0.1


