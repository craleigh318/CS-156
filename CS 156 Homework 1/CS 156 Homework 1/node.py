__author__ = "Christopher Raleigh and Anthony Ferrero"


class Node(object):
    """Represents a tree of nodes, used for searching. Note: we don't need to explicitly keep track of the action used
    to generate each node; tracking the location of the agent when each node is explored is enough."""

    def __init__(self, agent_location, cost, path_cost, parent=None):
        self._agent_location = agent_location
        self._path_cost = path_cost
        self._cost = cost
        self._parent = parent

    def __eq__(self, other):
        return isinstance(other, type(self)) and\
            self.get_agent_location() == other.get_agent_location() and\
            self.get_path_cost() == other.get_path_cost() and\
            self.get_cost() == other.get_cost()

    def __hash__(self):
        # It's important that a node only be hashed with regard to its _agent_location and _path_cost
        # for the internal map in NodePriorityQueue to work.
        return (hash(self._agent_location) ^ hash(self._path_cost) ^
                hash((self._agent_location, self._path_cost)))

    def get_agent_location(self):
        return self._agent_location

    def get_path_cost(self):
        return self._path_cost

    def get_cost(self):
        return self._cost

    def get_parent(self):
        return self._parent
