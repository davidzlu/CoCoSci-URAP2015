from Markov import *
import random, ast
from random import randrange

def create_board(rows=2, columns=2):
    """ Returns a board with the given dimensions.
    >>> create_board(3, 5)
    [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
    """
    return [[0 for x in range(0, columns)] for x in range(0, rows)]

def put_piece(board, row, column, player):
    """ Place a player's piece in a spot on the board."""
    assert row >= 0 and column >= 0 and row < len(board) and column < min([len(x) for x in board])
    """ in case rows/columns out of bounds"""
    x = board[:][:]
    x[row][column] = player
    return x

#cannot find a good way to write so assume the board to be 2*2
def check_win(board):
    """ Returns True if a player has won and 1 or 2 depending on which player won. """
    space0 = board[0][0]
    space1 = board[0][1]
    space2 = board[1][0]
    space3 = board[1][1]
    if space0 != 0 and space1 != 0:
        if space0 == space1:
            return True, space0
    if space2 != 0 and space3 != 0:
        if space2 == space3:
            return True, space2
    if space0 != 0 and space2 != 0:
        if space0 == space2:
            return True, space0
    if space1 != 0 and space3 != 0:
        if space1 == space3:
            return True, space1
    return False, None

def check_tie(board):
    """Returns True if there has been a tie, False otherwise."""
    if board[0][0] != 0 and board[1][0] != 0 and board[0][1] != 0 and board[1][1] != 0:
        return True
    else:
        return False

def other(who):
    """Helper method for play()"""
    return 3 - who

def moves_made(state):
    """
    Takes in a string representation of the current state and counts 
    the number of moves made up until that state of the game.
    """
    count = 0
    for i in range(len(state)):
        if state[i] == '0':
            count += 1
    return len(state) - count


def human_player(board):
    """
    A strategy for use with play().
    When passed into play(), an interactive game of TicTacToe begins
    against an opponent who choses moves randomly. This function allows
    users to input moves through the terminal.
    """
    actions = action_space(board)
    curr_state = board2state(board)
    moves = legal_actions(curr_state, actions)
    states = state_space()
    state_tree = create_state_tree(states)
    print("The current state of the game is: " + curr_state)
    print("Your available moves are: ")
    print(moves)
    response = input("Enter the move you'd like to make: ")
    my_move = ast.literal_eval(response)
    while my_move not in moves:
        my_move = ast.literal_eval(input("Please enter a valid move: "))
    test_state, reward = simulate_transition(curr_state, my_move)
    probs = []
    poss_states = []
    for next_state in state_tree[test_state]:
        if moves_made(next_state) == moves_made(test_state)+1:
            poss_states.append(next_state)
            probs.append(transition_prob(next_state, curr_state, my_move, state_tree)[0])
    print("These are the next possible states: ")
    print(poss_states)
    print("These are the probabilities associated with each state: ")
    print(probs)
    print("Your expected reward is: ")
    print(reward)
    response2 = input("Would you like to change your move? y/n: ")
    if (response2 == 'n') | (response2 == 'no'):
        return my_move
    else:
        return human_player(board)


def play(strategy1= human_player):
    """
    The main function for running a game of TicTacToe. Default is set to
    human_player phase but this function also accepts learning algorithms which return moves.
    Currently acceptable arguments are human_player and best_policy
    """
    who = 1
    board = create_board()
    print("The game has begun. The current board state is ")
    print(board)
    while not check_win(board)[0] and not check_tie(board):# try make a list of tuple for every move and return it with final
        if who == 1:
            actions = action_space(board)
            curr_state = board2state(board)
            moves = legal_actions(curr_state, actions)
            move = strategy1(board)
            if move not in moves:
                break
            row, column = move[0], move[1]
            board = put_piece(board, row, column, who)
            reward = 0
            print("Player's turn end.The current board state is ")
            print(board)
        if who == 2:
            actions = action_space(board)
            curr_state = board2state(board)
            moves = legal_actions(curr_state, actions)
            states = state_space()
            state_tree = create_state_tree(states)
            random_index = randrange(0, len(moves))
            row, column = moves[random_index][0], moves[random_index][1]
            board = put_piece(board, row, column, who)
            print("Computer's turn end.The current board state is ")
            print(board)
        who = other(who)
    if check_win(board)[0]:
        print('Player ' + str(check_win(board)[1]) + ' has won!')
        if str(check_win(board)[1]) == '1':
            reward = 1
        else:
            reward = -1
    elif check_tie(board):
        print('The game has ended in a tie.')
    else:
        print('An illegal move was made.')
        reward = -100
    return board, reward

def best_policy(board):
    """
    An 'agent' function that looks ahead and calculates future rewards when deciding its
    next move.
    """
    actions = action_space(board)
    curr_state = board2state(board)
    possible_actions_q = {}
    for act in actions:
        key = q(curr_state, act)
        value = key
        entry = act
        possible_actions_q[key] = entry
    best_q = max(possible_actions_q.keys())
    return possible_actions_q[best_q]


