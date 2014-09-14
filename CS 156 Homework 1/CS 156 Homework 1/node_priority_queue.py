__author__ = 'Christopher Raleigh and Anthony Ferrero'

import heapq


class NodePriorityQueue(object):

    def __init__(self, start_node):
        self._internal_list = []
        self.push(start_node)

    def __len__(self):
        return len(self._internal_list)

    def push(self, node):
        heapq.heappush(self._internal_list, (node.get_cost(), node))

    def pop(self):
        return heapq.heappop(self._internal_list)
