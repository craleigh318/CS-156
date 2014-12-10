import sys
import random

import abstract_classes
import algorithms


__author__ = 'Christopher Raleigh and Anthony Ferrero'


class Evaluator(object):
    # TODO currently biased towards making very random disconnected grids, but not so random
    # connected ones; the occupied squares in a connected grid tend to be more clumped together
    # than is ideal, whereas the disconnected matrices tend to have squares all over.
    @staticmethod
    def random_grid(probability_of_connected=0.5):
        """

        Generates a random grid, choosing to either make the grid connected or
        disconnected with a certain probability.

        :param probability_of_connected: the probability that the random grid will be connected.
        :return: a random grid.
        """

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

        choice_is_connected = random.random() <= probability_of_connected
        if choice_is_connected:
            num_occupied = random.randrange(1, Grid.total_squares())
            print(num_occupied)
            random_x = random.randrange(0, Grid.get_matrix_length())
            random_y = random.randrange(0, Grid.get_matrix_length())
            first_random_occupied_coord = (random_x, random_y)

            def random_occupied_component(coord_list, num_left_to_generate):
                if num_left_to_generate == 0:
                    return coord_list
                else:
                    random_component_coords = random.choice(coord_list)
                    adjecents = adjacent_coords(random_component_coords)
                    legal_adjacents = list(set(adjecents).difference(set(coord_list)))
                    # This might make things horribly slow, since it might keep trying again over and over.
                    try_again = len(legal_adjacents) == 0
                    if try_again:
                        return random_occupied_component(coord_list,
                                                         num_left_to_generate)
                    else:
                        return random_occupied_component(coord_list + [random.choice(legal_adjacents)],
                                                         num_left_to_generate - 1)

            occupied_coords_component = random_occupied_component([first_random_occupied_coord], num_occupied - 1)
            print(occupied_coords_component)
            random_connected_matrix = []
            for x in xrange(Grid.get_matrix_length()):
                row = []
                for y in xrange(Grid.get_matrix_length()):
                    if (x, y) in occupied_coords_component:
                        grid_value = GridSquare.occupied
                    else:
                        grid_value = GridSquare.unoccupied
                    row.append(grid_value)
                random_connected_matrix.append(row)
            random_matrix = random_connected_matrix
        else:
            def random_row():
                random_bit_row = [random.randrange(0, 2) for _ in xrange(Grid.get_matrix_length())]
                grid_values = [GridSquare.unoccupied, GridSquare.occupied]
                return map(lambda bit: grid_values[bit], random_bit_row)

            def is_connected(matrix):
                def find_first_o_coords(m):
                    for x in xrange(Grid.get_matrix_length()):
                        for y in xrange(Grid.get_matrix_length()):
                            if m[x][y] == GridSquare.occupied:
                                return x, y
                    return None

                def occupied_connected_component(m):
                    first_occupied_coords = find_first_o_coords(m)
                    if first_occupied_coords is not None:
                        component = [first_occupied_coords]
                        frontier_coords_list = [first_occupied_coords]
                        while len(frontier_coords_list) > 0:
                            new_frontier_coords_list = []
                            for pioneer_coords in frontier_coords_list:
                                for pioneer_candidate in adjacent_coords(pioneer_coords):
                                    if pioneer_candidate not in component:
                                        x, y = pioneer_candidate
                                        if m[x][y] == GridSquare.occupied:
                                            component.append(pioneer_candidate)
                                            new_frontier_coords_list.append(pioneer_candidate)
                            frontier_coords_list = new_frontier_coords_list
                        return component
                    else:
                        return []

                flattened_matrix = flatten(matrix)
                occupied_count = len(
                    [grid_value for grid_value in flattened_matrix if grid_value == GridSquare.occupied])
                return occupied_count == len(occupied_connected_component(matrix))

            random_disonnected_matrix = [random_row() for _ in xrange(Grid.get_matrix_length())]
            if is_connected(random_disonnected_matrix):
                occupied_coords_list = []
                for x in xrange(Grid.get_matrix_length()):
                    for y in xrange(Grid.get_matrix_length()):
                        if random_disonnected_matrix[x][y] == GridSquare.occupied:
                            occupied_coords_list.append((x, y))

                while is_connected(random_disonnected_matrix):
                    random_occupied_coord = random.choice(occupied_coords_list)
                    occupied_coords_list.remove(random_occupied_coord)
                    x, y = random_occupied_coord
                    random_disonnected_matrix[x][y] = GridSquare.unoccupied
            random_matrix = tuple(tuple(row) for row in random_disonnected_matrix)
            random_matrix = matrix_xo__to_boolean(random_matrix)

        return Grid(random_matrix, choice_is_connected)

    @staticmethod
    def random_data_set(size):
        return tuple(Evaluator.random_grid() for _ in xrange(size))

    @staticmethod
    def evaluate(data_set, num_folds=10):
        """
        Evaluates the perceptron using the passed-in data set.

        :param data_set: a collection of labeled Grids.
        :param num_folds: the number of folds to use during k-fold cross-validation.
        :return: the accuracy of the perceptron.
        """

        assert (len(data_set) <= num_folds)

        def split_data():
            data = []
            index = 0
            for num in xrange(num_folds):
                data.append(data_set[index: num * num_folds])
                index += num * num_folds
            return data

        folds = split_data()
        fold_training_accuracies = []
        for test_set_fold in xrange(num_folds):
            test_set = folds[test_set_fold]
            training_set = folds[:test_set_fold] + folds[test_set_fold + 1:]

            perceptron = algorithms.PerceptronLearner()
            # TODO train the perceptron here
            correct_count = 0
            for test_grid in test_set:
                classification = None  # TODO assign this to the perceptron's classification
                if classification == test_grid.is_connected:
                    correct_count += 1
            fold_training_accuracies.append(correct_count / len(training_set))

        return sum(fold_training_accuracies) / len(fold_training_accuracies)


