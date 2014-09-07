__author__ = "Christopher Raleigh"

from BoardSquareType import BoardSquareType

def generateFromFile(file):
    """Returns a maze from an inputted file."""
    # TO DO: Someone needs to write this function.
def charToBoardSquareType(character):
    """Changes a square type to a readable character."""
    return {
        '#' : BoardSquareType.wall,
        '@' : BoardSquareType.food,
        }.get(character, BoardSquareType.empty)