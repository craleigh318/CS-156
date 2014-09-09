__author__ = "Christopher Raleigh and Anthony Ferrero"

from board import Board
from board_square_type import BoardSquareType
from board_state import BoardState
import board_printer
import board_state_generator
from sys import argv


def print_error(error_message):
    print('')
    print(error_message)
    print('')
    print('Usage: cs_156_homework_1.py [file name] [heuristic name]')
    print('\t[heuristic name] -> manhattan|euclidean|made_up')

NUM_SUPPORTED_PROGRAM_ARGS = 2
# Python passes in the name of the executed module as the first argument
EXPECTED_ARG_NUM = NUM_SUPPORTED_PROGRAM_ARGS + 1
if len(argv) == EXPECTED_ARG_NUM:
    heuristic_name = argv[2]
    # Might want to replace this with a mapping from heuristic name to lambda.
    heuristic_name_is_valid = \
        heuristic_name == 'manhattan' or \
        heuristic_name == 'euclidean' or \
        heuristic_name == 'made_up'
    if heuristic_name_is_valid:
        ascii_board_file_path = argv[1]
        # TODO create lambdas for heuristic function and parse ascii board file

        print('Initial:')
        print('@..#')
        print('#.%#')
        print('')
        print('For real:')

        board_1 = Board(4, 2)
        board_1.square(0, 0, BoardSquareType.food)
        board_1.square(3, 0, BoardSquareType.wall)
        board_1.square(0, 1, BoardSquareType.wall)
        board_1.square(3, 1, BoardSquareType.wall)
        board_state_1 = BoardState(board_1, 2, 1)
        board_printer.print_board(board_state_1)

        # Next board will be printed until the agent eats its food.

        print('Initial:')
        board_state_2 = board_state_generator.generate_from_file(ascii_board_file_path)
        step_counter = 1
        while not board_state_2.food_eaten():
            print('Step ' + step_counter + ':')
            board_printer.print_board(board_state_2)
            ++step_counter
    else:
        print_error('Invalid heuristic name "' + heuristic_name + '"')
else:
    print_error('You must enter two arguments.')
