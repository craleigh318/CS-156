__author__ = "Christopher Raleigh and Anthony Ferrero"

from board_square_type import BoardSquareType
from board import Board
from board_state import BoardState


def generate_from_file(ascii_board_file_path):
    """Returns a maze from an inputted file."""
    board = None
    board_state = None
    agent_x = None
    agent_y = None
    with open(ascii_board_file_path, 'r') as ascii_board_file:
        file_lines = ascii_board_file.readlines()
        board_width = len(file_lines[0])
        board_height = len(ascii_board_file.readlines())
        board = Board(width=board_width, height=board_height)
        for j in xrange(board_height):
            for i in xrange(board_width):
                next_char = file_lines[j][i]
                if next_char is '@':
                    agent_x = i
                    agent_y = j
                square_type = char_to_board_square_type(next_char)
                board.set_square(i, j, square_type)
    board_state = BoardState(board, agent_x, agent_y)
    return board_state


def char_to_board_square_type(character):
    """Changes a square type to a readable character."""
    return {
        '.': BoardSquareType.empty,
        '#': BoardSquareType.wall,
        '%': BoardSquareType.food,
    }.get(character, BoardSquareType.empty)
