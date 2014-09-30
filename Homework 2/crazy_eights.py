__author__ = 'Christopher Raleigh and Anthony Ferrero'

import random

import driver


class CrazyEight(object):
    """Contains methods for AI actions."""

    @staticmethod
    def move(partial_state):
        """Returns a move by the AI with partial knowledge."""

        pass

    @staticmethod
    def move_perfect_knowledge(state):
        """Returns a move by the AI with full knowledge."""

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
    """A collection of cards that a player is holding."""

    def __init__(self):
        self.__cards = []

    @property
    def cards(self):
        cards = tuple(self.__cards)
        return cards

    def add_card(self, card):
        """Adds the card to the hand."""

        self.__cards.append(card)

    def remove_card(self, card):
        """Removes the card from the hand."""

        self.__cards.remove(card)


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
        random.shuffle(self.__cards)

    @property
    def cards(self):
        cards = tuple(self.__cards)
        return cards

    def draw_card(self):
        """Removes and returns the card from the top."""

        top_card = self.__cards.pop()
        return top_card


class State(object):
    """Stores the deck, opponent's hand, and partial state."""

    def __init__(self):
        self.__deck = Deck()
        self.__hand = Hand()
        face_up_card = self.__deck.draw_card()
        self.__partial_state = PartialState(face_up_card)

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
        """Adds the move to the game's move history.  Swaps the next player into the partial state."""

        self.__partial_state.add_move(move)
        temp = self.__hand
        self.__hand = self.__partial_state.hand
        self.__partial_state.hand = temp


class PartialState(object):
    """Stores information available to the current player."""

    def __init__(self, face_up_card):
        self.__face_up_card = face_up_card
        self.__suit = face_up_card.suit
        self.__hand = Hand()
        self.__history = []

    @property
    def face_up_card(self):
        return self.__face_up_card

    @face_up_card.setter
    def face_up_card(self, value):
        self.__face_up_card = value

    @property
    def suit(self):
        return self.__suit

    @suit.setter
    def suit(self, value):
        self.__suit = value

    @property
    def hand(self):
        return self.__hand

    @hand.setter
    def hand(self, value):
        self.__hand = value

    def add_move(self, move):
        """Adds the move to the game's move history."""

        self.__history.append(move)


class Move(object):
    """An action taken by a player."""

    @staticmethod
    def from_tuple(tuple_source):
        """Return a new move from a tuple."""

        new_move = Move(tuple_source[0], tuple_source[1], tuple_source[2], tuple_source[3])
        return new_move

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


class HumanPlayer(object):
    @staticmethod
    def move(partial_state):
        return driver.move(partial_state)

    @staticmethod
    def move_perfect_knowledge(state):
        return driver.move(state.partial_state)


class AIPlayer(object):
    @staticmethod
    def move(partial_state):
        return CrazyEight.move(partial_state)

    @staticmethod
    def move_perfect_knowledge(state):
        return CrazyEight.move_perfect_knowledge(state)


def perform_move(state, move):
    # Move face-up card.
    state.partial_state.hand.remove_card(move.face_up_card)
    state.partial_state.face_up_card = move.face_up_card
    # Set suit.
    state.partial_state.suit = move.suit
    # Draw cards.
    for i in xrange(0, move.number_of_cards):
        drawn_card = state.deck.draw_card()
        state.partial_state.hand.add_card(drawn_card)
    # Add this move to history.
    state.next_turn(move)


def game_is_over(state):
    pass


def game_loop(state, current_player, next_player):
    perform_move(state, current_player.move(state.partial_state))
    # Loop while game is not over.  Switch players.
    if not game_is_over(state):
        game_loop(state, next_player, current_player)


def start_game():
    human_choice = driver.get_first_player()
    if human_choice == 1:
        player_1 = HumanPlayer
        player_2 = AIPlayer
    elif human_choice == 2:
        player_1 = AIPlayer
        player_2 = HumanPlayer
    else:
        return
    current_state = State()
    game_loop(current_state, player_1, player_2)


start_game()