# A file containing data for all the map pieces for Thunderbolt Apache Leader

def get_tile(tilenum):
    """Creates a tile object and returns it.
    0 stands for no ridge while 1 means ridge"""
    if tilenum == 1:
        return Tile(0, 0, 0, 0, 0, 0)
    elif tilenum == 2:
        return Tile(0, 0, 0, 0, 0, 0) 
    elif tilenum == 3:
        return Tile(0, 0, 0, 0, 0, 0)
    elif tilenum == 4:
        return Tile(0, 0, 0, 0, 0, 0)
    elif tilenum == 5:
        return Tile(0, 1, 0, 0, 1, 0)
    elif tilenum == 6:
        return Tile(0, 0, 0, 0, 0, 1)
    elif tilenum == 7:
        return Tile(1, 0, 0, 1, 0, 0)
    elif tilenum == 8:
        return Tile(0, 1, 0, 0, 1, 0)
    elif tilenum == 9:
        return Tile(0, 0, 0, 0, 1, 1)
    elif tilenum == 10:
        return Tile(0, 1, 1, 0, 0, 0)
    elif tilenum == 11:
        return Tile(0, 1, 0, 0, 0, 0)
    elif tilenum == 12:
        return Tile(0, 0, 1, 0, 0, 0)
    elif tilenum == 13:
        return Tile(1, 0, 0, 0, 1, 1)
    elif tilenum == 14:
        return Tile(0, 0, 0, 0, 1, 0)
    elif tilenum == 15:
        return Tile(0, 1, 0, 1, 1, 0)
    elif tilenum == 16:
        return Tile(1, 1, 1, 1, 0, 0)
    elif tilenum == 17:
        return Tile(1, 1, 0, 1, 1, 0)
    elif tilenum == 18:
        return Tile(1, 0, 1, 1, 0, 1)



class Tile:
    """Terrain pieces are supposed to be placed with the arrow on it
    facing up so the sides of the hexagon are labeled alphabetically
    in a clockwise manner starting from that arrow i.e. side a is the
    top-right side while side f is the top-left
    
    *piece refers to whether there is a piece on the side labeled *
    *next refers to which tile is adjacent to the current tile on that side"""
    
    # Edge location values
    A = "a"
    B = "b"
    C = "c"
    D = "d"
    E = "e"
    F = "f"
    CENTER = "center"

    def __init__(self, a, b, c, d, e, f, center=[],
                 apiece=[], bpiece=[], cpiece=[], dpiece=[], epiece=[], fpiece=[],
                 anext=[], bnext=[], cnext=[], dnext=[], enext=[], fnext=[]):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f
        self.center = center
        self.apiece = apiece
        self.bpiece = bpiece
        self.cpiece = cpiece
        self.dpiece = dpiece
        self.epiece = epiece
        self.fpiece = fpiece
        self.anext = anext
        self.bnext = bnext
        self.cnext = cnext
        self.dnext = dnext
        self.enext = enext
        self.fnext = fnext
        
    def get_location(self, piece):
        """Returns location of the piece. Location represented by class variables.
        """
        if piece in self.center:
            return self.CENTER
        if piece in self.apiece:
            return self.A
        if piece in self.bpiece:
            return self.B
        if piece in self.cpiece:
            return self.C
        if piece in self.dpiece:
            return self.D
        if piece in self.epiece:
            return self.E
        if piece in self.fpiece:
            return self.F
        
    def get_neighbor(self, edge):
        if edge == self.CENTER:
            return self
        if edge == self.A:
            return self.anext
        if edge == self.B:
            return self.bnext
        if edge == self.C:
            return self.cnext
        if edge == self.D:
            return self.dnext
        if edge == self.E:
            return self.enext
        if edge == self.F:
            return self.fnext
    
    def get_opposite_edge(self, edge):
        if edge == self.A:
            return self.D
        if edge == self.B:
            return self.E
        if edge == self.C:
            return self.F
        if edge == self.D:
            return self.A
        if edge == self.E:
            return self.B
        if edge == self.F:
            return self.C
        
    def remove_piece(self, piece):
        if piece in self.center:
            self.center.remove(piece)
        if piece in self.apiece:
            self.apiece.remove(piece)
        if piece in self.bpiece:
            self.bpiece.remove(piece)
        if piece in self.cpiece:
            self.cpiece.remove(piece)
        if piece in self.dpiece:
            self.dpiece.remove(piece)
        if piece in self.epiece:
            self.epiece.remove(piece)
        if piece in self.fpiece:
            self.fpiece.remove(piece)
            
    def add_piece(self, piece, edge):
        if edge == self.CENTER:
            self.center.append(piece)
        if edge == self.A:
            self.apiece.append(piece)
        if edge == self.B:
            self.bpiece.append(piece)
        if edge == self.C:
            self.cpiece.append(piece)
        if edge == self.D:
            self.dpiece.append(piece)
        if edge == self.E:
            self.epiece.append(piece)
        if edge == self.F:
            self.fpiece.append(piece)
            
    def edge_has_ridge(self, edge):
        if edge == self.A:
            return self.a
        if edge == self.B:
            return self.b
        if edge == self.C:
            return self.c
        if edge == self.D:
            return self.d
        if edge == self.E:
            return self.e
        if edge == self.F:
            return self.f
    
    