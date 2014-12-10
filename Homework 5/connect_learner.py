import sys
import random

import abstract_classes
import algorithms
import copy


__author__ = 'Christopher Raleigh and Anthony Ferrero'


class RandomGrid(object):

    def __init__(self, grid_points):
        self.__grid_points = grid_points

    def __copy__(self):
        return RandomGrid(copy.deepcopy(self.__grid_points))

    @staticmethod
    def __completely_random():
        return RandomGrid([RandomGrid.__random_row() for _ in xrange(Grid.get_matrix_length())])

    @staticmethod
    def __all(is_occupied):
        return RandomGrid([[is_occupied] * Grid.get_matrix_length() for _ in xrange(Grid.get_matrix_length())])

    # TODO currently biased towards making very random disconnected grids, but not so random
    # connected ones; the occupied squares in a connected grid tend to be more clumped together
    # than is ideal, whereas the disconnected matrices tend to have squares all over.
    @staticmethod
    def generate(probability_of_connected=0.5):
        choice_is_connected = random.random() <= probability_of_connected
        if choice_is_connected:
            return RandomGrid.__generate_connected()
        else:
            return RandomGrid.__generate_disconnected()

    @staticmethod
    def __generate_connected():
        unoccupied_random_grid = RandomGrid.__all(is_occupied=False)
        random_connected_grid = unoccupied_random_grid.__with_random_occupied_component()
        return random_connected_grid.__to_grid(is_connected=True)

    @staticmethod
    def __generate_disconnected():
        random_grid = RandomGrid.__completely_random()
        if random_grid.__is_connected():
            occupied_points = [(x, y) for (x, y) in RandomGrid.__points() if random_grid.__is_occupied(x, y)]
            while random_grid.__is_connected():
                occupied_x, occupied_y = random.choice(occupied_points)
                occupied_points.remove((occupied_x, occupied_y))
                random_grid.__set_is_occupied(occupied_x, occupied_y, False)
        return random_grid.__to_grid(is_connected=False)

    @staticmethod
    def __random_row():
        random_bit_row = [random.randrange(0, 2) for _ in xrange(Grid.get_matrix_length())]
        return [bit == 0 for bit in random_bit_row]

    def __random_occupied_point(self):
        for x, y in RandomGrid.__points():
            if self.__grid_points[x][y]:
                return x, y
        return None

    def __is_occupied(self, x, y):
        return self.__grid_points[x][y]

    def __set_is_occupied(self, x, y, is_occupied):
        self.__grid_points[x][y] = is_occupied

    def __is_connected(self):
        total_occupied_count = len([(x, y) for (x, y) in RandomGrid.__points() if self.__is_occupied(x, y)])
        connected_occupied_count = len(self.__occupied_connected_component())
        return total_occupied_count == connected_occupied_count

    def __occupied_connected_component(self):
        occupied_point = self.__random_occupied_point()
        if occupied_point is not None:
            component = [occupied_point]
            frontier_points = [occupied_point]
            while len(frontier_points) > 0:
                fresh_frontier_points = []
                for pioneer_x, pioneer_y in frontier_points:
                    for pioneer_candidate_x, pioneer_candidate_y in RandomGrid.__neighbors(pioneer_x, pioneer_y):
                        if (pioneer_candidate_x, pioneer_candidate_y) not in component:
                            if self.__is_occupied(pioneer_candidate_x, pioneer_candidate_y):
                                fresh_pioneer = (pioneer_candidate_x, pioneer_candidate_y)
                                component.append(fresh_pioneer)
                                fresh_frontier_points.append(fresh_pioneer)
                frontier_points = fresh_frontier_points
            return component
        else:
            return []

    @staticmethod
    def __points():
        for x in xrange(Grid.get_matrix_length()):
            for y in xrange(Grid.get_matrix_length()):
                yield x, y

    @staticmethod
    def __neighbors(x, y):
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

    @staticmethod
    def __random_point():
        random_x = random.randrange(0, Grid.get_matrix_length())
        random_y = random.randrange(0, Grid.get_matrix_length())
        return random_x, random_y

    def __with_random_occupied_component(self):
        copy_self = copy.copy(self)
        num_occupied = random.randrange(1, Grid.total_squares())
        start_x, start_y = RandomGrid.__random_point()
        occupied_component = RandomGrid.__random_occupied_component([(start_x, start_y)], num_occupied - 1)
        for x, y in RandomGrid.__points():
            if (x, y) in occupied_component:
                copy_self.__set_is_occupied(x, y, True)
        return copy_self

    @staticmethod
    def __random_occupied_component(occupied_points, num_left_to_generate):
        if num_left_to_generate == 0:
            return occupied_points
        else:
            random_x, random_y = random.choice(occupied_points)
            neighbors = RandomGrid.__neighbors(random_x, random_y)
            legal_adjacents = list(set(neighbors).difference(set(occupied_points)))
            # This might make things horribly slow, since it might keep trying again over and over.
            try_again = len(legal_adjacents) == 0
            if try_again:
                return RandomGrid.__random_occupied_component(occupied_points,
                                                              num_left_to_generate)
            else:
                return RandomGrid.__random_occupied_component(occupied_points + [random.choice(legal_adjacents)],
                                                              num_left_to_generate - 1)

    def __tupled(self):
        return RandomGrid(tuple(tuple(row) for row in self.__grid_points))

    def __to_grid(self, is_connected):
        tupled_random_grid = self.__tupled()
        return Grid(tupled_random_grid.__grid_points, is_connected)

    @staticmethod
    def __grid_with_occupied(occupied_points):
        unoccupied_bool = False
        occupied_bool = True
        random_grid_points = [[unoccupied_bool] * Grid.get_matrix_length() for _ in xrange(Grid.get_matrix_length())]
        for x, y in RandomGrid.__points():
            if (x, y) in occupied_points:
                random_grid_points[x][y] = occupied_bool
        tupled_grid_points = RandomGrid.__tupled()
        return Grid(tupled_grid_points, is_connected=True)


