__author__ = 'Christopher Raleigh and Anthony Ferrero'


class Attribute(object):
    """
    An attribute has associated values.
    """

    @property
    def values(self):
        """
        :return: the values of this attribute
        """
        pass


class Example(object):
    """
    An example has a classification.
    """

    @property
    def classification(self):
        """
        :return: classification of this example
        """
        pass


class Tree(object):
    """
    A tree has a node with a label and may have child nodes.
    """

    @property
    def label(self):
        """
        :return: the label of this tree's root
        """
        pass

    @property
    def children(self):
        """
        :return: a tuple of the subtrees of this tree's root
        """
        pass

    def add_branch(self, new_branch):
        """
        Clones this tree and adds the specified branch to the clone.  This original object is unmodified.

        :param new_branch: a tree to add as a branch
        :return: a tree with the new branch added as a child node.
        """
        pass