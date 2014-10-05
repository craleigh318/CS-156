import driver

__author__ = 'Christopher Raleigh and Anthony Ferrero'

import copy
import random
from collections import Counter

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
        return state_object.best_move()


class Card(object):
    """A playing card."""

    rank_two = 1
    rank_eight = 8
    rank_jack = 10
    rank_queen = 11

    @staticmethod
    def deck_index(rank, suit):
        suit_placement = suit * Card.suit_size()
        return suit_placement + rank

    @staticmethod
    def num_suits():
        """The number of suits a card can have."""
        return 4

    @staticmethod
    def suit_size():
        """The number of cards in a suit."""
        return 13

    def __init__(self, deck_index):
        self.__deck_index = deck_index

    @property
    def deck_index(self):
        """The card's number in the deck, from 0 to 51."""
        return self.__deck_index

    @property
    def suit(self):
        """The card's suit, from 0 to 3."""
        suit = self.__deck_index / Card.suit_size()
        return suit

    @property
    def rank(self):
        """The card's number in the suit, from 0 to 12."""
        rank = self.__deck_index % Card.suit_size()
        return rank


class CardNames(object):
    """Suits and ranks of cards."""

    @staticmethod
    def full_name_and_deck_value(card):
        """The full name of the card, plus the deck index."""
        name = CardNames.full_name(card)
        name += ' (#'
        name += str(card.deck_index)
        name += ')'
        return name

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

    def __len__(self):
        return len(self.cards)

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
    def max_deck_size():
        """The initial number of cards in a deck."""
        return 52

    @staticmethod
    def __shuffled_deck():
        """Returns a filled and shuffled deck."""
        deck = []
        for index in xrange(0, Deck.max_deck_size()):
            deck.append(Card(index))
        random.shuffle(deck)
        return deck

    def __init__(self, initial_deck=None):
        if initial_deck is None:
            self.__cards = Deck.__shuffled_deck()
        else:
            self.__cards = list(initial_deck)

    def __len__(self):
        return len(self.__cards)

    @property
    def cards(self):
        """A copy of the list of the cards in the deck."""
        cards = list(self.__cards)
        return cards

    def draw_card(self):
        """Removes and returns the card from the top."""
        top_card = self.__cards.pop()
        return top_card


class State(object):
    """Stores the deck, opponent's hand, and partial state."""

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

    def __move_result(self, player_hand, move):
        """Returns the State that results from making a move."""
        self_copy = copy.deepcopy(self)
        player_hand_copy = copy.deepcopy(player_hand)

        if move.is_card_draw:
            for ind in xrange(0, move.number_of_cards):
                player_hand_copy.add_card(self_copy.deck.draw_card())
        else:
            # All 8 cards are treated equally by the rules of Crazy Eights, so if we're playing an 8 then we just
            # look for one in our hand and play it rather than trying to play any particular one.
            if move.face_up_card == Card.rank_eight:
                played_card = next(card for card in player_hand_copy.cards if card.rank == Card.rank_eight)
            else:
                move_card_deck_index = Card.deck_index(move.face_up_card, move.suit)
                played_card = Card(move_card_deck_index)
            player_hand_copy.remove_card(played_card)

        self_copy.partial_state.history.append(move)
        return self_copy, player_hand_copy

    def __min_move_result(self, move):
        result_state, result_hand = self.__move_result(self.partial_state.hand, move)
        result_state.partial_state.hand = result_hand
        return result_state

    def __max_move_result(self, move):
        result_state, result_hand = self.__move_result(self.hand, move)
        result_state.__hand = result_hand
        return result_state

    def __legal_moves(self, player_hand):
        """Return a list of Moves that can be performed by the AI in this state."""

        last_card_play = self.partial_state.last_card_play()
        # We need only consider if a single eight is in the AI's hand, since all 4 eights are considered
        # to be the same from the perspective of the game's rules.
        eight_in_hand = any((card.rank == Card.rank_eight) for card in self.__hand.cards)
        if eight_in_hand:
            legal_moves = [last_card_play.next_play(Card.rank_eight, suit) for suit in xrange(0, Card.num_suits())]
        hand_no_eights = [card for card in player_hand.cards if card.rank != Card.rank_eight]
        legal_moves += \
            [last_card_play.next_play(card.rank, card.suit)
             for card in hand_no_eights if last_card_play.can_precede(card)]

        return legal_moves

    def __evaluation(self):
        num_of_legal_moves = len(self.__legal_moves(self.hand))
        weight_of_legal_move = 1.25
        evaluation = num_of_legal_moves * weight_of_legal_move

        last_card_play = self.partial_state.last_card_play
        last_played_card = Card(Card.deck_index(last_card_play.face_up_card, last_card_play.suit))

        def next_play_weight(card):
            suit_weight = 0
            rank_weight = 0
            # It's less likely that the face up card will remain the same rank as the game continues than it is likely
            # that it will remain the same suit.
            if card.suit == last_played_card.suit:
                suit_weight = 2
            if card.rank == last_played_card.rank:
                rank_weight = 0.5
            return suit_weight + rank_weight

        def count_card_ranks(cards):
            return Counter([card.rank for card in cards])
        our_cards = self.hand.cards
        enemy_cards = self.partial_state.hand.cards
        enemy_hand_rank_counts = count_card_ranks(enemy_cards)
        our_hand_rank_counts = count_card_ranks(our_cards)

        def card_rank_weight(rank):
            if rank == Card.two:
                # These weights will be counted twice, so their true contribution is weight * 2
                if our_hand_rank_counts[rank] > enemy_hand_rank_counts[rank]:
                    return 1.5
                else:
                    return -1.5
            elif rank == Card.eight:
                # These weights will be counted twice, so their true contribution is weight * 2
                if our_hand_rank_counts[rank] > enemy_hand_rank_counts[rank]:
                    return 1.5
                else:
                    return 1.5
            elif rank == Card.rank_queen:
                return 4
            elif rank == Card.rank_jack:
                return 2
            else:
                return 1

        def total_card_weight(card):
            return next_play_weight(card) + card_rank_weight(card.rank)

        def hand_value(cards):
            return sum([total_card_weight(card) for card in cards])

        evaluation += hand_value(our_cards) - hand_value(enemy_cards)
        return evaluation

    def __max_value(self, alpha, beta, depth_counter):
        if self.game_ended() or depth_counter == 0:
            return self.__evaluation(), None
        else:
            wanted_value = float("-inf")
            for move in self.__legal_moves(self.hand):
                min_value = self.__max_move_result().__min_value(alpha, beta)
                if min_value >= wanted_value:
                    wanted_value = min_value
                    wanted_move = move
                if wanted_value >= beta:
                    return wanted_value, None
                alpha = max(alpha, wanted_value)

            return wanted_value, wanted_move

    def __min_value(self, alpha, beta, depth_counter):
        if self.game_ended() or depth_counter == 0:
            return self.__evaluation()
        else:
            wanted_value = float("inf")
            for move in self.__legal_moves(self.partial_state.hand):
                max_value, _ = self.__min_move_result(move).__max_value(alpha, beta)
                wanted_value = min(wanted_value, max_value)
                if wanted_value <= alpha:
                    return wanted_value
                beta = min(beta, wanted_value)

            return wanted_value

    def best_move(self):
        max_depth = 10  # TODO mess with this value, or find a better way to find a cutoff point
        _, best_move = self.__max_value(float("-inf"), float("inf"), max_depth)
        return best_move


