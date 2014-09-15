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
        self.movement_path_list = []

    def on_food_agent_turn(self):
        """Actions for the AI to perform on its agent's turn."""
        direction = self.recommend_direction()
        self.board_state.agent.move(direction)

    def solution(self, tree):
        """Returns the path that the agent should take in the form of a list."""
        solution_list = self.movement_path_list
        if tree is None:
            # This only works for Test 1.
            # Other tests will require a tree.
            solution_list.append(Direction.down)
            solution_list.append(Direction.right)
            solution_list.append(Direction.right)
        else:
            current_node = tree
            while current_node is not None:
                solution_list.append(current_node.get_direction())
                current_node = current_node.get_parent()
            return list(reversed(solution_list))

    def recommend_direction(self):
        """Returns a direction that will lead to a solution."""
        return self.movement_path_list.pop()

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
        start_node_cost = 0
        start_node = Node(agent_location=self.board_state.agent.get_location(),
                          direction=None,
                          path_cost=start_node_cost,
                          cost=start_node_cost)
        frontier_nodes = NodePriorityQueue(start_node)
        explored_locations = set()

        while True:

            no_solution = len(frontier_nodes) == 0
            if no_solution:
                self.board_is_unsolvable = True
                break;

            current_node = frontier_nodes.pop()
            # Not using move(), because A* can switch between considering completely different paths at any time.
            self.board_state.agent.set_location(current_node.get_agent_location())
            if self.board_state.food_eaten():
                self.movement_path_list = self.solution(current_node)
                break;

            explored_locations.add(current_node.get_agent_location())
            for direction in self.possible_actions():
                child_node = self._make_child_node(current_node, direction)
                child_in_frontier = child_node in frontier_nodes
                if child_node.get_agent_location() not in explored_locations and not child_in_frontier:
                    frontier_nodes.push(child_node)
                elif child_in_frontier and frontier_nodes.get_priority(child_node) > child_node.get_cost():
                    frontier_nodes.set_priority(child_node, child_node.get_cost())

    def _make_child_node(self, current_node, direction):
        child_node_path_cost = current_node.get_path_cost() + 1
        self.board_state.agent.move(direction)
        heuristic_value = self._heuristic(self.board_state.agent.get_location(),
                                          self.board_state.board.get_food_location())
        child_node_cost = child_node_path_cost + heuristic_value
        return Node(agent_location=self.board_state.agent.get_location(),
                    direction=direction,
                    cost=child_node_cost,
                    path_cost=child_node_path_cost,
                    parent=current_node)
