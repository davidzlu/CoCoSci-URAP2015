# A file containing data for all the map pieces for Thunderbolt Apache Leader

def get_piece(piecenum):
    """Creates a piece object and returns it.
    0 stands for no ridge while 1 means ridge"""
    if piecenum == 1:
        return Piece(0, 0, 0, 0, 0, 0) #written as example, not actually piece 1
    elif piecenum == 2:
        return Piece(1, 0, 0, 0, 1, 1) #same as above


class Piece:
    """Terrain pieces are supposed to be placed with the arrow on it
    facing up so the sides of the hexagon are labeled alphabetically
    in a clockwise manner starting from that arrow i.e. side a is the
    top-right side while side f is the top-left"""

    def __init__(self, a, b, c, d, e, f, center=None):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f
        self.center = center
