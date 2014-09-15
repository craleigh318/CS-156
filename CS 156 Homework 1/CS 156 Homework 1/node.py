__author__ = "Christopher Raleigh and Anthony Ferrero"


class Node(object):
    """Represents a tree of nodes. Used for searching with A*."""

    def __init__(
            self,
            agent_location,
            direction,
            cost,
            path_cost,
            parent=None):
        self._agent_location = agent_location
        self._direction = direction
        self._path_cost = path_cost
        self._cost = cost
        self._parent = parent

    def get_agent_location(self):
        return self._agent_location

    def get_direction(self):
        return self._direction

    def get_path_cost(self):
        return self._path_cost

    def get_cost(self):
        return self._cost

    def get_parent(self):
        return self._parent
