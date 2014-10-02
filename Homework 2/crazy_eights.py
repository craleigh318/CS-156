__author__ = 'Christopher Raleigh and Anthony Ferrero'

import random

import driver


class CrazyEight(object):
    """Contains methods for AI actions."""

    @staticmethod
    def move(partial_state):
        """Returns a move by the AI with partial knowledge."""
        partial_state_object = PartialState.from_tuple(partial_state)

    @staticmethod
    def move_perfect_knowledge(state):
        """Returns a move by the AI with full knowledge."""
        state_object = State.from_tuple(state)
        
    @staticmethod
    def __legal_moves(hand_cards, history):
        last_move = history[-1]
        current_player_num = last_move.player_num ^ 1
        draw_value = 0

        if last_move.face_up_card == Card.two:
            legal_moves = [Move(current_player_num, draw_value, draw_value, last_move.number_of_cards + 2)]
        elif last_move.face_up_card == Card.queen:
            legal_moves = [Move(current_player_num, draw_value, draw_value, 5)]
        else:
            # Find relevant move (i.e., move that contains rank and suit of the face-up card)
            relevant_move = last_move
            move_index = -2
            while relevant_move.number_of_cards > 0:
                relevant_move = history[move_index]
                move_index -= 1

            def legal_card(card):
                return card.rank == relevant_move.face_up_card or card.rank == relevant_move.suit
            legal_moves = [c for c in hand_cards if legal_card(c)]
            draw_move = Move(current_player_num, draw_value, draw_value, 1)
            legal_moves.push(draw_move)

        return legal_moves


class Card(object):
    """A playing card."""

    def __init__(self, deck_index):
        self.__deck_index = deck_index

    @property
    def deck_index(self):
        """The card's number in the deck, from 0 to 51."""
        return self.__deck_index

    @property
    def suit(self):
        """The card's suit, from 0 to 3."""
        suit = self.__deck_index / Deck.suit_size()
        return suit

    @property
    def rank(self):
        """The card's number in the suit, from 0 to 12."""
        rank = self.__deck_index % Deck.suit_size()
        return rank

    two = 1
    jack = 10
    queen = 11


class CardNames(object):
    """Suits and ranks of cards."""

    @staticmethod
    def full_name(card):
        """The full name of the card."""
        name = CardNames.rank(card.rank)
        name += ' of '
        name += CardNames.suit(card.suit)
        return name

    @staticmethod
    def suit(integer):
        """The name of the card's suit."""
        return {
            0: 'Spades',
            1: 'Hearts',
            2: 'Diamonds',
            3: 'Clubs'
        }.get(integer)

    @staticmethod
    def rank(integer):
        """The name of the card's rank."""
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
        """The number of cards with which a player starts."""
        return 8

    def __init__(self, initial_hand=[]):
        self.__cards = list(initial_hand)

    @property
    def cards(self):
        """A copy of the list of all of the cards in the hand."""
        cards = list(self.__cards)
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
    def deck_size():
        """The initial number of cards in a deck."""
        return 52

    @staticmethod
    def suit_size():
        """The number of cards in a suit."""
        return 13

    def __init__(self, initial_deck=None):
        if initial_deck is None:
            self.__cards = Deck.__shuffled_deck()
        else:
            self.__cards = list(initial_deck)

    @property
    def cards(self):
        """A copy of the list of the cards in the deck."""
        cards = list(self.__cards)
        return cards

    @staticmethod
    def __shuffled_deck():
        """Returns a filled and shuffled deck."""
        deck = []
        max_index = Deck.deck_size()
        for index in xrange(0, max_index):
            deck.append(Card(index))
        random.shuffle(deck)
        return deck

    def draw_card(self):
        """Removes and returns the card from the top."""
        top_card = self.__cards.pop()
        return top_card


