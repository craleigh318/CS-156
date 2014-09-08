__author__ = "Christopher Raleigh"

from board_square_type import BoardSquareType


def generate_from_file(file):
    """Returns a maze from an inputted file."""
    # TO DO: Someone needs to write this function.


def char_to_board_square_type(character):
    """Changes a square type to a readable character."""
    return {
        '#': BoardSquareType.wall,
        '@': BoardSquareType.food,
        }.get(character, BoardSquareType.empty)
