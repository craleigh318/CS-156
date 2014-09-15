__author__ = "Christopher Raleigh and Anthony Ferrero"

from direction import Direction


class FoodAgentAI(object):
    """An intelligence that controls a food agent"""

    def __init__(self, board_state, heuristic):
        self.board_state = board_state
        self._heuristic = heuristic
        self.board_is_unsolvable = False
        self.solution_list = []

    def on_food_agent_turn(self):
        """Actions for the AI to perform on its agent's turn."""
        direction = self.recommend_direction()
        self.board_state.agent.move(direction)

    def solution(self, tree):
        """Returns the path that the agent should take in the form of a list."""
        self.solution_list.append(Direction.down)
        self.solution_list.append(Direction.right)
        self.solution_list.append(Direction.right)

    def recommend_direction(self):
        """Returns a direction that will lead to a solution."""
        return self.solution_list.pop()

    def possible_actions(self):
        """Returns a list of directions that can be taken."""
        directions_list = [Direction.right, Direction.left, Direction.down, Direction.up]
        possible_directions = []
        agent = self.board_state.agent
        while directions_list:
            next_direction = directions_list.pop()
            if agent.can_move(next_direction):
                possible_directions.append(next_direction)
        return possible_directions