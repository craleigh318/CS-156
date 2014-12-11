import sys
import random
import math
import copy


__author__ = 'Christopher Raleigh and Anthony Ferrero'


class RandomExample(object):

    def __init__(self, grid_points):
        self.__grid_points = grid_points

    def __copy__(self):
        return RandomExample(copy.deepcopy(self.__grid_points))

    @staticmethod
    def __completely_random():
        return RandomExample([RandomExample.__random_row() for _ in xrange(Grid.DIMENSION_SIZE)])

    @staticmethod
    def __all(is_occupied):
        return RandomExample([[is_occupied] * Grid.DIMENSION_SIZE for _ in xrange(Grid.DIMENSION_SIZE)])

    # TODO currently biased towards making very random disconnected grids, but not so random
    # connected ones; the occupied squares in a connected grid tend to be more clumped together
    # than is ideal, whereas the disconnected matrices tend to have squares all over.
    @staticmethod
    def generate(probability_of_connected=0.5):
        choice_is_connected = random.random() <= probability_of_connected
        if choice_is_connected:
            return RandomExample.__generate_connected()
        else:
            return RandomExample.__generate_disconnected()

    @staticmethod
    def __generate_connected():
        unoccupied_random_grid = RandomExample.__all(is_occupied=False)
        random_connected_grid = unoccupied_random_grid.__with_random_occupied_component()
        return random_connected_grid.__to_grid(is_connected=True)

    @staticmethod
    def __generate_disconnected():
        random_grid = RandomExample.__completely_random()
        if random_grid.__is_connected():
            occupied_points = [(x, y) for (x, y) in RandomExample.__points() if random_grid.__is_occupied(x, y)]
            while random_grid.__is_connected():
                occupied_x, occupied_y = random.choice(occupied_points)
                occupied_points.remove((occupied_x, occupied_y))
                random_grid.__set_is_occupied(occupied_x, occupied_y, False)
        return random_grid.__to_grid(is_connected=False)

    @staticmethod
    def __random_row():
        random_bit_row = [random.randrange(0, 2) for _ in xrange(Grid.DIMENSION_SIZE)]
        return [bit == 0 for bit in random_bit_row]

    def __random_occupied_point(self):
        for x, y in RandomExample.__points():
            if self.__grid_points[x][y]:
                return x, y
        return None

    def __is_occupied(self, x, y):
        return self.__grid_points[x][y]

    def __set_is_occupied(self, x, y, is_occupied):
        self.__grid_points[x][y] = is_occupied

    def __is_connected(self):
        total_occupied_count = len([(x, y) for (x, y) in RandomExample.__points() if self.__is_occupied(x, y)])
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
                    for pioneer_candidate_x, pioneer_candidate_y in RandomExample.__neighbors(pioneer_x, pioneer_y):
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
        for x in xrange(Grid.DIMENSION_SIZE):
            for y in xrange(Grid.DIMENSION_SIZE):
                yield x, y

    @staticmethod
    def __neighbors(x, y):
        adjacents = []
        lowest_legal_coord = 0
        highest_legal_coord = Grid.DIMENSION_SIZE - 1

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
        random_x = random.randrange(0, Grid.DIMENSION_SIZE)
        random_y = random.randrange(0, Grid.DIMENSION_SIZE)
        return random_x, random_y

    def __with_random_occupied_component(self):
        copy_self = copy.copy(self)
        num_occupied = random.randrange(1, Grid.total_squares())
        start_x, start_y = RandomExample.__random_point()
        occupied_component = RandomExample.__random_occupied_component([(start_x, start_y)], num_occupied - 1)
        for x, y in RandomExample.__points():
            if (x, y) in occupied_component:
                copy_self.__set_is_occupied(x, y, True)
        return copy_self

    @staticmethod
    def __random_occupied_component(occupied_points, num_left_to_generate):
        if num_left_to_generate == 0:
            return occupied_points
        else:
            random_x, random_y = random.choice(occupied_points)
            neighbors = RandomExample.__neighbors(random_x, random_y)
            legal_adjacents = list(set(neighbors).difference(set(occupied_points)))
            # This might make things horribly slow, since it might keep trying again over and over.
            try_again = len(legal_adjacents) == 0
            if try_again:
                return RandomExample.__random_occupied_component(occupied_points,
                                                                 num_left_to_generate)
            else:
                return RandomExample.__random_occupied_component(occupied_points + [random.choice(legal_adjacents)],
                                                                 num_left_to_generate - 1)

    def __tupled(self):
        return RandomExample(tuple(tuple(row) for row in self.__grid_points))

    def __to_grid(self, is_connected):
        tupled_random_grid = self.__tupled()
        return Example(Grid(tupled_random_grid.__grid_points), is_connected)

    @staticmethod
    def __grid_with_occupied(occupied_points):
        unoccupied_bool = False
        occupied_bool = True
        random_grid_points = [[unoccupied_bool] * Grid.DIMENSION_SIZE for _ in xrange(Grid.DIMENSION_SIZE)]
        for x, y in RandomExample.__points():
            if (x, y) in occupied_points:
                random_grid_points[x][y] = occupied_bool
        tupled_grid_points = RandomExample.__tupled()
        return Example(Grid(tupled_grid_points), is_connected=True)


