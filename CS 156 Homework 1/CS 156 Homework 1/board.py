__author__ = "Christopher Raleigh and Anthony Ferrero"

from board_square_type import BoardSquareType


class Board(object):
    """A rectangular collection of squares, not including a food agent."""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.squares = [[BoardSquareType.empty for i in xrange(height)]
                        for i in xrange(width)]

    def set_square(self, x, y, square_type):
        """Sets the type of a square."""
        self.squares[x][y] = square_type
