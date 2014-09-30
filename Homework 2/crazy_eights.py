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
        suit = self.__deck_index / Deck.suit_size()
        return suit

    @property
    def rank(self):
        rank = self.__deck_index % Deck.suit_size()
        return rank


class CardNames(object):
    """Suits and ranks of cards."""

    @staticmethod
    def full_name(card):
        name = CardNames.rank(card.rank)
        name += ' of '
        name += CardNames.suit(card.suit)

        return name

    @staticmethod
    def suit(integer):
        return {
            0: 'Spades',
            1: 'Hearts',
            2: 'Diamonds',
            3: 'Clubs'
        }.get(integer)

    @staticmethod
    def rank(integer):
        return {
            0: 'Ace',
            1: 'Two',
            2: 'Three',
            3: 'Four',
            4: 'Five',
            5: 'Six',
            6: 'Seven',
            7: 'Eight',
            8: 'Nine',
            9: 'Ten',
            10: 'Jack',
            11: 'Queen',
            12: 'King'
        }.get(integer)


class Hand(object):
    """A collection of cards that a player is holding."""

    @staticmethod
    def initial_num_cards():
        return 8

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
    def suit_size():
        return 13

    def __init__(self):
        self.__cards = []
        max_index = Deck.num_cards()
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
        for i in xrange(0, Hand.initial_num_cards()):
            self.__hand.add_card(self.__deck.draw_card())
            self.__partial_state.hand.add_card(self.__deck.draw_card())

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
    player_move = current_player.move(state.partial_state)
    perform_move(state, player_move)
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


def test_method():
    state = State()
    print('Face-up card:')
    print(state.partial_state.face_up_card.deck_index)
    print('Cards in hand:')
    for card in state.hand.cards:
        print(CardNames.full_name(card))
        # perform_move(state, Move.from_tuple((1, 7, 0, 0)))


test_method()
# start_game()