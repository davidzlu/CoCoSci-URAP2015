def mean(s):
    """Return the arithmetic mean of a sequence of numbers s.

    >>> mean([-1, 3])
    1.0
    >>> mean([0, -3, 2, -1])
    -0.5
    """
    assert len(s) > 0, 'cannot find mean of empty sequence'
    return sum(s) / len(s)

def create_board(rows, columns):
    """ Returns a board with the given dimensions.

    >>> create_board(3, 5)
    [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
    """
    return [[0 for x in range(0, columns)] for x in range(0, rows)]

def put_piece(board, row, column, player):
    """ Place a player's piece in a spot on the board."""
    assert row >= 0 and column >= 0 and row < len(board) and column < min([len(x) for x in board])
    """ in case rows/columns out of bounds"""
    x = lst[:][:]
    x[row][column] = player
    return x

def check_win_row(board):
    default = True
    for x in range(0, len(board)):
        for y in range(0, len(board[x])):
            if board[x][y] != mean(board[x]):
                default = False
    return default
