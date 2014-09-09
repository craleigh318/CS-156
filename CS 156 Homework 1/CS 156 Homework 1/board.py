__author__ = "Christopher Raleigh"

from board_square_type import BoardSquareType


class Board(object):
    """A rectangular collection of squares."""
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.squares = [[BoardSquareType.empty] * height] * width

    @property
    def square(self, x, y, square_type):
        """Sets the type of a square."""
        self.squares[x][y] = square_type
