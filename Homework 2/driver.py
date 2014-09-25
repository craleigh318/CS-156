__author__ = 'Christopher Raleigh and Anthony Ferrero'

import sys

import crazy_eights


def ask_human():
    print ('Would you like to go first or second?')
    print ('[1] for first, [2] for second')
    str_input = sys.stdin.read()
    human_turn = int(str_input) - 1
    new_player_list = crazy_eights.PlayerList(human_turn)
    return new_player_list