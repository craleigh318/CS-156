__author__ = "Christopher Raleigh and Anthony Ferrero"

from board_square_type import BoardSquareType
from board_square import BoardSquare


class Board(object):
    """A rectangular collection of squares, not including a food agent."""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.squares = [[BoardSquareType.empty for i in xrange(height)]
                        for i in xrange(width)]
        self._food_location = None

    def set_square(self, x, y, square_type):
        """Sets the type of a square."""
        self.squares[x][y] = square_type

    def get_food_location(self):
        """Lazily evaluated food location."""
        if self._food_location is None:
            for x in xrange(self.width):
                for y in xrange(self.height):
                    if self.squares[x][y] == BoardSquareType.food:
                        self._food_location = BoardSquare(x, y)
        return self._food_location
