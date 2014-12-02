import sys

import abstract_classes
from algorithms import DecisionTree


__author__ = 'Christopher Raleigh and Anthony Ferrero'

abstract_classes.Tree.register(DecisionTree)


def train(training_file_name):
    return_string = ''
    with open(training_file_name) as training_file:
        file_lines = training_file.readlines()
        for line in file_lines:
            return_string += line
    return return_string


if __name__ == '__main__':
    print_this = train(sys.argv[1])
    print(print_this)