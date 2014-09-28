__author__ = 'Christopher Raleigh and Anthony Ferrero'

import driver

first_player = driver.get_first_player()
current_state = State()


class CrazyEight(object):
    """Contains methods for AI actions."""

    @staticmethod
    def move(partial_state):
        pass

    @staticmethod
    def move_perfect_knowledge(state):
        pass


class CardTypes(object):
    """Suits and ranks of cards."""

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


class Hand(object):
    """An actor in the game."""

    def __init__(self):
        self.__cards = []

    def add_card(self, card):
        can_add = (self.__cards.count(card) <= 0)
        if can_add:
            self.__cards.append(card)
        return can_add

    def give_card(self, card, recipient):
        received = recipient.add_card(card)
        if received:
            self.__cards.remove(card)
        return received


class Deck(object):
    """The collection of all 52 cards."""

    @staticmethod
    def num_cards():
        return 52

    @staticmethod
    def num_suits():
        return 4

    def __init__(self):
        self.__cards = []
        max_index = Deck.num_cards() - 1
        for index in xrange(0, max_index):
            self.__cards.append(index)

    def add_card(self, card):
        index = card.deck_index
        if self.__cards[index] is None:
            self.__cards[index] = card
            return True
        else:
            return False

    def give_card(self, card, recipient):
        received = recipient.add_card(card)
        if received:
            index = card.deck_index
            self.__cards[index] = None
        return received


class State(object):
    """Stores the deck, opponent's hand, and partial state."""

    def __init__(self):
        self.__deck = Deck()
        self.__hand = Hand()
        self.__partial_state = PartialState()

    @property
    def deck(self):
        return self.__deck

    @property
    def hand(self):
        return self.__hand

    @property
    def partial_state(self):
        return self.__partial_state

    def next_turn(self, move):
        self.__partial_state.add_move(move)
        temp = self.__hand
        self.__hand = self.__partial_state.hand
        self.__partial_state.hand = temp


class PartialState(object):
    """Stores information available to the current player."""

    def __init__(self):
        self.__face_up_card = None
        self.__suit = None
        self.__hand = Hand()
        self.__history = []

    @property
    def face_up_card(self):
        return self.__face_up_card

    @property
    def suit(self):
        return self.__suit

    @property
    def hand(self):
        return self.__hand

    @hand.setter
    def hand(self, value):
        self.__hand = value

    def add_move(self, move):
        self.__history.append(move)


class Move(object):
    """An action taken by a player."""

    def __init__(self, player_num, face_up_card, number_of_cards):
        self.__player_num = player_num
        self.__face_up_card = face_up_card
        self.__number_of_cards = number_of_cards

    @property
    def player_num(self):
        return self.__player_num

    @property
    def face_up_card(self):
        return self.__face_up_card

    @property
    def suit(self):
        suit = self.__face_up_card / Deck.num_suits()
        return suit

    @property
    def number_of_cards(self):
        return self.__number_of_cards