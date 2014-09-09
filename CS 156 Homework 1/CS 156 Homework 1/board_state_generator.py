__author__ = "Christopher Raleigh"

from board_square_type import BoardSquareType
from board import Board


def generate_from_file(ascii_board_file_path):
    """Returns a maze from an inputted file."""
    board = None
    with open(ascii_board_file_path, 'r') as ascii_board_file:
        file_lines = ascii_board_file.readlines()
        board_width = len(file_lines[0])
        board_height = len(ascii_board_file.readlines())
        board = Board(width=board_width, height=board_height)

        for y in xrange(board_width):
            square_types = [char_to_board_square_type(c) for c in file_lines[y]]
            for x in xrange(board_width):
                board.square(x, y, square_types[x])
    return board


def char_to_board_square_type(character):
    """Changes a square type to a readable character."""
    return {
        '.': BoardSquareType.empty,
        '#': BoardSquareType.wall,
        '@': BoardSquareType.food,
    }.get(character, BoardSquareType.empty)
