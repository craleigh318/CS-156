__author__ = "Christopher Raleigh"

from food_agent import FoodAgent
from board_square_type import BoardSquareType


class BoardState(object):
    """A board with a food agent."""

    def __init__(self, board, x, y):
        self.board = board
        self.agent = FoodAgent(board, x, y)

    def food_eaten(self):
        """Returns true if the food agent occupies a space with food."""
        agent = self.agent
        return self.board.squares[agent.x][agent.y] is BoardSquareType.food
