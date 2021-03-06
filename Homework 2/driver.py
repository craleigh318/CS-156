__author__ = 'Christopher Raleigh and Anthony Ferrero'

"""
Acts as the main module and contains all code related to simulating the game of Crazy Eights and interacting with
both the human and AI players.
"""

from crazy_eights import *


class Player(object):
    def __init__(self, number):
        self.__number = number

    @property
    def number(self):
        return self.__number


class HumanPlayer(Player):

    @staticmethod
    def __list_actions():
        """Lists possible actions for human to take."""
        print('Available actions:')
        print('[play #]: Place the card face-up.  # is the card number.')
        print('[draw]: Draw a card from the deck.')
        print('[suit #]: Declare a new suit after playing an 8.  # is the suit number')
        # print('[end]: End your turn.')

    def __init__(self, number):
        super(HumanPlayer, self).__init__(number)

    def move(self, partial_state):
        """Asks the player to choose a move."""
        print_partial_state(partial_state)
        self.__list_actions()
        return self.__choose_move(partial_state)

    @staticmethod
    def __choose_move(partial_state):
        legal_moves = partial_state.legal_moves(partial_state.hand)
        while True:
            str_input = raw_input()
            user_input = str_input.split()

            chosen_command = user_input[0]
            chosen_card = Card(int(user_input[1]))
            if chosen_command == 'draw':
                chosen_move = partial_state.last_move.next_draw(partial_state.face_up_card.rank)
            elif chosen_command == 'play':
                if chosen_card.rank == Card.rank_eight:
                    print('You have played an eight card! Please choose a suit number from the following list:')
                    for suit_num, suit_name in CardNames.suit_name_map.items():
                        print('[' + str(suit_num) + ']: ' + suit_name)
                    suit_input = raw_input()
                    suit_num = int(suit_input)
                    chosen_card = Card(Card.make_deck_index(Card.rank_eight, suit_num))
                chosen_move = partial_state.last_move().next_play(chosen_card)

            if chosen_move in legal_moves:
                return chosen_move
            else:
                print('You cannot place a [' + CardNames.full_name(chosen_move.face_up_card) +
                      '] on top of a [' + CardNames.full_name(partial_state.face_up_card) + ']')


class AIPlayer(Player):
    @staticmethod
    def move(partial_state):
        return Move.from_tuple(CrazyEight.move(partial_state.to_tuple()))


def print_partial_state(partial_state):
    """Prints, in console, the face-up card and the player's cards."""
    print('Face-up card:')
    print(CardNames.full_name_and_deck_value(partial_state.face_up_card))
    print('')
    print('Cards in hand:')
    for card in partial_state.hand.cards:
        print(CardNames.full_name_and_deck_value(card))
    print('')


def game_loop(state, current_player, next_player):
    """Cycles through player turns until the game is over."""

    player_move = current_player.move(state.partial_state)

    state.partial_state.next_turn(state.deck, state.partial_state.hand, player_move)
    # Loop while game is not over.  Switch players.
    if not state.game_ended():
        # If a jack was played, the player who played it gets to go again.
        if player_move.face_up_card.rank == Card.rank_jack:
            game_loop(state, current_player, next_player)
        else:
            game_loop(state, next_player, current_player)


def choose_human_player_number():
    print('Would you like to go first or second?')
    print('[0] for first, [1] for second')
    while True:
        str_input = raw_input()
        int_input = int(str_input)
        if int_input != 0 and int_input != 1:
            print('ERROR: You must choose either 0 or 1.')
        else:
            return int_input


def start_game():
    """Initializes game objects."""
    chosen_player_number = choose_human_player_number()
    human_player = HumanPlayer(chosen_player_number)
    ai_player = AIPlayer(chosen_player_number ^ 1)

    if chosen_player_number == 0:
        first_player, second_player = human_player, ai_player
    else:
        first_player, second_player = ai_player, human_player

    current_state = State()
    game_loop(current_state, first_player, second_player)


if __name__ == '__main__':
    start_game()