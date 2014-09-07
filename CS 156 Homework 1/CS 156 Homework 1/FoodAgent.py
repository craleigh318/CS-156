__author__ = "Christopher Raleigh"

class FoodAgent(object):
    """An agent that moves in the maze to reach food."""
    def __init__(self, board, x, y):
        self.board = board
        self.x = x
        self.y = y

    def moveUp(self):
        """Moves one square up."""
        if self.y > 0:
            --self.y
            return True
        else:
            return False

    def moveDown(self):
        """Moves one square down."""
        if self.y < (self.board.height - 1):
            ++self.y
            return True
        else:
            return False

    def moveLeft(self):
        """Moves one square left."""
        if self.x > 0:
            --self.x
            return True
        else:
            return False

    def moveRight(self):
        """Moves one square right."""
        if self.x < (self.board.width - 1):
            ++self.x
            return True
        else:
            return False