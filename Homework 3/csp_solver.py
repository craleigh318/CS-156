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

    @staticmethod
    def as_function(relation, opposite=False):
        """
        Converts one of the relation-strings defined on Relation as enum-like values to
        a lambda that implements the relation that the relation-string signifies.

        :type relation: str
        :type opposite: bool
        :rtype: lambda(int, int) -> bool

        :param relation: a string representing a relation.
        :param opposite: a boolean flag representing if we want to return the opposite of the
                         relation indicated by the relation-string or not.
        :return: a function that implements the appropriate relation, or the opposite relation.
        :raises: a ValueError if relation is not one of Relation's enum values.
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
    A variable that knows its name and domain.
    """

    def __init__(self, name, domain):
        self.__name = name
        self.__domain = domain

    def __copy__(self):
        return Variable(self.__name, self.__domain)

    def __hash__(self):
        # All variable names are (supposed to be) unique. So we can just hash based on their names.
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return self.name

    @property
    def name(self):
        return self.__name

    @property
    def domain(self):
        return set(self.__domain)

    @domain.setter
    def domain(self, new_domain):
        self.__domain = new_domain


class Constraints(object):
    """
    The constraints of a CSP.

    Constraints are represented using a dictionary. The dictionary may have
    {Variable: relation_lambda} entries for unary constraints, and
    {(Variable, Variable): relation_lambda} entries for binary constraints.

    relation_lambda is a lambda implementing a relation as returned by Relation.as_function().
    """

    def __init__(self, constraints=None):
        if constraints is None:
            self.__constraints = {}
        else:
            self.__constraints = constraints

    def __copy__(self):
        return Constraints(dict(self.__constraints))

    def add_constraint(self, left_var, relation, right_var_or_value):
        """
        Automatically chooses add_unary_constraint or add_binary_constraint.

        :type left_var: Variable
        :type relation: lambda(int, int) -> bool
        :type right_var_or_value: int or Variable

        :param left_var: the variable on the left side of the relation
        :param relation: the relation between the two variables (or the variable and the value).
        :param right_var_or_value: the variable or value that appears on the right side of the relation.
        """
        if right_var_or_value.isdigit():
            self.add_unary_constraint(left_var, relation, right_var_or_value)
        else:
            self.add_binary_constraint(left_var, relation, right_var_or_value)

    def add_unary_constraint(self, var, relation, integer):
        """
        Adds a unary constraint to the constraint map.

        :type var: Variable
        :type relation: lambda(int, int) -> bool
        :type integer: int

        :param var: the variable to add the unary constraint to
        :param relation: the relation involved in the unary constraint
        :param integer: the integer involved in the unary constraint
        """
        constraint = lambda left_value: relation(left_value, integer)
        if var in self.__constraints:
            self.__constraints[var].append(constraint)
        else:
            self.__constraints[var] = [constraint]

    def add_binary_constraint(self, left_var, relation, right_var):
        """
        Adds a constraint to the constraint map.

        :type left_var: Variable
        :type relation: lambda(int, int) -> bool
        :type: right_var: Variable

        :param left_var: the first variable involved in the constraint.
        :param relation: the relation that the two variables must satisfy.
        :param right_var: the second variable involved in the constraint.
        """
        self.__constraints[(left_var, right_var)] = relation

    def unary_constraints_satisfied(self, var, var_assigned_value):
        """
        :type var: Variable
        :type var_assigned_value: int
        :rtype: bool

        :param var: the variable involved in a unary constraint
        :param var_assigned_value: the value assigned to var.
        :return: True if the assigned value satisfies the unary constraint, False otherwise.
        """
        if var in self.__constraints:
            constraint_list = self.__constraints[var]
            return all(constraint(var_assigned_value) for constraint in constraint_list)
        else:
            raise ValueError('There is no variable by the name of "' + var.name + '"!')

    def binary_constraint_satisfied(self, left_var, left_value, right_var, right_value):
        """

        Checks whether an assignment to two variables satisfies a binary constraint.

        :type left_var: Variable
        :type left_value: int
        :type right_var: Variable
        :type right_value: int
        :rtype: bool

        :param left_var: a variable involved in a constraint.
        :param left_value: the value of first_var
        :param right_var: a variable involved in a constraint.
        :param right_value: the value of second_var
        :return: True if the constraint between first_var and second_var is satisfied by
                 the values first_value and second_value, False otherwise.
        """

        # The arc (tuple) of variables might have been in the reverse order as the
        # variables were passed in. We need to handle this case.
        arg_order_tuple = (left_var, right_var)
        reverse_arg_order_tuple = (right_var, left_var)
        if arg_order_tuple in self.__constraints:
            left_arg, right_arg = left_value, right_value
            arc = arg_order_tuple
        elif reverse_arg_order_tuple in self.__constraints:
            left_arg, right_arg = right_value, left_value
            arc = reverse_arg_order_tuple
        else:
            raise ValueError('There is no relation involving "' + left_var.name +
                             '" and "' + right_var.name + '"!')
        relation = self.__constraints[arc]
        return relation(left_arg, right_arg)

    def neighbors(self, var):
        """
        Find the neighbors of a variable.

        :type var: Variable
        :rtype: list

        :param var: the variable to find the neighbors of.
        :return: a list of neighbors of the variable.
        """
        # This is just to make this method technically correct in all contexts we want to support (i.e., we need to
        # account for the possibility that there will be unary constraints).
        arcs = [key for key in self.__constraints.keys() if type(key) is not Variable]
        arcs_involving_var = [arc for arc in arcs if var in arc]
        flattened_arcs = [neighbor for arc in arcs_involving_var for neighbor in arc]
        return [v for v in flattened_arcs if v != var]

    def has_unary_constraint(self, var):
        """
        Returns True if the variable has a unary constraint, False otherwise.

        :type var: Variable
        :rtype: bool

        :param var: the variable to check for unary constraints on.
        :return: True if var is constrained by a unary constraint, False otherwise.
        """
        return var in self.__constraints

    def remove_unary_constraint(self, var):
        """
        Removes a unary constraint.

        :type var: Variable
        :param var: the variable that has a unary constraint on it that we want to remove.
        """

        del self.__constraints[var]


