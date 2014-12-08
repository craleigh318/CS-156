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
    def get_grid_length():
        return 5

    @staticmethod
    def from_string_collection(collection):
        new_matrix = []
        for s in collection:
            new_list = s.split()
            new_matrix.append(new_list)
        # Separate classification
        new_classification = new_matrix.pop()[0]
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
    return string_list


def pop_grid(collection):
    """
    Pops the last six elements of the specified collection
    :param collection: the collection to pop
    :return: a Grid object
    """
    lines_for_new_grid = []
    for x in xrange(Grid.get_grid_length() + 1):
        next_line = collection.pop()
        lines_for_new_grid.append(next_line)
    lines_for_new_grid.reverse()
    new_grid = Grid.from_string_collection(lines_for_new_grid)
    return new_grid


def train(training_file_name):
    return_string = ''
    with open(training_file_name) as training_file:
        file_lines = training_file.readlines()
        for line in file_lines:
            return_string += line
    return return_string


if __name__ == '__main__':
    grid_data = file_to_string_collection(sys.argv[1])
    # Loop until all grids in file are parsed.
    print_this = pop_grid(grid_data)
    for row in print_this.matrix:
        print row
    print 'Classification: ' + print_this.classification