class Classification(object):
    CONNECTED = 'CONNECTED'
    DISCONNECTED = 'DISCONNECTED'


class GridSquare(object):
    OCCUPIED = 'O'
    UNOCCUPIED = 'X'


class Example(object):
    def __init__(self, grid, classification):
        self.__grid = grid
        self.__classification = classification

    @property
    def is_connected(self):
        return self.__classification

    @property
    def grid(self):
        return self.__grid

    def __str__(self):
        grid_str = str(self.grid)
        classification_str = is_connected_to_classification(self.__classification)
        return grid_str + '\n' + classification_str


class Grid(object):
    CONNECTED_BIT = 1
    DISCONNECTED_BIT = 0

    DIMENSION_SIZE = 5

    def __init__(self, rows=None):
        if rows:
            self.__rows = rows
        else:
            self.__rows = ()

    def num_occupied_in_row(self, row_number):
        assert(row_number < Grid.DIMENSION_SIZE)

        return len([grid_value for grid_value in self.__rows[row_number] if grid_value])

    def num_occupied_in_column(self, column_number):
        assert(column_number < Grid.DIMENSION_SIZE)

        column = [self.__rows[x][column_number] for x in xrange(Grid.DIMENSION_SIZE)]
        return len([grid_value for grid_value in column if grid_value])

    def with_classification(self, classification):
        return Example(Grid(copy.deepcopy(self.__rows)), classification)

    @staticmethod
    def total_squares():
        return Grid.DIMENSION_SIZE**2

    @property
    def rows(self):
        return self.__rows

    def __str__(self):
        grid_str = ''
        xo_rows = rows_boolean_to_xo(self.rows)

        for row in xo_rows:
            grid_str += ' '.join(row)
            grid_str += '\n'

        return grid_str


class Math(object):
    @staticmethod
    def dot_product(vector_1, vector_2):
        return sum([c1 * c2 for c1, c2 in zip(vector_1, vector_2)])

    @staticmethod
    def logistic_function(exp):
        return 1 / (1 + math.pow(math.e, -exp))

    @staticmethod
    def step_function(num, threshold=0.5):
        if num <= threshold:
            return 0
        else:
            return 1

    @staticmethod
    def boolean_to_integer(boolean):
        if boolean:
            return 1
        else:
            return 0


