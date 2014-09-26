__author__ = 'Christopher Raleigh and Anthony Ferrero'


class CrazyEight(object):
    """Contains methods for AI actions."""

    @staticmethod
    def move(partial_state):
        pass

    @staticmethod
    def move_perfect_knowledge(state):
        pass


class Card(object):
    """A playing card."""

    def __init__(self, deck_index):
        self.__deck_index = deck_index

    @property
    def deck_index(self):
        return self.__deck_index

    @property
    def suit(self):
        suit = self.__deck_index / Deck.num_suits()
        return suit

    @property
    def rank(self):
        rank = self.__deck_index % Deck.num_suits()
        return rank


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
        self.__hand = []

    def add_card(self, card):
        can_add = (self.__hand.count(card) <= 0)
        if can_add:
            self.__hand.append(card)
        return can_add

    def give_card(self, card, recipient):
        received = recipient.add_card(card)
        if received:
            self.__hand.remove(card)
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
            self.__cards.append(Card(index))

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

    def __init__(self, deck, hand, partial_state):
        self.__deck = deck
        self.__hand = hand
        self.__partial_state = partial_state

    @property
    def deck(self):
        return self.__deck

    @property
    def hand(self):
        return self.__hand

    @property
    def partial_state(self):
        return self.__partial_state


class PartialState(object):
    """Stores the face-up card, the suit, the hand, and the history."""

    def __init__(self, face_up_card, suit, hand, history):
        self.__face_up_card = face_up_card
        self.__suit = suit
        self.__hand = hand
        self.__history = history

    @property
    def face_up_card(self):
        return self.__face_up_card

    @property
    def suit(self):
        return self.__suit

    @property
    def hand(self):
        return self.__hand

    @property
    def history(self):
        return self.__history


class Move(object):
    """An action taken by a player."""

    def __init__(self, player_num, face_up_card, suit, number_of_cards):
        self.__player_num = player_num
        self.__face_up_card = face_up_card
        self.__suit = suit
        self.__number_of_cards = number_of_cards

    @property
    def player_num(self):
        return self.__player_num

    @property
    def face_up_card(self):
        return self.__face_up_card

    @property
    def suit(self):
        return self.__suit

    @property
    def number_of_cards(self):
        return self.__number_of_cards


class PlayerList(object):
    """Contains information for both players."""

    def __init__(self, human_index):
        self.__players = [Hand(), Hand()]
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