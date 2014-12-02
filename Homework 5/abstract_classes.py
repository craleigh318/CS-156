import abc

__author__ = 'Christopher Raleigh and Anthony Ferrero'


class Example(object):
    """
    An example has a classification.
    """

    @abc.abstractproperty
    def classification(self):
        """
        :return: classification of this example
        """