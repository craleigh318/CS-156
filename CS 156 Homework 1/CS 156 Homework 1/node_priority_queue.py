__author__ = 'Christopher Raleigh and Anthony Ferrero'

import heapq


class NodePriorityQueue(object):

    def __init__(self, start_agent_location):
        self._internal_list = []
        self.push(start_agent_location)

    def __len__(self):
        return len(self._internal_list)

    def push(self, agent_location, cost):
        heapq.heappush(self._internal_list, (cost, agent_location))

    def pop(self):
        return heapq.heappop(self._internal_list)
