__author__ = "Christopher Raleigh and Anthony Ferrero"

from direction import Direction


class FoodAgentAI(object):
    """An intelligence that controls a food agent"""

    def __init__(self, board_state, heuristic):
        self.board_state = board_state
        self._heuristic = heuristic
        self.board_is_unsolvable = False
        self.solution_list = [Direction.down, Direction.right, Direction.right]

    def on_food_agent_turn(self):
        """Actions for the AI to perform on its agent's turn."""
        direction = self.recommend_direction()
        self.board_state.agent.move(direction)

    def recommend_direction(self):
        """Returns a direction that will lead to a solution."""
        return self.solution_list.pop()