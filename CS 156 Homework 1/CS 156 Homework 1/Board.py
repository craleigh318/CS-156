__author__ = "Christopher Raleigh"

from BoardSquareType import BoardSquareType


class Board(object):
    """A rectangular collection of squares."""
    def __init__(self, width, height):
        self.width = width
        self.height = height
        empty_squares = [BoardSquareType.empty for i in xrange(height)]
        self.squares = [empty_squares for i in xrange(width)]

    def set_square(self, x, y, squareType):
        """Sets the type of a square."""
        self.squares[x][y] = squareType
