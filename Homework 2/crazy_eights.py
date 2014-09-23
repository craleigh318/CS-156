__author__ = 'Christopher Raleigh and Anthony Ferrero'


class CrazyEight(object):
    """Contains methods for AI actions."""

    @staticmethod
    def move(partial_state):
        pass

    @staticmethod
    def move_perfect_knowledge(state):
        pass


class Suit(object):
    """A collection of 13 cards."""

    @staticmethod
    def get_suit(deck_card):
        suit = deck_card / Deck.num_suits()
        return suit

    @staticmethod
    def get_suit_card(deck_card):
        suit_card = deck_card % Deck.num_suits()
        return suit_card

    @staticmethod
    def num_cards():
        return 13

    @staticmethod
    def ace():
        return 0

    @staticmethod
    def two():
        return 1

    @staticmethod
    def three():
        return 2

    @staticmethod
    def four():
        return 3

    @staticmethod
    def five():
        return 4

    @staticmethod
    def six():
        return 5

    @staticmethod
    def seven():
        return 6

    @staticmethod
    def eight():
        return 7

    @staticmethod
    def nine():
        return 8

    @staticmethod
    def ten():
        return 9

    @staticmethod
    def jack():
        return 10

    @staticmethod
    def queen():
        return 11

    @staticmethod
    def king():
        return 12


class Deck(object):
    """The collection of all 52 cards."""

    @staticmethod
    def get_deck_card(suit_card, suit):
        deck_card = suit * Suit.num_cards()
        deck_card += suit_card
        return deck_card

    @staticmethod
    def num_suits():
        return 4

    @staticmethod
    def spades():
        return 0

    @staticmethod
    def hearts():
        return 1

    @staticmethod
    def diamonds():
        return 2

    @staticmethod
    def clubs():
        return 3


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

    @property
    def human(self):
        return self.__players[self.__human_index]

    @property
    def ai(self):
        if self.__human_index == 0:
            ai_index = 1
        else:
            ai_index = 0
        return self.__players[ai_index]