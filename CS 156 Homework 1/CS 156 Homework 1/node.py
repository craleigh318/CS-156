__author__ = "Christopher Raleigh and Anthony Ferrero"


class Node(object):
    """Represents a tree of nodes, used for searching. Note: we don't need to explicitly keep track of the action used
    to generate each node; tracking the location of the agent when each node is explored is enough."""

    def __init__(self, agent_location, cost, path_cost, parent=None):
        self._agent_location = agent_location
        self._path_cost = path_cost
        self._cost = cost
        self._parent = parent

    def get_agent_location(self):
        return self._agent_location

    def get_path_cost(self):
        return self._path_cost

    def get_cost(self):
        return self._cost

    def get_parent(self):
        return self._parent
