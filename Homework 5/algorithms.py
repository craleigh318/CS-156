__author__ = 'Christopher Raleigh and Anthony Ferrero'

import connect_learner


def plurality_value(examples):
    pass


def __share_classification(examples):
    """
    Checks if all examples have the same classification.
    :param examples: the list of examples to check
    :return: the classification that the examples share if it exists, None otherwise
    """

    matching_classification = None
    for e in examples:
        # If this is the first example
        if matching_classification is None:
            matching_classification = e.is_connected
        # If this is after the first example, but this classification does not match
        elif matching_classification != e.is_connected:
            return None
    return matching_classification


def importance(a, examples):
    """
    Judges the importance of an attribute

    :param a: an attribute
    :param examples: examples for the attribute
    :return: the attributes importance
    """
    pass


def max_importance(attributes, examples):
    """
    Finds and returns the most important attribute of a collection.

    :param attributes: the collection of attributes
    :return: the most important attribute
    """
    max_a = None
    for a in attributes:
        if (max_a is None) or (importance(a, examples) > importance(max_a, examples)):
            max_a = a
    return max_a


def tuple_without_e(original_collection, e):
    """
    Copies a collection without element e.
    :param original_collection: the collection to derive
    :param e: the element to exclude
    :return: a new tuple
    """
    new_list = list(original_collection)
    new_list.pop(e)
    return_tuple = tuple(new_list)
    return return_tuple


def __build_decision_tree(examples, attributes):
    big_a = max_importance(attributes, examples)
    attributes_minus_big_a = tuple_without_e(attributes, big_a)
    tree = DecisionTree(big_a)
    for v_k in big_a.values:
        exs = {}
        for e in examples:
            exs[e] = v_k
        subtree = decision_tree_learning(exs, attributes_minus_big_a, examples)
        tree = tree.add_branch(subtree)
    return tree


def decision_tree_learning(examples, attributes, parent_examples):
    if not examples:
        return plurality_value(parent_examples)
    else:
        classification = __share_classification(examples)
        if classification is not None:
            return classification
        elif not attributes:
            return plurality_value(examples)
        else:
            return __build_decision_tree(examples, attributes)


class DecisionTree(object):
    """
    A decision tree has a node with a label and may have child nodes.
    """

    def __init__(self, label, children=()):
        self.__label = label
        self.__children = children

    @property
    def label(self):
        """
        :return: the label of this tree's root
        """
        return self.__label

    @property
    def children(self):
        """
        :return: a tuple of the subtrees of this tree's root
        """
        return self.__children

    def add_branch(self, new_branch):
        """
        Clones this tree and adds the specified branch to the clone.  The original tree is unmodified.

        :param new_branch: a tree to add as a branch
        :return: a tree with the new branch added as a child node.
        """
        new_children = self.__children + tuple(new_branch)
        new_tree = DecisionTree(self.__label, new_children)
        return new_tree


class PerceptronLearner(object):
    @staticmethod
    def heaviside_step_function(n):
        if n < 0:
            return 0
        else:
            return 1

    def __init__(self):
        self.__learned_examples = []

    @property
    def weighted_sum(self):
        weighted_sum = 0
        for example in self.__learned_examples:
            addition = example.input * example.weight
            weighted_sum += addition
        return weighted_sum

    def dot_product(self, matrix):
        """
        Returns the dot product of a matrix with the matrix of a training example.
        :param matrix: a matrix to multiply
        :return: the dot product
        """
        product = 1
        product_vector = []
        for i in xrange(len(matrix[0])):
            unit_product = 1
            for row in matrix:
                unit_product *= row[i]
            product_vector.append(unit_product)
        for unit in product_vector:
            product *= unit
        return product

    def give_example(self, example):
        """
        Teaches this learner with a new example.

        :param example: an Example object
        """
        self.__learned_examples.append(example)

    def guess_output(self, input_matrix):
        """
        Has this learner guess this input from previously-taught examples.

        :param input_matrix: the input to guess.
        :return: the guess.
        """
        difference = input_matrix - self.weighted_sum
        guess = PerceptronLearner.heaviside_step_function(difference)
        return guess

    @staticmethod
    def has_converged(previous_weights, updated_weights, convergence_threshold=0.2):
        sum_squared_differences = sum([(prev - cur)**2 for (prev, cur) in zip(previous_weights, updated_weights)])
        # This might cause this method to ignore when one weight is fluctuating a lot while the others aren't.
        # Might have to reconsider.
        average_squared_difference = sum_squared_differences / len(previous_weights)
        return average_squared_difference <= convergence_threshold

    def train(self, training_set):
        length_input_vector = len(training_set[0])
        dummy_value = 1
        previous_weight_vector = [[dummy_value] * length_input_vector]
        current_weight_vector = previous_weight_vector
        while True:  # Because we need a do-while loop, but Python doesn't have one.
            # TODO update the weights of the perceptron
            if PerceptronLearner.has_converged(previous_weight_vector, current_weight_vector):
                break
            previous_weight_vector = current_weight_vector


class GridPerceptronLearner(object):
    """
    A decorator of the regular PerceptronLearner, for use with Grid objects.
    """

    @staticmethod
    def boolean_to_weight(boolean):
        """
        Weighs this grid tile, assigning it an integer.

        :param boolean: the grid tile, a boolean value
        :return: the weight, for learning
        """
        return {
            True: 1,
            False: -1
        }.get(boolean)

    @staticmethod
    def weigh_matrix(matrix):
        """
        Copies this matrix, replacing tiles with their weights.

        :param matrix: the matrix to weigh
        :return: a new matrix with integer values
        """
        weighted_matrix = []
        for row in matrix:
            weighted_row = []
            for tile in row:
                weight = GridPerceptronLearner.boolean_to_weight(tile)
                weighted_row.append(weight)
            weighted_matrix.append(weighted_row)
        return weighted_matrix

    @staticmethod
    def weight_to_boolean(weight):
        if weight < 0:
            return False
        else:
            return True

    def __init__(self):
        self.__learner = PerceptronLearner()

    @property
    def weighted_sum(self):
        return self.__learner.weighted_sum

    def give_example(self, example):
        """
        Teaches this learner with a new example.

        :param example: an Example object
        """
        weighted_matrix = GridPerceptronLearner.weigh_matrix(example.matrix)
        weighted_example = connect_learner.Grid(weighted_matrix, example.is_connected)
        return self.__learner.give_example(weighted_example)

    def guess_output(self, input_matrix):
        """
        Has this learner guess this input from previously-taught examples.

        :param input_matrix: the input to guess.
        :return: the guess.
        """
        return self.__learner.guess_output(input_matrix)