__author__ = 'Anthony Ferrero'


class Node(object):
    """Represents a singly-linked list of nodes."""

    def __init__(self, cost, action=None, parent=None):
        self._cost = cost
        self._action = action
        self._parent = parent

    def get_cost(self):
        return self._cost

    def get_action(self):
        return self._action

    def get_parent(self):
        return self._parent
