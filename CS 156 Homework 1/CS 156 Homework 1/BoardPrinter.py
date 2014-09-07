__author__ = "Christopher Raleigh"

from BoardSquareType import BoardSquareType


def printBoard(boardState):
    """Prints a board."""
    board = boardState.board
    agent = boardState.agent
    for j in xrange(board.height):
        row = ''
        for i in xrange(board.width):
            if (agent.x == i) and (agent.y == j):
                nextChar = '%'
            else:
                nextChar = boardSquareTypeToChar(board.squares[i][j])
            row += nextChar
        print(row)


def boardSquareTypeToChar(squareType):
    """Changes a square type to a readable character."""
    return {
        BoardSquareType.wall: '#',
        BoardSquareType.food: '@',
        }.get(squareType, '.')
