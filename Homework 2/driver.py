__author__ = 'Christopher Raleigh and Anthony Ferrero'

import sys


def get_first_player():
    """Gets the first player. 0 is the human.  1 is the AI."""

    print ('Would you like to go first or second?')
    print ('[1] for first, [2] for second')
    str_input = sys.stdin.read()
    int_input = int(str_input)
    first_player = int_input - 1
    return first_player