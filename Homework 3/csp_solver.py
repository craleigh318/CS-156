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

    def as_function(self, relation):
        """
        :param relation: a string representing a relation.
        :raises: a ValueError if relation is not one of Relation's enum values.
        :return: a function that implements the appropriate relation.
        """

        if relation == self.greater_than:
            return lambda x, y: x > y
        elif relation == self.less_than:
            return lambda x, y: x < y
        elif relation == self.equal:
            return lambda x, y: x == y
        elif relation == self.not_equal:
            return lambda x, y: x != y
        else:
            raise ValueError('"' + relation + '" is not a known relation.')


class Variable(object):
    """
    A variable, which consists of all things relating to variables in the CSP: name, domain, and constraints.
    """

    def __init__(self, name, domain, constraints):
        # The state of these objects should not be mutated.
        self.__name = name
        self.__domain = domain
        self.__constraints = constraints

    # This is called when copy() is called on a Variable, for example: copy(variable_object)
    def __copy__(self):
        # We don't need a deep copy, because none of these objects will ever be mutated.
        return Variable(self.__name, self.__domain, self.__constraints)

    def __hash__(self):
        # All variable names are (supposed to be) unique. So we can just hash based on their names.
        return hash(self.name)

    @property
    def name(self):
        return self.__name

    def without_useless_domain_values(self):
        """
        Finds domain values that always violate a constraint on this variable no matter what value from the domain of
        the other variable involved in the constraint is chosen, and thus cannot be involved in a complete assignment.

        This is an implementation of REVISE from the book in Figure 3 on page 265, with the alteration that we return
        both a new copy of this Variable object without any useless domain values and a boolean indicating whether or
        not there were any useless domain values.

        :return: a (new_variable, has_useless_values) tuple, new_variable being this variable without useless domain
                 values and has_useless_values being a boolean value indicating if there were any such values. If there
                 are no useless domain values, new_variable is just a copy of this variable.
        """
        pass

    def order_domain_values(self, partial_assignment):
        """
        Orders this variable's domain values based on the least constraining value heuristic.

        :param partial_assignment: the partial assignment that (might) contribute to the constraints on the variable.
        :return: variable's domain values, ordered according to the least constraining value heuristic.
        """
        pass


class Assignment(object):
    """
    An immutable assignment of variables.
    """

    def __init__(self, assignments=None):
        if assignments is None:
            self.__assignments = {}
        else:
            self.__assignments = assignments

    @staticmethod
    def empty():
        """
        Utility method used to make an empty assignment. Just for readability's sake.
        :return: an empty assignment.
        """
        return Assignment()

    def assign(self, variable, value):
        """
        :param variable: the variable to assign a value to.
        :param value: the value to assign to the variable
        :return: an Assignment updated with the new assignment.
        """
        new_assignments = self.__assignments + {variable: value}
        return Assignment(new_assignments)

    def make_inferences(self):
        pass

    def is_consistent(self):
        pass


class CSP(object):
    """
    A constraint satisfaction problem (CSP).
    """

    def __init__(self, variables):
        self.__variables = variables

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
        return variables

    def make_node_consistent(self):
        """
        Restricts the domain of all variables with unary constraints so that those
        constraints are satisfied by all domain values.
        """
        pass

    # TODO: Use backtracking search!
    # TODO: Don't mutate values like the book does. Use immutable data structures/classes in order to avoid bugs.
    def solve(self, do_forward_checking):
        """
        :param do_forward_checking: a boolean flag that indicates whether or not we are to do forward checking.
        :return: a complete assignment for this CSP, or None if it cannot be solved.
        """
        pass

    def __select_unassigned_variable(self, assigned_variables):
        """
        Selects an unassigned variable using the MRV and degree heuristics.

        :param assigned_variables: variables that have already been assigned.
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
            return assignment.make_inferences()
        else:
            return Assignment.empty()


forward_checking = sys.argv[2]
with open(sys.argv[1], 'r') as problem_file:
    csp = CSP.from_file(problem_file)
    solution = csp.solve()
    print(solution)