class GridSquare(object):
    occupied = 'O'
    unoccupied = 'X'


class Grid(abstract_classes.Example):
    def __init__(self, matrix=None, is_connected=None):
        if matrix:
            self.__matrix = matrix
        else:
            self.__matrix = ()
        self.__is_connected = is_connected

    def num_occupied_in_row(self, row_number):
        assert(row_number < Grid.get_matrix_length())

        return len([grid_value for grid_value in self.__matrix[row_number] if grid_value])

    def num_occupied_in_column(self, column_number):
        assert(column_number < Grid.get_matrix_length())

        column = [self.__matrix[x][column_number] for x in xrange(Grid.get_matrix_length())]
        return len([grid_value for grid_value in column if grid_value])

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


def random_data_set(size):
    return tuple(RandomGrid.generate() for _ in xrange(size))


def transform_grid_bits(grid):
    def boolean_to_integer(boolean):
        if boolean:
            return 1
        else:
            return 0
    flattened_grid = [is_occupied for row in grid for is_occupied in row]
    return [boolean_to_integer(is_occupied) for is_occupied in flattened_grid], grid.is_connected


def transform_grid_counts(grid):
    column_counts = [grid.num_occupied_in_column(col_num) for col_num in xrange(Grid.get_matrix_length())]
    row_counts = [grid.num_occupied_in_row(row_num) for row_num in xrange(Grid.get_matrix_length())]
    return column_counts + row_counts, grid.is_connected


def transform_data_set(data_set, transformation_function):
    """
    Transform the data set into a form that can more easily be used to train a perceptron learner.

    Counts the occurrences of occupied squares in all rows and all columns of the matrix, and returns a list of the
    form:

    [column_counts | row_counts]

    :param data_set: the data set to transform.
    :return: the transformed data set, represented as a tuple of (input_vector, is_connected).
    """
    transformed_data_set = [transformation_function(grid) for grid in data_set]
    input_vectors = [t[0] for t in transformed_data_set]
    is_connected_list = [t[1] for t in transformed_data_set]

    return input_vectors, is_connected_list


def evaluate(data_set, num_folds=10):
    """
    Evaluates the perceptron using the passed-in data set.

    :param data_set: a collection of labeled Grids.
    :param num_folds: the number of folds to use during k-fold cross-validation.
    :return: the accuracy of the perceptron.
    """

    assert (len(data_set) <= num_folds)

    tranformed_data_set, is_connected_list = transform_data_set(data_set, lambda grid: transform_grid_counts(grid))

    def split_data():
        data = []
        index = 0
        for num in xrange(num_folds):
            data.append(tranformed_data_set[index: num * num_folds])
            index += num * num_folds
        return data

    folds = split_data()
    fold_training_accuracies = []
    for test_set_fold in xrange(num_folds):
        test_set = folds[test_set_fold]
        training_set = folds[:test_set_fold] + folds[test_set_fold + 1:]

        perceptron = algorithms.PerceptronLearner()
        # TODO train the perceptron here
        test_set_index_start = test_set_fold * num_folds
        correct_count = 0
        for test_set_num in xrange(len(test_set)):
            test_input_vector = test_set[test_set_num]
            is_connected = is_connected_list[test_set_index_start + test_set_num]
            classification = None  # TODO assign this to the perceptron's classification
            if classification == is_connected:
                correct_count += 1
        fold_training_accuracies.append(correct_count / len(training_set))

    return sum(fold_training_accuracies) / len(fold_training_accuracies)


def main():
    learner = algorithms.GridPerceptronLearner()
    file_name = sys.argv[1]
    with open(file_name) as opened_file:
        print_these = file_to_grids(opened_file)
        for grid in print_these:
            print(str(grid) + '\n')
            print '\n'
            learner.give_example(grid)
        #print 'Weight:' + str(learner.weighted_sum) + '\n'


if __name__ == '__main__':
    main()
