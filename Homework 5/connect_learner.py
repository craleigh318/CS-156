import sys
import random

import abstract_classes


__author__ = 'Christopher Raleigh and Anthony Ferrero'


class Grid(abstract_classes.Example):
    def __init__(self, matrix=None, classification=None):
        if matrix:
            self.__matrix = matrix
        else:
            self.__matrix = ()
        self.__classification = classification

    @staticmethod
    def get_matrix_length():
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

    @staticmethod
    def random():
        """Generates a random grid."""

        def random_row():
            random_bit_row = tuple(random.randrange(0, 2) for _ in xrange(Grid.get_matrix_length()))
            grid_values = ['X', 'O']
            return tuple(map(lambda bit: grid_values[bit], random_bit_row))

        return Grid(tuple(random_row() for _ in xrange(Grid.get_matrix_length())))

    @property
    def matrix(self):
        return self.__matrix

    @property
    def classification(self):
        return self.__classification


def file_to_string_collection(opened_file):
    string_list = []
    file_lines = opened_file.readlines()
    for line in file_lines:
        string_list.append(line)
    return string_list


def pop_grid(collection):
    """
    Pops the first six elements of the specified collection.

    :param collection: the collection to pop
    :return: a Grid object
    """
    # Exit if not enough lines for grid.
    if len(collection) <= Grid.get_matrix_length():
        return None
    new_grid = Grid.from_string_collection(collection)
    return new_grid


def append_to_grid_list(grid_list, lines_for_next_grid):
    """
    Appends the next grid to the list, if possible.

    :param grid_list: the grid list
    :param lines_for_next_grid: the lines for a new grid
    """
    next_grid = pop_grid(lines_for_next_grid)
    if next_grid is not None:
        grid_list.append(next_grid)


def file_to_grids(opened_file):
    """
    Creates Grid objects from an opened file.

    :param opened_file: the opened file
    :return: a list of Grids
    """
    grid_list = []
    file_lines = opened_file.readlines()
    # Loop to parse all grids in file.
    lines_for_next_grid = []
    for line in file_lines:
        if line == '\n':
            append_to_grid_list(grid_list, lines_for_next_grid)
            lines_for_next_grid = []
        else:
            lines_for_next_grid.append(line)
    append_to_grid_list(grid_list, lines_for_next_grid)
    return grid_list


def train(training_file_name):
    return_string = ''
    with open(training_file_name) as training_file:
        file_lines = training_file.readlines()
        for line in file_lines:
            return_string += line
    return return_string


def random_training_set(min_size=5, max_size=5000):
    random_size = random.randrange(min_size, max_size + 1)
    return tuple(Grid.random() for _ in xrange(random_size))


def main():
    file_name = sys.argv[1]
    with open(file_name) as opened_file:
        print_these = file_to_grids(opened_file)
        for grid in print_these:
            for row in grid.matrix:
                print row
            print grid.classification


if __name__ == '__main__':
    main()
