__author__ = "Christopher Raleigh"

from BoardSquareType import BoardSquareType


def print_board(boardState):
    """Prints a board."""
    board = boardState.board
    agent = boardState.agent
    for j in xrange(board.height):
        row = ''
        for i in xrange(board.width):
            nextChar = None
            if (agent.x == i) and (agent.y == j):
                nextChar = '%'
            else:
                nextChar = board_square_type_to_char(board.squares[i][j])
            row += nextChar
        print(row)


def board_square_type_to_char(squareType):
    """Changes a square type to a readable character."""
    return {
        BoardSquareType.wall: '#',
        BoardSquareType.food: '@',
        }.get(squareType, '.')
