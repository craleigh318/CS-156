__author__ = "Christopher Raleigh and Anthony Ferrero"

from sys import argv
from math import sqrt

from food_agent_ai import FoodAgentAI
import board_printer
import board_state_generator


def print_error(error_message):
    print('')
    print(error_message)
    print('')
    print('Usage: cs_156_homework_1.py [file name] [heuristic name]')
    print('\t[heuristic name] -> manhattan|euclidean|made_up')


NUM_SUPPORTED_PROGRAM_ARGS = 2
# Python passes in the name of the executed module as the first argument
NUM_EXPECTED_ARGS = NUM_SUPPORTED_PROGRAM_ARGS + 1
if len(argv) == NUM_EXPECTED_ARGS:
    heuristic_map = {
        'manhattan': lambda point_1, point_2: abs(point_1.x - point_2.x) + abs(point_1.y - point_2.y),
        'euclidean': lambda point_1, point_2: sqrt((point_1.x - point_2.x) ** 2 + (point_1.y - point_2.y) ** 2),
        'made_up': lambda not_used: 'NOT YET IMPLEMENTED'  # Can't have lambdas raise exceptions
    }
    heuristic_name = argv[2]
    if heuristic_name in heuristic_map:
        ascii_board_file_path = argv[1]
        heuristic = heuristic_map[heuristic_name]

        # Board will be printed until the agent eats its food.

        print('Initial:')
        board_state_2 = board_state_generator.generate_from_file(ascii_board_file_path)
        current_ai = FoodAgentAI(board_state_2, heuristic)
        board_printer.print_board(board_state_2)
        step_counter = 1
        current_ai.solution(None)

        # TODO this loop needs to be moved into a method in FoodAgentAI
        while not board_state_2.food_eaten():
            print('Step ' + str(step_counter) + ':')
            current_ai.on_food_agent_turn()
            if current_ai.board_is_unsolvable:
                print('This board is unsolvable.')
                break
            board_printer.print_board(board_state_2)
            step_counter += 1

    else:
        print_error('Invalid heuristic name "' + heuristic_name + '"')
else:
    print_error('You must enter two arguments.')
