__author__ = 'Christopher Raleigh and Anthony Ferrero'

import sys
from copy import copy


class Relation(object):
    """
    An enum that has all possible relation-strings that can exist in a CSP file as its values.
    """

    greater_than = 'gt'
    less_than = 'lt'
    equal = 'eq'
    not_equal = 'ne'

    always_true = lambda x, y: True

    @staticmethod
    def as_function(relation, opposite=False):
        """
        :param relation: a string representing a relation.
        :param opposite: a boolean flag representing if we want to return the opposite of the
                         relation indicated by the relation-string or not.
        :raises: a ValueError if relation is not one of Relation's enum values.
        :return: a function that implements the appropriate relation, or the opposite relation.
        """

        greater_than = lambda x, y: x > y
        less_than = lambda x, y: x < y
        equal = lambda x, y: x == y
        not_equal = lambda x, y: not equal(x, y)
        if relation == Relation.greater_than:
            if not opposite:
                return greater_than
            else:
                return less_than
        elif relation == Relation.less_than:
            if not opposite:
                return less_than
            else:
                return greater_than
        elif relation == Relation.equal:
            if not opposite:
                return equal
            else:
                return not_equal
        elif relation == Relation.not_equal:
            if not opposite:
                return not_equal
            else:
                return equal
        else:
            raise ValueError('"' + relation + '" is not a known relation.')


class Variable(object):
    """
    A variable, which consists of all things relating to variables in the CSP: name, domain, and constraints.
    """

    def __init__(self, name, domain):
        # The state of these objects should not be mutated.
        self.__name = name
        self.__domain = domain

    def __copy__(self):
        return Variable(self.__name, self.__domain, self.__constraints)

    def __hash__(self):
        # All variable names are (supposed to be) unique. So we can just hash based on their names.
        return hash(self.name)

    @property
    def name(self):
        return self.__name

    def order_domain_values(self, constraints):
        """
        Orders this variable's domain values based on the least constraining value heuristic.

        :param constraints: the constraints that this variable is involved in.
        :return: this variable's domain values, ordered based on the least constraining value heuristic.
        """
        pass


class Constraints(object):
    """
    The constraints of a CSP.
    """

    def __init__(self, constraints=None):
        if constraints is None:
            self.__constraints = {}
        else:
            self.__constraints = constraints

    def add_constraint(self, first_var, second_var, relation):
        self.__constraints[(first_var, second_var)] = relation

    def arcs_involving(self, var):
        return [arc for arc in self.__constraints.keys() if var in arc]

    def constraint_satisfied(self, arc, first_value, second_value):
        return self.__constraints[arc](first_value, second_value)


class CSP(object):
    """
    A constraint satisfaction problem (CSP).
    """

    def __init__(self, variables, constraints):
        """
        Create this CSP and make sure that it's node consistent upon creation.

        :param variables: a list of Variable objects, representing the variables involved in this CSP
        :param constraints: a mapping from (var1, var2) tuples to relations, representing the constraints of this CSP.
        :return: a CSP object.
        """
        self.__variables = variables
        self.__constraints = constraints

        # TODO make this CSP node consistent here.

    # This will need to be used in solve() in order to maintain immutability.
    def __copy__(self):
        new_variables = [copy(var) for var in self.__variables]
        return CSP(new_variables)

    @staticmethod
    def from_file(csp_file_name):
        """
        Generates a CSP object from a file.

        Grammar of CSP file language:

            csp               -> {constraint\n} constraint
            constraint        -> unary_constraint|binary_constraint
            unary_constraint  -> variable relation integer
            binary_constraint -> variable relation variable
            variable          -> [a-zA-Z][a-zA-Z0-9_]*
            relation          -> "eq"|"ne"|"lt"|"gt"
            integer           -> [0-9]+

        Example CSP file contents:
            SA ne NSW
            bob eq 27
            Ewoks lt Yoda

        :param csp_file_name: the name of the CSP file to generate the CSP object from.
        :return: a CSP object generated from csp_file_name.
        """

        variables = []
        file_lines = csp_file_name.readlines()
        for line in file_lines:
            # TODO: Make variables from words in this line.
            pass
        return variables

    # TODO: Use backtracking search!
    # TODO: Don't mutate values like the book does. Use immutable data structures/classes in order to avoid bugs.
    def solve(self, do_forward_checking):
        """
        :param do_forward_checking: a boolean flag that indicates whether or not we are to do forward checking.
        :return: a complete assignment for this CSP, or None if it cannot be solved.
        """
        pass

    def __select_unassigned_variable(self, unassigned_vars):
        """
        Selects an unassigned variable using the MRV and degree heuristics.

        :param unassigned_vars: list of variables that are not assigned.
        :return: a variable that has not yet been assigned.
        """
        pass

    def __inferences(self, assignment, do_forward_checking):
        """
        :param assignment: a dict containing variable => value assignments.
        :param do_forward_checking: flag that determines whether or not we do forward checking.
        :return: an assignment, reflecting the inferences that were made or an empty list if we are not to
                 do any inference.
        """
        if do_forward_checking:
            pass
        else:
            return {}

    def __minimum_remaining_values(self, unassigned_vars):
        """
        An implementation of the minimum remaining values (MRV) heuristic.
        :param unassigned_vars: list of variables that are not assigned.
        :return: the variable with the fewest remaining legal values.
        """
        pass

    def __degree(self, var, unassigned_vars):
        """
        An implementation of the degree heuristic.

        :param var: the variable to find the degree of.
        :param unassigned_vars: list of variables that are not assigned.
        :return: the number of constraints that var is involved in with unassigned variables.
        """
        pass


if __name__ == "__main__":
    forward_checking = sys.argv[2]
    with open(sys.argv[1], 'r') as problem_file:
        csp = CSP.from_file(problem_file)
        solution = csp.solve()
        print(solution)