__author__ = 'Christopher Raleigh and Anthony Ferrero'


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
            matching_classification = e.classification
        # If this is after the first example, but this classification does not match
        elif matching_classification is not e.classification:
            return None
    return matching_classification


def max_importance(attributes):
    """
    Finds and returns the most important attribute of a collection.

    :param attributes: the collection of attributes
    :return: the most important attribute
    """
    max_a = None
    for a in attributes:
        if (max_a is None) or (a.importance > max_a.importance):
            max_a = a
    return max_a


def __build_decision_tree(examples, attributes):
    A = max_importance()
    tree = DecisionTree(A)
    for v_k in A:
        exs = {}
        for e in examples:
            exs[e.A] = v_k
        subtree = decision_tree_learning(exs, attributes - A, examples)
        tree = tree.add_branch(subtree)
    return None


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
        new_children = self.__children + (new_branch)
        new_tree = DecisionTree(self.__label, new_children)
        return new_tree