class GridSquare(object):
    occupied = 'O'
    unoccupied = 'X'


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
    def total_squares():
        return Grid.get_matrix_length() ** 2

    @staticmethod
    def from_string_collection(collection):
        new_matrix = []
        for s in collection:
            new_list = s.split()
            new_matrix.append(new_list)
        # Separate classification
        new_classification = new_matrix.pop()[0]
        new_classification = classification_to_is_connected(new_classification)
        new_matrix = matrix_xo__to_boolean(new_matrix)
        new_grid = Grid(tuple(new_matrix), new_classification)
        return new_grid

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
        xo_matrix = matrix_boolean_to_xo(self.matrix)

        for row in xo_matrix:
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
    return {
        'CONNECTED': True,
        'DISCONNECTED': False
    }.get(classification)


def is_connected_to_classification(is_connected):
    """
    Converts a boolean to a connection classification.

    :param is_connected: a boolean
    :return: 'CONNECTED' if true, 'DISCONNECTED' if false
    """
    return {
        True: 'CONNECTED',
        False: 'DISCONNECTED'
    }.get(is_connected)


def matrix_xo__to_boolean(matrix):
    """
    Converts a matrix with xo__to_boolean.

    :param matrix: the matrix
    :return: the converted matrix
    """
    boolean_matrix = []
    for row in matrix:
        boolean_row = []
        for xo in row:
            boolean = xo__to_boolean(xo)
            boolean_row.append(boolean)
        boolean_matrix.append(boolean_row)
    return boolean_matrix


def xo__to_boolean(xo):
    """
    Converts the character of a grid to a boolean.

    :param xo: the character
    :return: a boolean
    """
    return {
        'X': False,
        'O': True
    }.get(xo)


def matrix_boolean_to_xo(matrix):
    """
    Converts a matrix with boolean_to_xo.

    :param matrix: the matrix
    :return: the converted matrix
    """
    xo_matrix = []
    for row in matrix:
        xo_row = []
        for boolean in row:
            xo = boolean_to_xo(boolean)
            xo_row.append(xo)
        xo_matrix.append(xo_row)
    return xo_matrix


def boolean_to_xo(boolean):
    """
    Converts the boolean of a grid to a character.

    :param boolean: the boolean
    :return: a character
    """
    return {
        False: 'X',
        True: 'O'
    }.get(boolean)


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


def flatten(iterable):
    return [item for subiterable in iterable for item in subiterable]


def main():
    learner = algorithms.PerceptronLearner()
    print 'Weight:' + str(learner.weighted_sum) + '\n'
    file_name = sys.argv[1]
    with open(file_name) as opened_file:
        print_these = file_to_grids(opened_file)
        for grid in print_these:
            print(str(grid) + '\n')


if __name__ == '__main__':
    main()
