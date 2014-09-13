__author__ = "Christopher Raleigh and Anthony Ferrero"

from board_square_type import BoardSquareType


class FoodAgent(object):
    """An agent that moves in the maze to reach food."""

    def __init__(self, board, x, y):
        self.board = board
        self.x = x
        self.y = y

    def move_up(self):
        """Moves one square up."""
        if self.y > 0:
            return self.move_to(self.x, (self.y - 1))
        else:
            return False

    def move_down(self):
        """Moves one square down."""
        if self.y < (self.board.height - 1):
            return self.move_to(self.x, (self.y + 1))
        else:
            return False

    def move_left(self):
        """Moves one square left."""
        if self.x > 0:
            return self.move_to((self.x - 1), self.y)
        else:
            return False

    def move_right(self):
        """Moves one square right."""
        if self.x < (self.board.width - 1):
            return self.move_to((self.x + 1), self.y)
        else:
            return False

    def move_to(self, x, y):
        """Moves to the defined coordinates"""
        target_space = self.board.squares[x][y]
        if target_space is not BoardSquareType.wall:
            self.x = x
            self.y = y
            return True
        else:
            return False