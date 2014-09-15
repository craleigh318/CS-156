__author__ = "Christopher Raleigh and Anthony Ferrero"

from direction import Direction
from node_priority_queue import NodePriorityQueue
from node import Node


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

    def find_path(self):

        start_node = Node(self.board_state.agent.get_location())
        frontier_nodes = NodePriorityQueue(start_node)
        explored_locations = set()

        searching_for_solution = True
        while searching_for_solution:

            no_solution = len(frontier_nodes) == 0
            if no_solution:
                self.board_is_unsolvable = False
                searching_for_solution = False

            current_node = frontier_nodes.pop()
            self.board_state.agent.set_location(current_node.get_agent_location())
            if self.board_state.food_eaten():
                self.solution_list = self.solution(current_node)
                searching_for_solution = False

            explored_locations += current_node.get_agent_location()
            for direction in self.possible_actions():
                child_node_path_cost = current_node.get_path_cost() + 1
                self.board_state.agent.move(direction)
                heuristic_value = self._heuristic(self.board_state.agent.get_location(),
                                                  self.board_state.board.get_food_location())
                child_node_cost = child_node_path_cost + heuristic_value
                
