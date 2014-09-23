__author__ = 'Christopher Raleigh and Anthony Ferrero'


class CrazyEight(object):
    """Contains methods for AI actions."""

    @staticmethod
    def move(partial_state):
        pass

    @staticmethod
    def move_perfect_knowledge(state):
        pass


class Player(object):
    """An actor in the game."""
    pass


class PlayerList(object):
    """Contains information for both players."""

    def __init__(self, human_index):
        self.__players = [Player(), Player()]
        self.__human_index = human_index

    def get_player(self, index):
        return self.__players[index]

    def get_human(self):
        return self.__players[self.__human_index]

    def get_ai(self):
        if self.__human_index == 0:
            ai_index = 1
        else:
            ai_index = 0
        return self.__players[ai_index]