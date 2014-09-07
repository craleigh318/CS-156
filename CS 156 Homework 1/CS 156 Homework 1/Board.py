__author__ = "Christopher Raleigh"

from BoardSquareType import BoardSquareType

class Board(object):
    """A rectangular collection of squares."""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.squares = [[BoardSquareType.empty for i in xrange(height)] for i in xrange(width)]

    def setSquare(self, x, y, squareType):
        """Sets the type of a square."""
        self.squares[x][y] = squareType