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
        self.__is_connected = classification

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
        new_classification = classification_to_is_connected(new_classification)
        new_grid = Grid(tuple(new_matrix), new_classification)
        return new_grid

    @staticmethod
    def random():
        """Generates a random grid."""

        def random_row():
            random_bit_row = tuple(random.randrange(0, 2) for _ in xrange(Grid.get_matrix_length()))
            grid_values = ['X', 'O']
            return tuple(map(lambda bit: grid_values[bit], random_bit_row))

        random_matrix = tuple(random_row() for _ in xrange(Grid.get_matrix_length()))

        # Label the random matrix

        # Because 'break' doesn't break out of the outer loop. This is the cleanest way to do so.
        def find_first_o_coords():
            for x in xrange(Grid.get_matrix_length()):
                for y in xrange(Grid.get_matrix_length()):
                    if random_matrix[x][y] == 'O':
                        return x, y
        first_o_coords = find_first_o_coords()

        def adjacent_coords(coords):
            x, y = coords
            adjacents = []
            lowest_legal_coord = 0
            highest_legal_coord = Grid.get_matrix_length() - 1

            if x > lowest_legal_coord:
                adjacents.append((x - 1, y))
            if x < highest_legal_coord:
                adjacents.append((x + 1, y))

            # Yes, duplication. But it's not worth it to get rid of. Trust me.
            if y > lowest_legal_coord:
                adjacents.append((x, y - 1))
            if y < highest_legal_coord:
                adjacents.append((x, y + 1))

            return adjacents

        # WARNING: first_o_coords might not be initialized yet!
        if first_o_coords is not None:
            adjacent_o_coordinates = [first_o_coords]
            frontier_coords = [first_o_coords]
            while len(frontier_coords) > 0:
                new_frontier_coords = []
                for component_coords in frontier_coords:
                    for adj_coords in adjacent_coords(component_coords):
                        if adj_coords not in adjacent_o_coordinates:
                            x, y = adj_coords
                            if random_matrix[x][y] == 'O':
                                adjacent_o_coordinates.append(adj_coords)
                                new_frontier_coords.append(adj_coords)
                frontier_coords = new_frontier_coords

            flattened_matrix = flatten(random_matrix)
            o_count = len([grid_value for grid_value in flattened_matrix if grid_value == 'O'])
            connected = o_count == len(adjacent_o_coordinates)
        else:
            connected = False

        return Grid(random_matrix, connected)

    @property
    def matrix(self):
        return self.__matrix

    @property
    def is_connected(self):
        return self.__is_connected

    @property
    def input(self):
        return self.matrix

    @property
    def weight(self):
        if self.is_connected:
            return 1
        else:
            return -1

    def __str__(self):
        grid_str = ''

        for row in self.matrix:
            grid_str += ' '.join(row)
            grid_str += '\n'

        grid_str += is_connected_to_classification(self.is_connected)

        return grid_str


def classification_to_is_connected(classification):
    """
    Converts a connection classification to a boolean.

    :param classification: 'CONNECTED' or 'DISCONNECTED'
    :return: true if 'CONNECTED'
    """
    if classification == 'CONNECTED':
        return True
    elif classification == 'DISCONNECTED':
        return False
    else:
        return None


def is_connected_to_classification(is_connected):
    """
    Converts a boolean to a connection classification.

    :param is_connected: a boolean
    :return: 'CONNECTED' if true, 'DISCONNECTED' if false
    """
    if is_connected:
        return 'CONNECTED'
    else:
        return 'DISCONNECTED'


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


def random_data_set(min_size=5, max_size=5000):
    random_size = random.randrange(min_size, max_size + 1)
    return tuple(Grid.random() for _ in xrange(random_size))


def flatten(iterable):
    return [item for subiterable in iterable for item in subiterable]


def main():
    file_name = sys.argv[1]
    with open(file_name) as opened_file:
        print_these = file_to_grids(opened_file)
        for grid in print_these:
            print(str(grid) + '\n')


if __name__ == '__main__':
    main()