class State(object):
    """Stores the deck, opponent's hand, and partial state."""

    def __init__(self, deck=Deck(), hand=Hand(), partial_state=None):
        self.__deck = deck
        self.__hand = hand
        if partial_state is None:
            self.__randomize_partial_state()
        else:
            self.__partial_state = partial_state

    @property
    def deck(self):
        """The current deck of cards."""
        return self.__deck

    @property
    def hand(self):
        """The hand of the inactive player."""
        return self.__hand

    @property
    def partial_state(self):
        """Information that the active player can access."""
        return self.__partial_state

    @staticmethod
    def from_tuple(tpl_param):
        """Return a new state from a tuple."""
        deck = Deck(tpl_param[0])
        hand = Hand()
        for num in tpl_param[1]:
            hand.add_card(Card(num))
        partial_state = PartialState.from_tuple(tpl_param[2])
        new_state = State(deck, hand, partial_state)
        return new_state

    def __randomize_partial_state(self):
        """Fills both hands and places a face-up card."""
        face_up_card = self.__deck.draw_card()
        self.__partial_state = PartialState(face_up_card)
        for i in xrange(0, Hand.initial_num_cards()):
            self.__hand.add_card(self.__deck.draw_card())
            self.__partial_state.hand.add_card(self.__deck.draw_card())

    def next_turn(self, move):
        """Adds the move to the game's move history.  Swaps the next player into the partial state."""
        self.__partial_state.add_move(move)
        temp = self.__hand
        self.__hand = self.__partial_state.hand
        self.__partial_state.hand = temp

    def game_ended(self):
        """Returns true if the game ended.  The game ends if the deck or either hand is empty."""
        ended = not (self.__deck.cards and self.__hand.cards and self.__partial_state.hand.cards)
        return ended


class PartialState(object):
    """Stores information available to the active player."""

    def __init__(self, face_up_card, suit=None, hand=Hand(), history=[]):
        self.__face_up_card = face_up_card
        if suit is None:
            self.__suit = face_up_card.suit
        else:
            self.__suit = suit
        self.__hand = hand
        self.__history = list(history)

    @property
    def face_up_card(self):
        """The card that the active player must follow."""
        return self.__face_up_card

    @face_up_card.setter
    def face_up_card(self, value):
        self.__face_up_card = value

    @property
    def suit(self):
        """The suit that the active player must match."""
        return self.__suit

    @suit.setter
    def suit(self, value):
        self.__suit = value

    @property
    def hand(self):
        """The hand of the active player."""
        return self.__hand

    @hand.setter
    def hand(self, value):
        self.__hand = value

    @property
    def history(self):
        """A copy of the list of moves made during this game."""
        history = list(self.__history)
        return history

    @staticmethod
    def from_tuple(tpl_param):
        """Return a new partial state from a tuple."""
        face_up_card = Card(tpl_param[0])
        suit = tpl_param[1]
        hand = Hand()
        for num in tpl_param[2]:
            hand.add_card(Card(num))
        history = []
        for move in tpl_param[3]:
            history.append(Move.from_tuple(move))
        new_partial_state = PartialState(face_up_card, suit, hand, history)
        return new_partial_state

    def add_move(self, move):
        """Adds the move to the game's move history."""
        self.__history.append(move)


class Move(object):
    """An action taken by a player."""

    @staticmethod
    def from_tuple(tpl_param):
        """Return a new move from a tuple."""
        new_move = Move(tpl_param[0], tpl_param[1], tpl_param[2], tpl_param[3])
        return new_move

    def __init__(self, player_num, face_up_card, suit, number_of_cards):
        self.__player_num = player_num
        self.__face_up_card = face_up_card
        self.__suit = suit
        self.__number_of_cards = number_of_cards

    @property
    def player_num(self):
        """Returns 0 if the human made this move.  Returns 1 if the AI did."""
        return self.__player_num

    @property
    def face_up_card(self):
        """The card that was placed face-up in this move."""
        return self.__face_up_card

    @property
    def suit(self):
        """The suit that must be matched in the next turn."""
        return self.__suit

    @property
    def number_of_cards(self):
        """The number of cards that the active player drew in this turn."""
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
    # Draw cards.
    for i in xrange(0, move.number_of_cards):
        drawn_card = state.deck.draw_card()
        state.partial_state.hand.add_card(drawn_card)
    # Move face-up card.
    state.partial_state.hand.remove_card(move.face_up_card)
    state.partial_state.face_up_card = move.face_up_card
    # Set suit.
    state.partial_state.suit = move.suit
    # Add this move to history.
    state.next_turn(move)


def game_loop(state, current_player, next_player):
    """Cycles through player turns until the game is over."""
    player_move = current_player.move(state.partial_state)
    perform_move(state, player_move)
    # Loop while game is not over.  Switch players.
    if not state.game_ended():
        game_loop(state, next_player, current_player)


def start_game():
    """Initializes game objects."""
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


if __name__ == '__main__':
    start_game()