_zip = zip

from Markov import *
import random, ast, randrange


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
    if board[0][0] != 0 and board[1][0] != 0 and board[0][1] != 0 and board[1][1] != 0:
        return True
    else:
        return False

def other(who):
    return 3 - who

<<<<<<< HEAD
def play(strategy1, strategy2):
=======
#human-player phase: we print a comment to ask
def play(strategy1=human_player):
>>>>>>> 90ed0fa70b205a5cccdf6f4dabc05f65d6822bee
    who = 1
    board = create_board()
    while not check_win(board)[0] and not check_tie(board):# try make a list of tuple for every move and return it with final
        if who == 1:
            row, column = strategy1(board)[0], strategy1(board)[1]
            board = put_piece(board, row, column, who)
            print("Player's turn end.The current board state is ")
            print(board)
        if who == 2:
            actions = action_space(board)
            curr_state = board2state(board)
            moves = legal_actions(curr_state, actions)
            states = create_states()
            state_tree = create_state_tree(states)
            random_index = randrange(0, len(moves))
            row, column = moves[random_index][0], moves[random_index][1]
            board = put_piece(board, row, column, who)
            print("Computer's turn end.The current board state is ")
            print(board)
        who = other(who)
    return board


def human_player(board):
    actions = action_space(board)
    curr_state = board2state(board)
    moves = legal_actions(curr_state, actions)
    states = create_states()
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
    for next_state in state_tree[test_state]:
        probs.append(transition_prob(next_state, test_state, my_move, state_tree))
    print("These are the next possible states: ")
    print(state_tree[test_state])
    print("These are the probabilities associated with each state: ")
    print(probs)
    response2 = input("Would you like to change your move? y/n: ")
    if (response2 == 'n') | (response2 == 'no'):
        return my_move
    else:
        return human_player(board)
