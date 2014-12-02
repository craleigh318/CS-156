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


def __build_decision_tree(examples, attributes):
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
