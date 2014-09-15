__author__ = "Christopher Raleigh and Anthony Ferrero"

from food_agent_class import FoodAgent
from board_square_type import BoardSquareType
from board_square import BoardSquare


class BoardState(object):
    """A board with a food agent."""

    def __init__(self, board, x, y):
        self.board = board
        self.agent = FoodAgent(board, x, y)
        self.agent_start_location = BoardSquare(x, y)

    def food_eaten(self):
        """Returns true if the food agent occupies a space with food."""
        agent = self.agent
        return self.board.squares[agent.x][agent.y] == BoardSquareType.food

    def reset_agent_position(self):
        self.agent.set_location(self.agent_start_location)
