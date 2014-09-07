__author__ = "Christopher Raleigh"

from FoodAgent import FoodAgent
from BoardSquareType import BoardSquareType


class BoardState(object):
    """A board with a food agent."""

    def __init__(self, board, x, y):
        self.board = board
        self.agent = FoodAgent(board, x, y)

    def foodEaten(self):
        """Returns true if the food agent occupies a space with food."""
        agent = self.agent
        return self.board.squares[agent.x][agent.y] is BoardSquareType.food
