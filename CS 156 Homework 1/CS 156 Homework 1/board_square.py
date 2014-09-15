__author__ = "Christopher Raleigh and Anthony Ferrero"


class BoardSquare(object):
    """Represents the location of a square on the board."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(self.x) ^ hash(self.y) ^ hash((self.x, self.y))