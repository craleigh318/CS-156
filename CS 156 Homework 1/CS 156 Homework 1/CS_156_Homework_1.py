import BoardStateGenerator
__author__ = "Christopher Raleigh"

from Board import Board
from BoardSquareType import BoardSquareType
from BoardState import BoardState
import BoardPrinter
import BoardStateGenerator

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
boardState1 = BoardState(board1, 2, 1)
BoardPrinter.print_board(boardState1)

# Next board will be printed until the agent eats its food.

print('Initial:')
boardState2 = BoardStateGenerator.generate_from_file()
stepCounter = 1
while not boardState2.food_eaten():
    print('Step ' + stepCounter + ':')
    BoardPrinter.print_board(boardState2)
    ++stepCounter
