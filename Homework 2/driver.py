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
        number_of_cards = 0
        move = (0, partial_state[0], partial_state[1], number_of_cards)
        move = list_actions(move)
        return move


class AIPlayer(object):
    @staticmethod
    def move(partial_state):
        return CrazyEight.move(partial_state)


def print_partial_state(partial_state):
    """Prints, in console, the face-up card and the player's cards."""
    print('Face-up card:')
    print(CardNames.full_name_and_deck_value(Card(Card.make_deck_index(partial_state[0], partial_state[1]))))
    print('')
    print('Cards in hand:')
    for card in partial_state[2]:
        print(CardNames.full_name_and_deck_value(Card(card)))
    print('')


def list_actions(move):
    """Lists possible actions for human to take."""
    print('Available actions:')
    print('[play #]: Place the card face-up.  # is the card number.')
    print('[draw]: Draw a card from the deck.')
    print('[suit #]: Declare a new suit after playing an 8.  # is the suit number')
    # print('[end]: End your turn.')
    str_input = raw_input()
    args = str_input.split()
    player_num = move[0]
    face_up_card = move[1]
    suit = move[2]
    number_of_cards = move[3]
    if args[0] == 'draw':
        number_of_cards += 1
    elif args[0] == 'play':
        face_up_card = int(args[1])
    elif args[0] == 'suit':
        suit = int(args[1])
    new_move = Move(player_num, Card(Card.make_deck_index(face_up_card, suit)), number_of_cards)
    return new_move


def perform_move(state, move):
    # Draw cards.
    for i in xrange(0, move.number_of_cards):
        drawn_card = state.deck.draw_card()
        state.partial_state.hand.add_card(drawn_card)
    # Move face-up card.
    state.partial_state.hand.remove_card(move.face_up_card)
    state.partial_state.face_up_card = move.face_up_card
    # Add this move to history.
    state.next_turn(move)


def game_loop(state, current_player, next_player):
    """Cycles through player turns until the game is over."""
    player_move = current_player.move(state.partial_state.to_tuple())
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