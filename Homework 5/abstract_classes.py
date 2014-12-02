import abc

__author__ = 'Christopher Raleigh and Anthony Ferrero'


class Example:
    """
    An example has a classification.
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def classification(self):
        """
        :return: classification of this example
        """


class Tree:
    """
    A tree has a node with a label and may have child nodes.
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def label(self):
        """
        :return: the label of this tree's root
        """

    @abc.abstractproperty
    def children(self):
        """
        :return: a tuple of the subtrees of this tree's root
        """

    @abc.abstractmethod
    def add_branch(self, new_branch):
        """
        Clones this tree and adds the specified branch to the clone.  This original object is unmodified.

        :param new_branch: a tree to add as a branch
        :return: a tree with the new branch added as a child node.
        """