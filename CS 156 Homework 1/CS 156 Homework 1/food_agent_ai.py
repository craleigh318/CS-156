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

    @staticmethod
    def solution(tree):
        """Returns a list of directions the agent should move to
           get to the food via an optimal path."""
        solution_list = []
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
        directions_list = \
            [Direction.right, Direction.left, Direction.down, Direction.up]
        possible_directions = []
        agent = self.board_state.agent
        while directions_list:
            next_direction = directions_list.pop()
            if agent.can_move(next_direction):
                possible_directions.append(next_direction)
        return possible_directions

    def find_path(self):
        """Uses A* to find a path from the agent's current position to the food
           on the board."""
        start_node_cost = 0
        start_node = Node(agent_location=self.board_state.agent.get_location(),
                          direction=None,
                          path_cost=start_node_cost,
                          cost=start_node_cost)
        frontier = NodePriorityQueue(start_node)
        explored_locations = set()

        agent = self.board_state.agent
        while True:
            no_solution = len(frontier) == 0
            if no_solution:
                self.board_is_unsolvable = True
                break

            current_node = frontier.pop()
            '''Not using move(), because A* can switch between considering
            completely different paths at any time.'''
            agent.set_location(current_node.get_agent_location())
            if self.board_state.food_eaten():
                self.movement_path_list = self.solution(current_node)
                break

            explored_locations.add(current_node.get_agent_location())
            for direction in self.possible_actions():
                # Must try to move from the position of current_node repeatedly
                agent.set_location(current_node.get_agent_location())
                agent.move(direction)

                child = self._make_child_node(current_node, direction)
                child_in_frontier = child in frontier

                if child.get_agent_location() not in explored_locations and \
                        not child_in_frontier:
                    frontier.push(child)
                elif child_in_frontier and \
                        frontier.get_priority(child) > child.get_cost():
                    frontier.set_priority(
                        node=child,
                        new_cost=child.get_cost()
                    )

    def _make_child_node(self, current_node, direction):
        """Creates a child node of current_node."""
        child_node_path_cost = current_node.get_path_cost() + 1
        heuristic_value = self._heuristic(
            self.board_state.agent.get_location(),
            self.board_state.board.get_food_location()
        )
        child_node_cost = child_node_path_cost + heuristic_value
        return Node(agent_location=self.board_state.agent.get_location(),
                    direction=direction,
                    cost=child_node_cost,
                    path_cost=child_node_path_cost,
                    parent=current_node)
