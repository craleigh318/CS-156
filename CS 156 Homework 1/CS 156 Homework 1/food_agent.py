__author__ = "Christopher Raleigh"


class FoodAgent(object):
    """An agent that moves in the maze to reach food."""
    def __init__(self, board, x, y):
        self.board = board
        self.x = x
        self.y = y

    def move_up(self):
        """Moves one square up."""
        if self.y > 0:
            self.y -= 1
            return True
        else:
            return False

    def move_down(self):
        """Moves one square down."""
        if self.y < (self.board.height - 1):
            self.y += 1
            return True
        else:
            return False

    def move_left(self):
        """Moves one square left."""
        if self.x > 0:
            self.x -= 1
            return True
        else:
            return False

    def move_right(self):
        """Moves one square right."""
        if self.x < (self.board.width - 1):
            self.x += 1
            return True
        else:
            return False
