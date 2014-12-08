import sys

import abstract_classes


__author__ = 'Christopher Raleigh and Anthony Ferrero'


class Grid(abstract_classes.Example):
    def __init__(self, matrix=(), classification=None):
        self.__matrix = matrix
        self.__classification = classification
        # self.__matrix = [[0 for i in range(Grid.__get_grid_length())]
        # for j in range(Grid.__get_grid_length())]

    @staticmethod
    def __get_grid_length():
        return 5

    @staticmethod
    def from_string_collection(collection):
        new_matrix = []
        for s in collection:
            new_list = s.split()
            new_matrix.append(new_list)
        # Separate classification
        new_classification = new_matrix.pop()
        new_grid = Grid(tuple(new_matrix), new_classification)
        return new_grid

    @property
    def matrix(self):
        return self.__matrix


    @property
    def classification(self):
        return self.__classification


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
    grid_data = file_to_string_collection(sys.argv[1])
    print_this = Grid.from_string_collection(grid_data)
    for row in print_this.matrix:
        print row
    print print_this.classification