class Perceptron(object):
    LEARNING_RATE = 1.0

    @staticmethod
    def hypothesis(weight_vector, input_vector):
        return Math.logistic_function(Math.dot_product(weight_vector, input_vector))

    @staticmethod
    def __updated_weights(weight_vector, input_vector, classification_bit):
        hypothesis_value = Perceptron.hypothesis(weight_vector, input_vector)
        actual_vs_hypothesis = classification_bit - hypothesis_value
        constant_expression = Perceptron.LEARNING_RATE * \
            (actual_vs_hypothesis * hypothesis_value * (1 - hypothesis_value))
        return [w + constant_expression * x for w, x in zip(weight_vector, input_vector)]

    # TODO the default value for convergence_threshold is probably incorrect. Will need to test it
    # when the perceptron is finished to figure out what a good value is.
    @staticmethod
    def __has_converged(previous_weights, updated_weights, convergence_threshold=0.2):
        sum_squared_differences = sum([(prev - cur)**2 for (prev, cur) in zip(previous_weights, updated_weights)])
        # This might cause this method to ignore when one weight is fluctuating a lot while the others aren't.
        # Might have to reconsider.
        average_squared_difference = sum_squared_differences / len(previous_weights)
        return average_squared_difference <= convergence_threshold

    @staticmethod
    def __add_dummy_inputs(training_set):
        """
        Adds a dummy value of 1 to every input vector in the training set so we can simply
        take the dot product of the weight vector and the input vector to calculate the
        sum of products of the components of the two vectors.
        """
        return [(Perceptron.__add_dummy_input(input_vector), is_connected)
                for input_vector, is_connected in training_set]

    @staticmethod
    def __add_dummy_input(input_vector):
        dummy_value = 1
        return [dummy_value] + input_vector

    @staticmethod
    def __starting_weight_vector(length_input_vector):
        dummy_value = 1
        return [dummy_value] * length_input_vector

    @staticmethod
    def __classify(learned_weights, grid_bit_vector):
        input_vector_with_dummy = Perceptron.__add_dummy_input(grid_bit_vector)
        hypothesis_value = Perceptron.hypothesis(learned_weights, input_vector_with_dummy)
        return Math.step_function(hypothesis_value)

    @staticmethod
    def learn(training_set):
        training_with_dummies = Perceptron.__add_dummy_inputs(training_set)
        length_input_vector = len(training_with_dummies[0][0])
        previous_weight_vector = Perceptron.__starting_weight_vector(length_input_vector)
        current_weight_vector = previous_weight_vector
        while True:  # Because we need a do-while loop, but Python doesn't have one.
            for input_vector, real_classification in training_with_dummies:
                current_weight_vector = Perceptron.__updated_weights(weight_vector=current_weight_vector,
                                                                     input_vector=input_vector,
                                                                     classification_bit=real_classification)
            if Perceptron.__has_converged(previous_weight_vector, current_weight_vector):
                break
            previous_weight_vector = current_weight_vector
        return lambda vec: Perceptron.__classify(current_weight_vector, vec) == Grid.CONNECTED_BIT


class Evaluator(object):
    @staticmethod
    def __k_folds(transformed_data_set, num_folds):
        folds = []
        index = 0
        for num in xrange(num_folds):
            folds.append(transformed_data_set[index: num * num_folds])
            index += num * num_folds
        return folds

    @staticmethod
    def __test_and_training_sets(folds, fold_num):
        test_set = folds[fold_num]
        training_set = folds[:fold_num] + folds[fold_num + 1:]
        return test_set, training_set

    @staticmethod
    def __correct_classification_count(classifier, test_set):
        correct_count = 0
        for input_vector, classification_bit in test_set:
            is_connected = classification_bit == Grid.CONNECTED_BIT
            perceptron_classification = classifier(input_vector)
            if perceptron_classification == is_connected:
                correct_count += 1
        return correct_count

    @staticmethod
    def evaluate(data_set, num_folds=10):
        """
        Evaluates the perceptron using the passed-in data set.

        :param data_set: a collection of labeled Grids.
        :param num_folds: the number of folds to use during k-fold cross-validation.
        :return: the accuracy of the perceptron.
        """

        assert (len(data_set) >= num_folds)

        transformed_data_set = transform_data_set(data_set, lambda grid: transform_grid_counts(grid))
        folds = Evaluator.__k_folds(transformed_data_set, num_folds)
        fold_training_accuracies = []
        for test_set_fold_num in xrange(num_folds):
            test_set, training_set = Evaluator.__test_and_training_sets(folds, test_set_fold_num)
            classifier = Perceptron.learn(training_set)
            correct_count = Evaluator.__correct_classification_count(classifier, test_set)
            training_accuracy = correct_count / len(test_set)
            fold_training_accuracies.append(training_accuracy)

        return sum(fold_training_accuracies) / len(fold_training_accuracies)


