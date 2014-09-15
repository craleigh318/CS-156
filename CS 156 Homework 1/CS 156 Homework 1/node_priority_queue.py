__author__ = 'Christopher Raleigh and Anthony Ferrero'

import heapq


class NodePriorityQueue(object):
    """A priority queue for nodes used in the A* algorithm."""

    class Priority(object):
        """Allows the priority of a node to change without the priority queue needing to know where
           it is in its internal list."""

        def __init__(self, value):
            self.value = value

        def __cmp__(self, other):
            return isinstance(other, type(self)) and self.value == other.value

    def __init__(self, start_node):
        self._internal_list = []
        # For easily checking for membership and accessing agent location priority
        # Maps node agent location (so we don't need to implement __hash__ for Node) to its associated Priority object
        self._priority_map = {}
        self.push(start_node)

    def __len__(self):
        return len(self._internal_list)

    def __contains__(self, node):
        """Only checks to see if a node is in this queue, not the tuple of (priority, node)
           as might be expected."""
        return node.get_agent_location() in self._priority_map

    def push(self, node):
        """Adds a node to the priority queue with a priority equal to its cost."""
        priority = self.Priority(node.get_cost())
        heapq.heappush(self._internal_list, (priority, node))
        self._priority_map[node.get_agent_location()] = priority

    def pop(self):
        """Returns a node on the board with the least cost."""
        ignored_cost, popped_node = heapq.heappop(self._internal_list)
        del self._priority_map[popped_node.get_agent_location()]
        return popped_node

    def set_priority(self, node, new_cost):
        """Replaces a node's priority with a new one."""
        self._priority_map[node.get_agent_location()].value = new_cost
        heapq.heapify(self._internal_list)

    def get_priority(self, node):
        return self._priority_map[node.get_agent_location()].value
