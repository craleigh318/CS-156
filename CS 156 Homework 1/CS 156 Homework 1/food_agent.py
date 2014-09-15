__author__ = "Christopher Raleigh and Anthony Ferrero"

from board_square_type import BoardSquareType
from direction import Direction
from board_square import BoardSquare


class FoodAgent(object):
    """An agent that moves in the maze to reach food."""

    def __init__(self, board, x, y):
        self.board = board
        self.x = x
        self.y = y

    def can_move(self, direction):
        """Can move in the specified direction."""
        target_x = self.x
        target_y = self.y
        if direction == Direction.up:
            target_y -= 1
        elif direction == Direction.down:
            target_y += 1
        elif direction == Direction.left:
            target_x -= 1
        elif direction == Direction.right:
            target_x += 1
        else:
            return False
        if (target_x < 0) or (target_y < 0):
            return False
        board = self.board
        max_x = board.width - 1
        max_y = board.height - 1
        if (target_x > max_x) or (target_y > max_y):
            return False
        if board.squares[target_x][target_y] == BoardSquareType.wall:
            return False
        return True

    def move(self, direction):
        """Moves one square in the specified direction"""
        ret = self.can_move(direction)
        if ret:
            if direction == Direction.up:
                self.y -= 1
            elif direction == Direction.down:
                self.y += 1
            elif direction == Direction.left:
                self.x -= 1
            elif direction == Direction.right:
                self.x += 1
        return ret

    # For convenience
    def get_location(self):
        return BoardSquare(self.x, self.y)

    def set_location(self, board_square_location):
        self.x = board_square_location.x
        self.y = board_square_location.y
