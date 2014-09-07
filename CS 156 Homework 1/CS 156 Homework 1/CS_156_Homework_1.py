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
board1.setSquare(0, 0, BoardSquareType.food)
board1.setSquare(3, 0, BoardSquareType.wall)
board1.setSquare(0, 1, BoardSquareType.wall)
board1.setSquare(3, 1, BoardSquareType.wall)
boardState1 = BoardState(board1, 2, 1)
BoardPrinter.printBoard(boardState1)

# Next board will be printed until the agent eats its food.

print('Initial:')
boardState2 = BoardStateGenerator.generateFromFile()
stepCounter = 1
while not boardState2.foodEaten():
    print('Step ' + stepCounter + ':')
    BoardPrinter.printBoard(boardState2)
    ++stepCounter