class Solution(object):
    @staticmethod
    def as_string(assignment):
        """
        Converts a dict of {variable: value} assignments to a string, listing the values assigned
        to each variable in lexicographic order of variable names.

        Example:

        x=2
        y=9
        z=-1

        :type assignment: dict
        :rtype: str

        :param assignment: the assignment dict to convert to a string.
        :return: a string representation of the assignment in the above format, or 'NO SOLUTION' if assignment is None.
        """
        if assignment is None:
            return 'NO SOLUTION'
        else:
            sorted_assignment = sorted(assignment.items(), key=lambda key_value: key_value[0].name)
            lines = [var.name + "=" + str(value) for (var, value) in sorted_assignment]
            return '\n'.join(lines)


class CSP(object):
    """
    A constraint satisfaction problem (CSP).
    """

    def __init__(self, variables, constraints):
        """
        Create this CSP and make sure that it's node consistent upon creation.

        :type variables: list
        :type constraints: Constraints
        :rtype: CSP

        :param variables: a list of Variable objects, representing the variables involved in this CSP
        :param constraints: a mapping from (var1, var2) tuples to relations, representing the constraints of this CSP.
        :return: a node consistent CSP object.
        """
        self.__variables = variables
        self.__constraints = constraints

        self.__make_node_consistent()

    @property
    def variables(self):
        return list(self.__variables)

    @property
    def constraints(self):
        return copy(self.__constraints)

    def __make_node_consistent(self):
        vars_with_unary_constraints = [v for v in self.__variables if self.__constraints.has_unary_constraint(v)]
        for var in vars_with_unary_constraints:
            domain_no_inconsistencies = \
                [val for val in var.domain if self.__constraints.unary_constraints_satisfied(var, val)]
            var.domain = domain_no_inconsistencies
            self.__constraints.remove_unary_constraint(var)

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

        The domain of all variables in a CSP is equal to max(D, V - 1), where D is the number of distinct variables in the
        CSP and V is the maximum value out of all integers used in constraints in the CSP.

        :type csp_file_name: str
        :rtype: CSP

        :param csp_file_name: the name of the CSP file to generate the CSP object from.
        :return: a CSP object generated from csp_file_name.
        """

        with open(csp_file_name, 'r') as problem_file:
            file_lines = problem_file.readlines()
        variables = {}
        constraints = Constraints()
        largest_value = 0
        # Make a list of variable names.
        for line in file_lines:
            words = line.split()
            next_variable = CSP.__get_variable_from_dictionary(variables, words[0])
            next_relation = Relation.as_function(words[1])
            next_value = words[2]
            if next_value.isdigit():
                next_value = int(next_value)
                if next_value > largest_value:
                    largest_value = next_value
                constraints.add_unary_constraint(next_variable, next_relation, next_value)
            else:
                next_value = CSP.__get_variable_from_dictionary(variables, next_value)
                constraints.add_binary_constraint(next_variable, next_relation, next_value)
        # Find d and v.
        d = len(variables)
        v = largest_value
        # Set domains.
        for var in variables.values():
            var.domain = set(xrange(max(d, (v - 1))))
        new_csp = CSP(variables.values(), constraints)
        return new_csp

    @staticmethod
    def __get_variable_from_dictionary(dictionary, variable_name):
        """Gets a Variable object from a dictionary, creating a new Variable if necessary."""
        if variable_name not in dictionary.keys():
            dictionary[variable_name] = Variable(variable_name, None)
        return dictionary.get(variable_name)

    def solve(self, do_forward_checking):
        """
        :type do_forward_checking: bool
        :rtype: dict

        :param do_forward_checking: a boolean flag that indicates whether or not we are to do forward checking.
        :return: a complete assignment for this CSP, or None if it cannot be solved.
        """
        return self.__backtracking_search({}, do_forward_checking)

    def __backtracking_search(self, assignment, do_forward_checking):
        if self.__assignment_is_complete(assignment):
            return assignment
        else:
            unassigned_vars = self.__unassigned_variables(assignment)
            var, unassigned_vars = self.__select_unassigned_variable(unassigned_vars)
            for value in self.__order_domain_values(var, assignment):
                if self.__value_consistent_with_assignment(var, value, assignment):
                    # Make sure we don't mutate the variable's state across loop iterations.
                    var = copy(var)
                    assignment[var] = value
                    inferences = self.__inferences(var, value, unassigned_vars, do_forward_checking)
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

        :type var: Variable
        :type assignment: dict
        :rtype: list

        :param var: the variable who's domain values are being ordered.
        :param assignment: the current assignment being considered by CSP.solve().
        :return: this variable's domain values, ordered based on the least constraining value heuristic.
        """
        values_to_inconsistencies = {}
        unassigned_vars = self.__unassigned_variables(assignment)
        unassigned_neighbors = self.__unassigned_neighbors(var, unassigned_vars)
        for value in var.domain:
            inconsistent_value_count = 0
            for unassigned_neighbor in unassigned_neighbors:
                consistent_domain_values = self.__consistent_domain_values(var, value, unassigned_neighbor)
                inconsistencies = unassigned_neighbor.domain.difference(consistent_domain_values)
                inconsistent_value_count += len(inconsistencies)
            values_to_inconsistencies[value] = inconsistent_value_count

        ordered_values = sorted(values_to_inconsistencies, key=values_to_inconsistencies.get)
        return ordered_values

    def __consistent_domain_values(self, var, var_assigned_value, neighbor_var):
        return {val for val in neighbor_var.domain
                if self.__constraints.binary_constraint_satisfied(left_var=var,
                                                                  left_value=var_assigned_value,
                                                                  right_var=neighbor_var,
                                                                  right_value=val)}

    def __unassigned_neighbors(self, var, unassigned_vars):
        var_neighbors = self.__constraints.neighbors(var)
        return set(unassigned_vars).intersection(set(var_neighbors))

    def __unassigned_variables(self, assignment):
        return [v for v in self.__variables if v not in assignment.keys()]

    def __assignment_is_complete(self, assignment):
        return len(assignment) == len(self.__variables)

    def __value_consistent_with_assignment(self, var_being_assigned, assigning_value, assignment):
        for neighbor in self.__constraints.neighbors(var_being_assigned):
            if neighbor in assignment:
                if not self.__constraints.binary_constraint_satisfied(left_var=var_being_assigned,
                                                                      left_value=assigning_value,
                                                                      right_var=neighbor,
                                                                      right_value=assignment[neighbor]):
                    return False
        return True

    def __select_unassigned_variable(self, unassigned_vars):
        """
        Selects an unassigned variable using the MRV and degree heuristics.

        :type unassigned_vars: list
        :rtype: (Variable, list)

        :param unassigned_vars: variables not yet assigned.
        :return: a variable that has not yet been assigned.
        """
        mrv = self.__minimum_remaining_values(unassigned_vars)
        copy_unassigned_vars = list(unassigned_vars)
        copy_unassigned_vars.remove(mrv)
        return mrv, copy_unassigned_vars

    def __forward_check(self, assigned_var, assigned_value, unassigned_vars):
        """
        Implements forward checking, which establishes arc consistency for a recently-assigned variable.

        :type assigned_var: Variable
        :type assigned_value: int
        :type unassigned_vars: list
        :rtype: bool

        :param assigned_var: the recently-assigned variable to forward check.
        :param assigned_value: the value assigned to the variable.
        :param unassigned_vars: a list of unassigned variables.
        :return: True if no inconsistencies are found. False if otherwise.
        """
        for unassigned_neighbor in self.__unassigned_neighbors(assigned_var, unassigned_vars):
            consistent_values = self.__consistent_domain_values(assigned_var, assigned_value, unassigned_neighbor)
            if len(consistent_values) == 0:
                return False
            else:
                unassigned_neighbor.domain = consistent_values
        return True

    def __inferences(self, assigned_var, assigned_value, unassigned_vars, do_forward_checking):
        """
        Checks for consistent inferences, forward checking if the flag is set.

        :type assigned_var: Variable
        :type assigned_value: int
        :type do_forward_checking: bool
        :type unassigned_vars: list
        :rtype: bool

        :param assigned_var: the recently-assigned variable to do forward checking on.
        :param assigned_value: the value assigned to the variable.
        :param do_forward_checking: flag that determines whether or not we do forward checking.
        :param unassigned_vars: a list of unassigned variables.
        :return: True if we didn't find an inconsistency in the assignment, False otherwise.
        """
        if do_forward_checking:
            return self.__forward_check(assigned_var, assigned_value, unassigned_vars)
        else:
            return True

    def __minimum_remaining_values(self, unassigned_vars):
        """
        An implementation of the minimum remaining values (MRV) heuristic.

        :type unassigned_vars: list
        :rtype: Variable

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

        :type var: Variable
        :type unassigned_vars: list
        :rtype: int

        :param var: the variable to find the degree of.
        :param unassigned_vars: list of variables that are not assigned.
        :return: the number of constraints that var is involved in with unassigned variables.
        """
        return len(self.__unassigned_neighbors(var, unassigned_vars))


def solve_csp(problem_filename, use_forward_checking_str):
    forward_checking = use_forward_checking_str == "1"
    csp = CSP.from_file(problem_filename)
    solution = csp.solve(forward_checking)
    return Solution.as_string(solution)


if __name__ == '__main__':
    solution_string = solve_csp(sys.argv[1], sys.argv[2])
    print(solution_string)
