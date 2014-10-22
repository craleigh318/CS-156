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
        return Variable(self.__name, self.__domain)

    def __hash__(self):
        # All variable names are (supposed to be) unique. So we can just hash based on their names.
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    @property
    def name(self):
        return self.__name

    @property
    def domain(self):
        return self.__domain


class Constraints(object):
    """
    The constraints of a CSP.
    """

    def __init__(self, constraints=None):
        if constraints is None:
            self.__constraints = {}
        else:
            self.__constraints = constraints

    def add_unary_constraint(self, var, relation, integer):
        """
        Adds a unary constraint to the constraint map.

        :param var: the variable to add the unary constraint to
        :param relation: the relation involved in the unary constraint
        :param integer: the integer involved in the unary constraint
        """
        self.__constraints[var] = lambda x: relation(x, integer)

    def add_binary_constraint(self, first_var, relation, second_var):
        """
        Adds a constraint to the constraint map.

        :param arc: a tuple consisting of the two variables involved in a constraint, in order.
        :param relation: the relation that the variables in the arc must satisfy.
        """
        self.__constraints[(first_var, second_var)] = relation

    def arcs_involving(self, var):
        """
        Find the arcs involving a variable var.

        :param var: the variable to find the arcs involving it.
        :return: a list of arcs (tuples of variables) involving the variable.
        """
        return [arc for arc in self.__constraints.keys() if var in arc]

    def constraint_satisfied(self, first_var, first_value, second_var, second_value):
        """
        :param first_var: a variable involved in a constraint.
        :param first_value: the value of first_var
        :param second_var: a variable involved in a constraint.
        :param second_value: the value of second_var
        :return: True if the constraint between first_var and second_var is satisfied by
                 the values first_value and second_value, False otherwise.
        """

        # The arc (tuple) of variables might have been in the reverse order as the
        # variables were passed in. We need to handle this case.
        arg_order_tuple = (first_var, second_var)
        reverse_arg_order_tuple = (second_var, first_var)
        if arg_order_tuple in self.__constraints:
            first_arg, second_arg = first_value, second_value
            arc = arg_order_tuple
        elif reverse_arg_order_tuple in self.__constraints:
            first_arg, second_arg = second_value, first_value
            arc = reverse_arg_order_tuple
        else:
            raise ValueError('There is no relation involving "' + first_var.name +
                             '" and "' + second_var.name + '"!')
        relation = self.__constraints[arc]
        return relation(first_arg, second_arg)


class Assignment(object):
    @staticmethod
    def as_string(assignment):
        """
        Converts a dict of {variable: value} assignments to a string. Example:

        x = 2
        y = 9
        z = -1
        
        :param assignment: the assignment dict to convert to a string.
        :return: a string representation of the assignment in the above format.
        """

        lines = [var.name + " = " + str(value) for (var, value) in assignment.items()]
        return '\n'.join(lines)


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

        The domain of all variables in a CSP is equal to max(D, V), where D is the number of distinct variables in the
        CSP and V is the maximum value out of all integers used in constraints in the CSP.

        :param csp_file_name: the name of the CSP file to generate the CSP object from.
        :return: a CSP object generated from csp_file_name.
        """

        # TODO compute variable domains (should probably be represented as set(range(0, max(D, V))))
        variable_names = []
        file_lines = csp_file_name.readlines()
        for line in file_lines:
            next_variable_name = line.partition(' ')[0]
            if next_variable_name not in variable_names:
                variable_names.append(next_variable_name)
        variables = []
        for name in variable_names:
            variables.append(Variable(name, None))
        new_csp = CSP(variables, None)
        return new_csp

    # TODO: Don't mutate values like the book does. Use immutable data structures/classes in order to avoid bugs.
    def solve(self, do_forward_checking):
        """
        :param do_forward_checking: a boolean flag that indicates whether or not we are to do forward checking.
        :return: a complete assignment for this CSP, or None if it cannot be solved.
        """
        return self.__backtracking_search({}, do_forward_checking)

    def __backtracking_search(self, assignment, do_forward_checking):
        if self.__assignment_is_complete(assignment):
            return assignment
        else:
            var = self.__select_unassigned_variable(assignment)
            for value in self.__order_domain_values(var, assignment):
                if self.__value_consistent_with_assignment(var, value, assignment):
                    # Make sure we don't mutate the variable's state across loop iterations.
                    var = copy(var)
                    assignment[var] = value
                    inferences = self.__inferences(var, do_forward_checking)
                    if inferences:
                        # Note: the book "adds inferences" to the assignment here, but we don't have to because
                        # all we do when performing inference is delete values from the domains of variables.
                        recursive_solution = self.__backtracking_search(dict(assignment), do_forward_checking)
                        if recursive_solution:
                            return recursive_solution
            return None

    def __order_domain_values(self, var, assignment):
        """
        Orders this variable's domain values based on the least constraining value heuristic.

        :param var: the variable who's domain values are being ordered.
        :param assignment: the current assignment being considered by CSP.solve().
        :return: this variable's domain values, ordered based on the least constraining value heuristic.
        """
        pass

    def __assignment_is_complete(self, assignment):
        return len(assignment) == len(self.__variables)

    def __value_consistent_with_assignment(self, var_being_assigned, assigning_value, assignment):
        for arc in self.__constraints.arcs_involving(var_being_assigned):
            other_var = next([v for v in arc if v != var_being_assigned])
            if other_var in assignment:
                if not self.__constraints.constraint_satisfied(first_var=var_being_assigned,
                                                               first_value=assigning_value,
                                                               second_var=other_var,
                                                               second_value=assignment[other_var]):
                    return False
        return True

    def __select_unassigned_variable(self, assignment):
        """
        Selects an unassigned variable using the MRV and degree heuristics.

        :param assignment: a dict containing variable => value assignments.

        :return: a variable that has not yet been assigned.
        """
        unassigned_vars = [v for v in self.__variables if v not in assignment.keys()]
        mrv = self.__minimum_remaining_values(unassigned_vars)
        return mrv

    def __inferences(self, assigned_var, assigned_value, do_forward_checking):
        """
        Implements forward checking, which establishes arc consistency for a recently-assigned variable.

        :param assigned_var: the recently-assigned variable to do forward checking on.
        :param assigned_value: the value assigned to the variable.
        :param do_forward_checking: flag that determines whether or not we do forward checking.
        :return: True if we didn't find an inconsistency in the assignment, False otherwise.
        """
        if do_forward_checking:
            pass
        else:
            return True

    def __minimum_remaining_values(self, unassigned_vars):
        """
        An implementation of the minimum remaining values (MRV) heuristic.
        :param unassigned_vars: list of variables that are not assigned.
        :return: the variable with the fewest remaining legal values.
        """
        min_var = None
        for var in unassigned_vars:
            if min_var is None:
                min_var = var
            elif len(var.domain) < len(min_var.domain):
                min_var = var
        return min_var

    def __degree(self, var, unassigned_vars):
        """
        An implementation of the degree heuristic.

        :param var: the variable to find the degree of.
        :param unassigned_vars: list of variables that are not assigned.
        :return: the number of constraints that var is involved in with unassigned variables.
        """
        degree = 0
        involved_arcs = self.__constraints.arcs_involving(var)
        for arc in involved_arcs:
            for unassigned_var in unassigned_vars:
                if unassigned_var in arc:
                    degree += 1
        return degree


if __name__ == '__main__':
    forward_checking = sys.argv[2] == "1"
    with open(sys.argv[1], 'r') as problem_file:
        csp = CSP.from_file(problem_file)
        solution = csp.solve(forward_checking)
        print(CSP.assignment_as_string(solution))
