_zip = zip

def mean(s):
    """Return the arithmetic mean of a sequence of numbers s.

    >>> mean([-1, 3])
    1.0
    >>> mean([0, -3, 2, -1])
    -0.5
    """
    assert len(s) > 0, 'cannot find mean of empty sequence'
    return sum(s) / len(s)

def zip(*sequences):
    """Returns a list of lists, where the i-th list contains the i-th
    element from each of the argument sequences.

    >>> zip(range(0, 3), range(3, 6))
    [[0, 3], [1, 4], [2, 5]]
    >>> for a, b in zip([1, 2, 3], [4, 5, 6]):
    ...     print(a, b)
    1 4
    2 5
    3 6
    >>> for triple in zip(['a', 'b', 'c'], [1, 2, 3], ['do', 're', 'mi']):
    ...     print(triple)
    ['a', 1, 'do']
    ['b', 2, 're']
    ['c', 3, 'mi']
    """
    return list(map(list, _zip(*sequences)))

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
    return board

#cannot find a good way to write so assume the board to be 2*2
def check_win(board):
    if board[0][0] == board[0][1] or board[1][0] == board[1][1] or board[0][0] == board[1][0] or board[0][1] == board[1][1]:
        return True
    else:
        return False
        
def check_tie(board):
    if board[0][0] != 0 and board[1][0] != 0 and board[0][1] != 0 and board[1][1] != 0:
        return True
    else:
        return False
