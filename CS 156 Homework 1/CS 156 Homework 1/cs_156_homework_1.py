import board_state_generator
__author__ = "Christopher Raleigh"

from board import Board
from board_square_type import BoardSquareType
from board_state import BoardState
import board_printer
import board_state_generator

print('Initial:')
print('@..#')
print('#.%#')
print('')
print('For real:')

board1 = Board(4, 2)
board1.set_square(0, 0, BoardSquareType.food)
board1.set_square(3, 0, BoardSquareType.wall)
board1.set_square(0, 1, BoardSquareType.wall)
board1.set_square(3, 1, BoardSquareType.wall)
board_state_1 = BoardState(board1, 2, 1)
board_printer.print_board(board_state_1)

# Next board will be printed until the agent eats its food.

print('Initial:')
board_state_2 = board_state_generator.generate_from_file()
step_counter = 1
while not board_state_2.food_eaten():
    print('Step ' + step_counter + ':')
    board_printer.print_board(board_state_2)
    ++step_counter
