__author__ = 'Christopher Raleigh and Anthony Ferrero'

import sys


def get_first_player():
    """Gets the first player. 0 is the human.  1 is the AI."""

    print ('Would you like to go first or second?')
    print ('[1] for first, [2] for second')
    str_input = sys.stdin.read()
    int_input = int(str_input)
    return int_input


def move(partial_state):
    """Gets a tuple from the player's input."""
    print("Enter input as a tuple:")
    str_input = sys.stdin.read()
    tpl_input = tuple(str_input)
    return tpl_input