class ExampleFileParser(object):
    @staticmethod
    def parse_grid_value(grid_value):
        return {
            GridSquare.OCCUPIED: True,
            GridSquare.UNOCCUPIED: False
        }.get(grid_value)

    @staticmethod
    def parse_grid_row(grid_row_string):
        return [ExampleFileParser.parse_grid_value(s) for s in grid_row_string]

    @staticmethod
    def parse_classification(classification_string):
        """
        Converts a connection classification to a boolean.

        :param classification_string: 'CONNECTED' or 'DISCONNECTED'
        :return: true if 'CONNECTED'
        """
        return {
            'CONNECTED': True,
            'DISCONNECTED': False
        }.get(classification_string)

    @staticmethod
    def parse_input_vector(grid_string_list):
        grid_string_list_no_newlines = [s.rstrip() for s in grid_string_list]
        grid_bits = [ExampleFileParser.parse_grid_value(value)
                     for grid_string in grid_string_list_no_newlines
                     for value in grid_string]

        return grid_bits

    @staticmethod
    def parse_grid(file_lines):
        grid_rows = [ExampleFileParser.parse_grid_row(grid_row_string) for grid_row_string in file_lines]
        return Grid(grid_rows)

    @staticmethod
    def parse_example(file_example_lines):
        grid_lines = file_example_lines[:-1]
        grid = ExampleFileParser.parse_grid(grid_lines)

        classification_string = file_example_lines[-1]
        classification = ExampleFileParser.parse_classification(classification_string)

        return grid.with_classification(classification)

    @staticmethod
    def read_examples(filename):
        with open(filename) as example_file:
            file_lines = example_file.readlines()
            if '\n' in file_lines:
                example_str_list = split_list_by(file_lines, '\n')
            else:
                example_str_list = file_lines
            examples = [ExampleFileParser.parse_example(str_example) for str_example in example_str_list]
            return examples

    @staticmethod
    def read_grid(filename):
        with open(filename) as grid_file:
            grid_string_list = grid_file.readlines()
            return ExampleFileParser.parse_grid(grid_string_list)


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


def rows_boolean_to_xo(matrix):
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
    if len(collection) <= Grid.DIMENSION_SIZE:
        return None
    new_grid = Grid.from_file_lines(collection)
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


def file_to_grids(filename):
    """
    Reads in Grid objects from a file.

    :param filename: the filename of the file containing grids.
    :return: a list of Grids read from the file denoted by 'filename'.
    """
    with open(filename) as grid_file:
        grid_list = []
        file_lines = grid_file.readlines()
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


def write_grids_to_file(grid_list, file_path):
    with open(file_path, 'w') as grid_file:
        for grid in grid_list:
            grid_file.write(str(grid) + '\n\n')


def train(training_file_name):
    return_string = ''
    with open(training_file_name) as training_file:
        file_lines = training_file.readlines()
        for line in file_lines:
            return_string += line
    return return_string


def random_data_set(size):
    return tuple(RandomExample.generate() for _ in xrange(size))


def transform_grid_bits(grid):
    flattened_grid = [is_occupied for row in grid.rows for is_occupied in row]
    return [Math.boolean_to_integer(is_occupied) for is_occupied in flattened_grid]


def transform_grid_counts(grid):
    column_counts = [grid.num_occupied_in_column(col_num) for col_num in xrange(Grid.DIMENSION_SIZE)]
    row_counts = [grid.num_occupied_in_row(row_num) for row_num in xrange(Grid.DIMENSION_SIZE)]
    return column_counts + row_counts


def transform_example(example, grid_transformer):
    transformed_grid = grid_transformer(example.grid)
    classification_bit = Math.boolean_to_integer(example.is_connected)
    return transformed_grid, classification_bit


def transform_data_set(data_set, grid_transformer):
    """
    Transform the data set into a form that can more easily be used to train a perceptron learner.

    Counts the occurrences of occupied squares in all rows and all columns of the matrix, and returns a list of the
    form:

    [column_counts | row_counts]

    :param data_set: the data set to transform.
    :return: the transformed data set, represented as a tuple of (input_vector, is_connected).
    """
    return [transform_example(example, grid_transformer) for example in data_set]


def split_list_by(li, split_value):
    split_list = []
    split_piece = []
    for element in li:
        if element == split_value:
            split_list.append(split_piece)
            split_piece = []
        else:
            split_piece.append(element)
    return split_list


def main():
    if sys.argv[1] == 'gen':
        if len(sys.argv) == 4:
            random_data_set_size, data_set_file = int(sys.argv[2]), sys.argv[3]
            random_grids = random_data_set(random_data_set_size)
            write_grids_to_file(random_grids, data_set_file)
        else:
            print('Usage: connect_learner.py gen [data set size] [data set file path]')
    else:
        _, training_file_name, test_file_name = sys.argv
        training_grid_list = ExampleFileParser.read_examples(training_file_name)
        test_grid = ExampleFileParser.read_grid(test_file_name)
        training_set = transform_data_set(training_grid_list, lambda g: transform_grid_bits(g))
        classifier = Perceptron.learn(training_set)
        input_vector_to_classify = transform_grid_counts(test_grid)
        is_connected = classifier(input_vector_to_classify)

        if is_connected:
            print('CONNECTED')
        else:
            print('DISCONNECTED')


if __name__ == '__main__':
    main()
