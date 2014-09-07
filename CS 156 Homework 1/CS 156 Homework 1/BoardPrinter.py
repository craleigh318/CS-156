__author__ = "Christopher Raleigh"

from BoardSquareType import BoardSquareType


def print_board(board_state):
    """Prints a board."""
    board = board_state.board
    agent = board_state.agent
    for j in xrange(board.height):
        row = ''
        for i in xrange(board.width):
            next_char = None
            if (agent.x == i) and (agent.y == j):
                next_char = '%'
            else:
                next_char = board_square_type_to_char(board.squares[i][j])
            row += next_char
        print(row)


def board_square_type_to_char(square_type):
    """Changes a square type to a readable character."""
    return {
        BoardSquareType.wall: '#',
        BoardSquareType.food: '@',
        }.get(square_type, '.')
