__author__ = 'Christopher Raleigh and Anthony Ferrero'

"""
Acts as the main module and contains all code related to simulating the game of Crazy Eights and interacting with
both the human and AI players.
"""

from crazy_eights import *


class HumanPlayer(object):
    @staticmethod
    def move(partial_state):
        """Gets a tuple from the player's input."""
        print_partial_state(partial_state)
        # Get user input.
        print("Enter input as a tuple:")
        str_input = raw_input()
        tpl_input = tuple(str_input)
        return tpl_input

    @staticmethod
    def move_perfect_knowledge(state):
        return HumanPlayer.move(state.partial_state)


class AIPlayer(object):
    @staticmethod
    def move(partial_state):
        return CrazyEight.move(partial_state)

    @staticmethod
    def move_perfect_knowledge(state):
        return CrazyEight.move_perfect_knowledge(state)


def print_partial_state(partial_state):
    """Prints, in console, the face-up card and the player's cards."""
    print('Face-up card:')
    print(CardNames.full_name_and_deck_value(partial_state.face_up_card))
    print('')
    print('Cards in hand:')
    for card in partial_state.hand.cards:
        print(CardNames.full_name_and_deck_value(card))
    print('')


def list_actions(partial_state):
    """Lists possible actions for human to take."""
    pass


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


def get_first_player():
    """Gets the first player. 0 is the human.  1 is the AI."""
    print ('Would you like to go first or second?')
    print ('[1] for first, [2] for second')
    str_input = raw_input()
    int_input = int(str_input)
    return int_input


def start_game():
    """Initializes game objects."""
    human_choice = get_first_player()
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