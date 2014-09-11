__author__ = "Christopher Raleigh and Anthony Ferrero"


class BoardSquare(object):
    """Represents an object in a space of a board."""

    # Using a strange name here because "type" is a built-in identifier
    def __init__(self, typ):
        self.type = typ
