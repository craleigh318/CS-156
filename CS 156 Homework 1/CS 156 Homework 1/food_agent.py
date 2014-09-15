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
        'manhattan': lambda p1, p2: abs(p1.x - p2.x) + abs(p1.y - p2.y),
        'euclidean': lambda p1, p2: sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2),
        'made_up': lambda p1, p2: sqrt(abs((p1.x - p2.x) * (p1.y - p2.y)))
    }
    heuristic_name = argv[2]
    if heuristic_name in heuristic_map:
        ascii_board_file_path = argv[1]
        heuristic = heuristic_map[heuristic_name]

        board_state_2 = \
            board_state_generator.generate_from_file(ascii_board_file_path)
        current_ai = FoodAgentAI(board_state_2, heuristic)

        current_ai.find_path()
        if current_ai.board_is_unsolvable:
            print('This board is unsolvable')
        else:
            # Make sure agent starts where it began from originally.
            board_state_2.reset_agent_position()
            # Ignore agent start position node.
            current_ai.movement_path_list.remove(None)
            print('Initial:')
            board_printer.print_board(board_state_2)

            solution_step_nums = xrange(len(current_ai.movement_path_list))
            for step_number in solution_step_nums:
                print('')
                step_direction = current_ai.movement_path_list[step_number]
                board_state_2.agent.move(step_direction)
                print('Step ' + str(step_number + 1) + ':')
                board_printer.print_board(board_state_2)
            print('Problem Solved! I had some noodles!')
    else:
        print_error('Invalid heuristic name "' + heuristic_name + '"')
else:
    print_error('You must enter two arguments.')