class PartialState(object):
    """Stores information available to the active player."""

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

    def add_move(self, move):
        """Adds the move to the game's move history."""
        self.__history.append(move)

    def last_card_play(self):
        last_non_draw_ind = -1
        # We assume that the human player goes first, so there is always a move in the move-history list.
        while self.__history[last_non_draw_ind].is_card_draw:
            last_non_draw_ind -= 1
        last_card_play = self.__history[last_non_draw_ind]
        return last_card_play


class Move(object):
    """An action taken by a player."""

    @staticmethod
    def from_tuple(tpl_param):
        """Return a new move from a tuple."""
        new_move = Move(tpl_param[0], tpl_param[1], tpl_param[2], tpl_param[3])
        return new_move

    @staticmethod
    def draw(player_num, number_of_cards):
        """Return a Move representing a card-draw."""
        draw_placeholder = 0
        return Move(player_num, draw_placeholder, draw_placeholder, number_of_cards)

    @staticmethod
    def play(player_num, face_up_card, suit):
        """Return a Move representing a card-play."""
        return Move(player_num, face_up_card, suit, 0)

    def __init__(self, player_num, face_up_card, suit, number_of_cards):
        self.__player_num = player_num
        self.__face_up_card = face_up_card
        self.__suit = suit
        self.__number_of_cards = number_of_cards

    def next_draw(self):
        """Return a new Move representing a card-draw performed immediately after the current Move."""
        if self.__face_up_card == Card.rank_two:
            num_of_cards_to_draw = 2
        elif self.__face_up_card == Card.rank_queen:
            num_of_cards_to_draw = 5
        else:
            num_of_cards_to_draw = 1
        return Move.draw(self.__next_player_num(), num_of_cards_to_draw)

    def next_play(self, face_up_card, suit):
        """Return a new Move representing a card-play performed immediately after the current Move."""
        return Move.play(self.__next_player_num(), face_up_card, suit)

    def __next_player_num(self):
        """Return the ID number (0 or 1) of the player who is to make a move after this Move."""
        return self.__player_num ^ 1

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

    @property
    def is_card_draw(self):
        """Return True if this Move represents a card-draw, otherwise return False."""
        return self.__number_of_cards > 0

    @property
    def can_precede(self, next_move_card_candidate):
        """Return True if next_move_card_candidate can be played after this Move, otherwise return False."""
        if next_move_card_candidate.rank == Card.rank_eight:
            value = True
        elif self.__face_up_card == next_move_card_candidate.rank:
            value = True
        elif self.__face_up_card == Card.rank_two:
            value = False
        elif self.__suit == next_move_card_candidate.suit:
            value = True
        else:
            value = False
        return value


if __name__ == '__main__':
    driver.start_game()