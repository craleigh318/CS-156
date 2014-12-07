import sys

import abstract_classes


__author__ = 'Christopher Raleigh and Anthony Ferrero'


class Grid(abstract_classes.Example):
    def __init__(self):
        self.__matrix = [[0 for i in range(Grid.__get_grid_length())]
                         for j in range(Grid.__get_grid_length())]

    @staticmethod
    def __get_grid_length():
        return 5

    @staticmethod
    def from_string_collection(collection):
        new_grid = Grid()
        # Assign each number to the grid.


def file_to_string_collection(file_name):
    string_list = []
    with open(file_name) as file:
        file_lines = file.readlines()
        for line in file_lines:
            string_list.append(line)
    string_tuple = tuple(string_list)
    return string_tuple


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