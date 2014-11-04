__author__ = 'Christopher Raleigh and Anthony Ferrero'

import unittest

from csp_solver import *


class ConstraintTestCase(unittest.TestCase):
    def _constraint_violation_message(self, constraints, left_var, left_value, right_var, right_value):
        def identify_relation():
            low_value = -1
            high_value = 1

            greater_than = constraints.binary_constraint_satisfied(left_var=left_var,
                                                                   left_value=high_value,
                                                                   right_var=right_var,
                                                                   right_value=low_value)
            less_than = constraints.binary_constraint_satisfied(left_var=left_var,
                                                                left_value=low_value,
                                                                right_var=right_var,
                                                                right_value=high_value)
            equal = constraints.binary_constraint_satisfied(left_var=left_var,
                                                            left_value=low_value,
                                                            right_var=right_var,
                                                            right_value=low_value)
            not_equal = greater_than and less_than

            if not_equal:
                relation_str = '!='
            elif equal:
                relation_str = '=='
            elif greater_than:
                relation_str = '>'
            elif less_than:
                relation_str = '<'
            else:
                raise ValueError('Unknown relation between ' +
                                 left_var.name +
                                 ' and ' +
                                 right_var.name)

            return relation_str

        return 'Constraint not satisfied: ' + left_var.name + ' ' + identify_relation() + ' ' + right_var.name

    def assert_all_constraints_satisfied(self, variables, constraints, solution_assignment):
        for var in variables:
            for neighbor in constraints.neighbors(var):
                constraint_satisfied = \
                    constraints.binary_constraint_satisfied(left_var=var,
                                                            left_value=solution_assignment[var],
                                                            right_var=neighbor,
                                                            right_value=solution_assignment[neighbor])
                self.assertTrue(constraint_satisfied, self._constraint_violation_message(constraints,
                                                                                         var,
                                                                                         solution_assignment[var],
                                                                                         neighbor,
                                                                                         solution_assignment[neighbor]))

    def assert_all_variables_assigned(self, variables, solution_assignment):
        key = lambda v: v.name
        self.assertListEqual(sorted(variables, key=key), sorted(solution_assignment.keys(), key=key))

    def assert_domain_values_assigned(self, domain, solution_assignment):
        self.assertTrue(set(solution_assignment.values()).issubset(set(domain)))


class VariableHashing(unittest.TestCase):
    def test_hashes_based_on_name(self):
        name = "Variable Name"
        name_hash = hash(name)
        var = Variable(name, None)
        var_hash = hash(var)

        self.assertEqual(name_hash, var_hash, "You're not hashing Variables based on their names!")


class ConstraintsNeighborsHasNeighbors(unittest.TestCase):
    def test_constraints_neighbors_has_neighbors(self):
        constraints = Constraints()
        first_var = Variable("First!", None)
        second_var = Variable("Second!", None)
        constraints.add_binary_constraint(first_var, None, second_var)

        expected = [second_var]
        actual = constraints.neighbors(first_var)
        self.assertSequenceEqual(expected, actual)

        expected = [first_var]
        actual = constraints.neighbors(second_var)
        self.assertSequenceEqual(expected, actual)


class ConstraintsNeighborsHasNoNeighbors(unittest.TestCase):
    def test_constraints_neighbors_has_no_neighbors(self):
        constraints = Constraints()
        unconstrained_var = Variable("Not Constrained", None)
        expected = []
        actual = constraints.neighbors(unconstrained_var)
        self.assertSequenceEqual(expected, actual)


class ConstraintsConstraintSatisfiedHasConstraint(unittest.TestCase):
    def test_constraints_satisfied_returns_true_when_relation_is_true(self):
        constraints = Constraints()
        first_var = Variable("First!", None)
        second_var = Variable("Second!", None)
        relation = Relation.as_function(Relation.greater_than)
        constraints.add_binary_constraint(first_var, relation, second_var)

        result = constraints.binary_constraint_satisfied(first_var, 9999999999999, second_var, 0)
        self.assertTrue(result)


class ConstraintsConstraintNotSatisfiedHasConstraint(unittest.TestCase):
    def test_constraints_satisfied_returns_false_when_relation_is_false(self):
        constraints = Constraints()
        first_var = Variable("First!", None)
        second_var = Variable("Second!", None)
        relation = Relation.as_function(Relation.greater_than)
        constraints.add_binary_constraint(first_var, relation, second_var)

        result = constraints.binary_constraint_satisfied(first_var, 0, second_var, 48932749874)
        self.assertFalse(result)


class ConstraintsConstraintSatisfiedHasNoConstraint(unittest.TestCase):
    def test_constraints_satisfied_raises_value_error_when_has_no_constraint(self):
        constraints = Constraints()
        first_var = Variable("First!", None)
        second_var = Variable("Second!", None)
        self.assertRaises(ValueError, constraints.binary_constraint_satisfied, first_var, 0, second_var, 0)


class AssignmentAsString(unittest.TestCase):
    def test_assignment_as_string(self):
        test_assignment = {
            Variable("X", None): 5,
            Variable("Y", None): 20
        }
        expected = "X=5\nY=20"
        actual = Solution.as_string(test_assignment)
        self.assertEqual(expected, actual)


class CSPSolveEmptyCSP(unittest.TestCase):
    def test_csp_solve_empty_csp(self):
        test_csp = CSP([], Constraints())
        expected = {}
        actual = test_csp.solve(False)
        self.assertDictEqual(expected, actual)


def all_variables_assigned(variables, solution_assignment):
    key = lambda v: v.name
    return sorted(variables, key=key) == sorted(solution_assignment.keys(), key=key)


def domain_values_assigned(domain, solution_assignment):
    return set(solution_assignment.values()).issubset(set(domain))


def all_constraints_satisfied(variables, constraints, solution_assignment):
    for var in variables:
        for neighbor in constraints.neighbors(var):

            if not constraints.binary_constraint_satisfied(left_var=var,
                                                           left_value=solution_assignment[var],
                                                           right_var=neighbor,
                                                           right_value=solution_assignment[neighbor]):
                return False
    return True


class CSPSolveOneUnaryConstraintNoForwardChecking(unittest.TestCase):
    def test_csp_solve_one_unary_constraint_no_forward_checking(self):
        var_1 = Variable("X", set(range(0, 2)))
        var_2 = Variable("Y", set(range(0, 2)))
        constraints = Constraints()
        constraints.add_unary_constraint(var_1, lambda x, y: x < y, 1)
        variables = [var_1, var_2]
        test_csp = CSP(variables, constraints)
        solution_assignment = test_csp.solve(False)

        self.assertTrue(all_variables_assigned(variables, solution_assignment))
        self.assertTrue(domain_values_assigned(set(range(0, 2)), solution_assignment))
        self.assertTrue(all_constraints_satisfied(variables, constraints, solution_assignment))


class CSPSolveOneBinaryConstraintNoForwardChecking(unittest.TestCase):
    def test_csp_solve_one_binary_constraint_no_forward_checking(self):
        var_1 = Variable("X", set(range(0, 2)))
        var_2 = Variable("Y", set(range(0, 2)))
        relation = lambda x, y: x > y
        constraints = Constraints()
        constraints.add_binary_constraint(var_1, relation, var_2)
        variables = [var_1, var_2]
        test_csp = CSP(variables, constraints)
        solution_assignment = test_csp.solve(False)

        self.assertTrue(all_variables_assigned(variables, solution_assignment))
        self.assertTrue(domain_values_assigned(set(range(0, 2)), solution_assignment))
        self.assertTrue(all_constraints_satisfied(variables, constraints, solution_assignment))


class CSPSolveOneBinaryConstraintWithForwardChecking(unittest.TestCase):
    def test_csp_solve_one_binary_constraint_with_forward_checking(self):
        var_1 = Variable("X", set(range(0, 2)))
        var_2 = Variable("Y", set(range(0, 2)))
        relation = lambda x, y: x > y
        constraints = Constraints()
        constraints.add_binary_constraint(var_1, relation, var_2)
        variables = [var_1, var_2]
        test_csp = CSP(variables, constraints)
        solution_assignment = test_csp.solve(True)

        self.assertTrue(all_variables_assigned(variables, solution_assignment))
        self.assertTrue(domain_values_assigned(set(range(0, 2)), solution_assignment))
        self.assertTrue(all_constraints_satisfied(variables, constraints, solution_assignment))


class CSPSolveSeveralBinaryConstraintsNoForwardChecking(unittest.TestCase):
    def test_csp_solve_several_binary_constraints_no_forward_checking(self):
        num_variables = 4
        var_1 = Variable("W", set(range(0, num_variables)))
        var_2 = Variable("X", set(range(0, num_variables)))
        var_3 = Variable("Y", set(range(0, num_variables)))
        var_4 = Variable("Z", set(range(0, num_variables)))

        relation = lambda x, y: x > y
        constraints = Constraints()
        constraints.add_binary_constraint(var_1, relation, var_2)
        constraints.add_binary_constraint(var_1, relation, var_3)
        constraints.add_binary_constraint(var_1, relation, var_4)
        relation = lambda x, y: x != y
        constraints.add_binary_constraint(var_2, relation, var_3)
        constraints.add_binary_constraint(var_3, relation, var_4)

        variables = [var_1, var_2, var_3, var_4]
        test_csp = CSP(variables, constraints)
        test_solution = test_csp.solve(False)

        self.assertTrue(all_variables_assigned(variables, test_solution))
        self.assertTrue(domain_values_assigned(set(range(0, num_variables)), test_solution))
        self.assertTrue(all_constraints_satisfied(variables, constraints, test_solution))


class CSPSolveSeveralBinaryConstraintsWithForwardChecking(unittest.TestCase):
    def test_csp_solve_several_binary_constraints_with_forward_checking(self):
        num_variables = 4
        var_1 = Variable("W", set(range(0, num_variables)))
        var_2 = Variable("X", set(range(0, num_variables)))
        var_3 = Variable("Y", set(range(0, num_variables)))
        var_4 = Variable("Z", set(range(0, num_variables)))

        relation = lambda x, y: x > y
        constraints = Constraints()
        constraints.add_binary_constraint(var_1, relation, var_2)
        constraints.add_binary_constraint(var_1, relation, var_3)
        constraints.add_binary_constraint(var_1, relation, var_4)
        relation = lambda x, y: x != y
        constraints.add_binary_constraint(var_2, relation, var_3)
        constraints.add_binary_constraint(var_3, relation, var_4)

        variables = [var_1, var_2, var_3, var_4]
        test_csp = CSP(variables, constraints)
        test_solution = test_csp.solve(True)

        self.assertTrue(all_variables_assigned(variables, test_solution))
        self.assertTrue(domain_values_assigned(set(range(0, num_variables)), test_solution))
        self.assertTrue(all_constraints_satisfied(variables, constraints, test_solution))


class CSPSolveAllConstraintsNoForwardChecking(unittest.TestCase):
    def test_csp_solve_all_constraints_no_forward_checking(self):
        max_value = 24
        domain_upper_bound = max_value + 1
        var_1 = Variable("W", set(range(0, domain_upper_bound)))
        var_2 = Variable("X", set(range(0, domain_upper_bound)))
        var_3 = Variable("Y", set(range(0, domain_upper_bound)))
        var_4 = Variable("Z", set(range(0, domain_upper_bound)))

        constraints = Constraints()
        # Unary constraint additions.
        relation = lambda x, y: x == y
        constraints.add_unary_constraint(var_1, relation, max_value)
        relation = lambda x, y: x < y
        constraints.add_unary_constraint(var_2, relation, 3)

        # Binary constraint additions.
        relation = lambda x, y: x > y
        constraints.add_binary_constraint(var_1, relation, var_2)
        constraints.add_binary_constraint(var_1, relation, var_3)
        constraints.add_binary_constraint(var_1, relation, var_4)
        relation = lambda x, y: x == y
        constraints.add_binary_constraint(var_2, relation, var_3)
        constraints.add_binary_constraint(var_3, relation, var_4)

        variables = [var_1, var_2, var_3, var_4]
        test_csp = CSP(variables, constraints)
        test_solution = test_csp.solve(True)

        self.assertTrue(all_variables_assigned(variables, test_solution))
        self.assertTrue(domain_values_assigned(set(range(0, domain_upper_bound)), test_solution))
        self.assertTrue(all_constraints_satisfied(variables, constraints, test_solution))


class CSPSolveUlandWithForwardChecking(unittest.TestCase):
    def test_csp_from_file_uland(self):
        actual = solve_csp('Test Uland.txt', '1')
        # Doesn't output exactly what the assignment says it should, but it's still technically correct.
        expected = 'ME=0\nShortz=2\nUland=1'
        self.assertEqual(actual, expected)


class CSPSolveUlandNoForwardChecking(unittest.TestCase):
    def test_csp_from_file_uland(self):
        actual = solve_csp('Test Uland.txt', '0')
        # Doesn't output exactly what the assignment says it should, but it's still technically correct.
        expected = 'ME=0\nShortz=2\nUland=1'
        self.assertEqual(actual, expected)


class CSPSolveAustraliaMapColoringWithForwardChecking(unittest.TestCase):
    def test_csp_solve_australia_map_coloring_with_forward_checking(self):
        test_csp = CSP.from_file('Test Australia.txt')
        solution = test_csp.solve(True)

        # Variable-related assertions.
        num_of_vars = 10  # We're counting the color-variables too.
        domain_upper_bound = num_of_vars - 1
        var_domain = set(xrange(domain_upper_bound))
        red = Variable('red', var_domain)
        green = Variable('green', var_domain)
        blue = Variable('blue', var_domain)
        wa = Variable('WA', var_domain)
        t = Variable('T', var_domain)
        nt = Variable('NT', var_domain)
        sa = Variable('SA', var_domain)
        q = Variable('Q', var_domain)
        nsw = Variable('NSW', var_domain)
        v = Variable('V', var_domain)
        variables = [red, green,
                     blue, wa,
                     t, nt,
                     sa, q,
                     nsw, v]
        self.assertTrue(all_variables_assigned(variables, solution))
        self.assertTrue(domain_values_assigned(set(range(0, domain_upper_bound)), solution))

        # Constraint-related assertion.
        constraints = Constraints()
        eq = lambda x, y: x == y
        constraints.add_unary_constraint(red, eq, 0)
        constraints.add_unary_constraint(green, eq, 1)
        constraints.add_unary_constraint(blue, eq, 2)

        lt = lambda x, y: x < y
        constraints.add_unary_constraint(t, lt, 3)
        constraints.add_unary_constraint(wa, lt, 3)
        constraints.add_unary_constraint(nt, lt, 3)
        constraints.add_unary_constraint(sa, lt, 3)
        constraints.add_unary_constraint(q, lt, 3)
        constraints.add_unary_constraint(nsw, lt, 3)
        constraints.add_unary_constraint(v, lt, 3)

        ne = lambda x, y: x != y
        # We're assuming that the Tasmanians are 'patriotic', as the book mentions.
        # This is just so we don't have to arbitrarily choose our own color for the variable T.
        # (If we did neither, it wouldn't be present in the CSP formulation at all).
        constraints.add_binary_constraint(t, ne, v)
        constraints.add_binary_constraint(wa, ne, nt)
        constraints.add_binary_constraint(wa, ne, sa)
        constraints.add_binary_constraint(nt, ne, q)
        constraints.add_binary_constraint(nt, ne, sa)
        constraints.add_binary_constraint(sa, ne, q)
        constraints.add_binary_constraint(sa, ne, nsw)
        constraints.add_binary_constraint(sa, ne, v)
        constraints.add_binary_constraint(q, ne, nsw)
        constraints.add_binary_constraint(nsw, ne, v)
        self.assertTrue(all_constraints_satisfied(variables, constraints, solution))


class CSPSolveAustraliaMapColoringNoForwardChecking(unittest.TestCase):
    def test_csp_solve_australia_map_coloring_no_forward_checking(self):
        test_csp = CSP.from_file('Test Australia.txt')
        solution = test_csp.solve(False)

        # Variable-related assertions.
        num_of_vars = 10  # We're counting the color-variables too.
        domain_upper_bound = num_of_vars - 1
        var_domain = set(xrange(domain_upper_bound))
        red = Variable('red', var_domain)
        green = Variable('green', var_domain)
        blue = Variable('blue', var_domain)
        wa = Variable('WA', var_domain)
        t = Variable('T', var_domain)
        nt = Variable('NT', var_domain)
        sa = Variable('SA', var_domain)
        q = Variable('Q', var_domain)
        nsw = Variable('NSW', var_domain)
        v = Variable('V', var_domain)
        variables = [red, green,
                     blue, wa,
                     t, nt,
                     sa, q,
                     nsw, v]
        self.assertTrue(all_variables_assigned(variables, solution))
        self.assertTrue(domain_values_assigned(set(range(0, domain_upper_bound)), solution))

        # Constraint-related assertion.
        constraints = Constraints()
        eq = lambda x, y: x == y
        constraints.add_unary_constraint(red, eq, 0)
        constraints.add_unary_constraint(green, eq, 1)
        constraints.add_unary_constraint(blue, eq, 2)

        lt = lambda x, y: x < y
        constraints.add_unary_constraint(t, lt, 3)
        constraints.add_unary_constraint(wa, lt, 3)
        constraints.add_unary_constraint(nt, lt, 3)
        constraints.add_unary_constraint(sa, lt, 3)
        constraints.add_unary_constraint(q, lt, 3)
        constraints.add_unary_constraint(nsw, lt, 3)
        constraints.add_unary_constraint(v, lt, 3)

        ne = lambda x, y: x != y
        # We're assuming that the Tasmanians are 'patriotic', as the book mentions.
        # This is just so we don't have to arbitrarily choose our own color for the variable T.
        # (If we did neither, it wouldn't be present in the CSP formulation at all).
        constraints.add_binary_constraint(t, ne, v)
        constraints.add_binary_constraint(wa, ne, nt)
        constraints.add_binary_constraint(wa, ne, sa)
        constraints.add_binary_constraint(nt, ne, q)
        constraints.add_binary_constraint(nt, ne, sa)
        constraints.add_binary_constraint(sa, ne, q)
        constraints.add_binary_constraint(sa, ne, nsw)
        constraints.add_binary_constraint(sa, ne, v)
        constraints.add_binary_constraint(q, ne, nsw)
        constraints.add_binary_constraint(nsw, ne, v)
        self.assertTrue(all_constraints_satisfied(variables, constraints, solution))


class SolveCSPSudokuWithForwardChecking(ConstraintTestCase):
    def test_solve_csp_sudoku_with_forward_checking(self):
        actual_solution_string = solve_csp('Test Sudoku.txt', '0')
        expected_solution_string = (
            'A1=4\n'
            'A2=8\n'
            'A3=3\n'
            'A4=9\n'
            'A5=2\n'
            'A6=1\n'
            'A7=6\n'
            'A8=5\n'
            'A9=7\n'
            'B1=9\n'
            'B2=6\n'
            'B3=7\n'
            'B4=3\n'
            'B5=4\n'
            'B6=5\n'
            'B7=8\n'
            'B8=2\n'
            'B9=1\n'
            'C1=2\n'
            'C2=5\n'
            'C3=1\n'
            'C4=8\n'
            'C5=7\n'
            'C6=6\n'
            'C7=4\n'
            'C8=9\n'
            'C9=3\n'
            'D1=5\n'
            'D2=4\n'
            'D3=8\n'
            'D4=1\n'
            'D5=3\n'
            'D6=2\n'
            'D7=9\n'
            'D8=7\n'
            'D9=6\n'
            'E1=7\n'
            'E2=2\n'
            'E3=9\n'
            'E4=5\n'
            'E5=6\n'
            'E6=4\n'
            'E7=1\n'
            'E8=3\n'
            'E9=8\n'
            'F1=1\n'
            'F2=3\n'
            'F3=6\n'
            'F4=7\n'
            'F5=9\n'
            'F6=8\n'
            'F7=2\n'
            'F8=4\n'
            'F9=5\n'
            'G1=3\n'
            'G2=7\n'
            'G3=2\n'
            'G4=6\n'
            'G5=8\n'
            'G6=9\n'
            'G7=5\n'
            'G8=1\n'
            'G9=4\n'
            'H1=8\n'
            'H2=1\n'
            'H3=4\n'
            'H4=2\n'
            'H5=5\n'
            'H6=3\n'
            'H7=7\n'
            'H8=6\n'
            'H9=9\n'
            'I1=6\n'
            'I2=9\n'
            'I3=5\n'
            'I4=4\n'
            'I5=1\n'
            'I6=7\n'
            'I7=3\n'
            'I8=8\n'
            'I9=2'
        )
        self.assertEqual(expected_solution_string, actual_solution_string)


class SolveCSPSudokuWithForwardChecking(ConstraintTestCase):
    def test_solve_csp_sudoku_with_forward_checking(self):
        actual_solution_string = solve_csp('Test Sudoku.txt', '1')
        expected_solution_string = (
            'A1=4\n'
            'A2=8\n'
            'A3=3\n'
            'A4=9\n'
            'A5=2\n'
            'A6=1\n'
            'A7=6\n'
            'A8=5\n'
            'A9=7\n'
            'B1=9\n'
            'B2=6\n'
            'B3=7\n'
            'B4=3\n'
            'B5=4\n'
            'B6=5\n'
            'B7=8\n'
            'B8=2\n'
            'B9=1\n'
            'C1=2\n'
            'C2=5\n'
            'C3=1\n'
            'C4=8\n'
            'C5=7\n'
            'C6=6\n'
            'C7=4\n'
            'C8=9\n'
            'C9=3\n'
            'D1=5\n'
            'D2=4\n'
            'D3=8\n'
            'D4=1\n'
            'D5=3\n'
            'D6=2\n'
            'D7=9\n'
            'D8=7\n'
            'D9=6\n'
            'E1=7\n'
            'E2=2\n'
            'E3=9\n'
            'E4=5\n'
            'E5=6\n'
            'E6=4\n'
            'E7=1\n'
            'E8=3\n'
            'E9=8\n'
            'F1=1\n'
            'F2=3\n'
            'F3=6\n'
            'F4=7\n'
            'F5=9\n'
            'F6=8\n'
            'F7=2\n'
            'F8=4\n'
            'F9=5\n'
            'G1=3\n'
            'G2=7\n'
            'G3=2\n'
            'G4=6\n'
            'G5=8\n'
            'G6=9\n'
            'G7=5\n'
            'G8=1\n'
            'G9=4\n'
            'H1=8\n'
            'H2=1\n'
            'H3=4\n'
            'H4=2\n'
            'H5=5\n'
            'H6=3\n'
            'H7=7\n'
            'H8=6\n'
            'H9=9\n'
            'I1=6\n'
            'I2=9\n'
            'I3=5\n'
            'I4=4\n'
            'I5=1\n'
            'I6=7\n'
            'I7=3\n'
            'I8=8\n'
            'I9=2'
        )
        self.assertEqual(expected_solution_string, actual_solution_string)


class CSPFromFileSudoku(ConstraintTestCase):
    def test_csp_from_file_sudoku(self):
        csp = CSP.from_file('Test Sudoku.txt')
        
        expected_variable_names = [
            'A1',
            'A2',
            'A3',
            'A4',
            'A5',
            'A6',
            'A7',
            'A8',
            'A9',

            'B1',
            'B2',
            'B3',
            'B4',
            'B5',
            'B6',
            'B7',
            'B8',
            'B9',

            'C1',
            'C2',
            'C3',
            'C4',
            'C5',
            'C6',
            'C7',
            'C8',
            'C9',

            'D1',
            'D2',
            'D3',
            'D4',
            'D5',
            'D6',
            'D7',
            'D8',
            'D9',

            'E1',
            'E2',
            'E3',
            'E4',
            'E5',
            'E6',
            'E7',
            'E8',
            'E9',

            'F1',
            'F2',
            'F3',
            'F4',
            'F5',
            'F6',
            'F7',
            'F8',
            'F9',

            'G1',
            'G2',
            'G3',
            'G4',
            'G5',
            'G6',
            'G7',
            'G8',
            'G9',

            'H1',
            'H2',
            'H3',
            'H4',
            'H5',
            'H6',
            'H7',
            'H8',
            'H9',

            'I1',
            'I2',
            'I3',
            'I4',
            'I5',
            'I6',
            'I7',
            'I8',
            'I9'
        ]
        actual_variable_names = [var.name for var in csp.variables]
        self.assertListEqual(sorted(actual_variable_names), sorted(expected_variable_names))

        given_variables = [
            Variable('A3', set([3])),
            Variable('A5', set([2])),
            Variable('A7', set([6])),

            Variable('B1', set([9])),
            Variable('B4', set([3])),
            Variable('B6', set([5])),
            Variable('B9', set([1])),

            Variable('C3', set([1])),
            Variable('C4', set([8])),
            Variable('C6', set([6])),
            Variable('C7', set([4])),

            Variable('D3', set([8])),
            Variable('D4', set([1])),
            Variable('D6', set([2])),
            Variable('D7', set([9])),

            Variable('E1', set([7])),
            Variable('E9', set([8])),

            Variable('F3', set([6])),
            Variable('F4', set([7])),
            Variable('F6', set([8])),
            Variable('F7', set([2])),

            Variable('G3', set([2])),
            Variable('G4', set([6])),
            Variable('G6', set([9])),
            Variable('G7', set([5])),

            Variable('H1', set([8])),
            Variable('H4', set([2])),
            Variable('H6', set([3])),
            Variable('H9', set([9])),

            Variable('I3', set([5])),
            Variable('I5', set([1])),
            Variable('I7', set([3]))
        ]
        actual_variables = csp.variables
        
        for given_var in given_variables:
            for actual_var in actual_variables:
                if actual_var.name == given_var.name:
                    self.assertSetEqual(actual_var.domain, given_var.domain)
        
        solution_assignment = {
            Variable('A1', None): 4,
            Variable('A2', None): 8,
            Variable('A3', None): 3,
            Variable('A4', None): 9,
            Variable('A5', None): 2,
            Variable('A6', None): 1,
            Variable('A7', None): 6,
            Variable('A8', None): 5,
            Variable('A9', None): 7,

            Variable('B1', None): 9,
            Variable('B2', None): 6,
            Variable('B3', None): 7,
            Variable('B4', None): 3,
            Variable('B5', None): 4,
            Variable('B6', None): 5,
            Variable('B7', None): 8,
            Variable('B8', None): 2,
            Variable('B9', None): 1,

            Variable('C1', None): 2,
            Variable('C2', None): 5,
            Variable('C3', None): 1,
            Variable('C4', None): 8,
            Variable('C5', None): 7,
            Variable('C6', None): 6,
            Variable('C7', None): 4,
            Variable('C8', None): 9,
            Variable('C9', None): 3,

            Variable('D1', None): 5,
            Variable('D2', None): 4,
            Variable('D3', None): 8,
            Variable('D4', None): 1,
            Variable('D5', None): 3,
            Variable('D6', None): 2,
            Variable('D7', None): 9,
            Variable('D8', None): 7,
            Variable('D9', None): 6,

            Variable('E1', None): 7,
            Variable('E2', None): 2,
            Variable('E3', None): 9,
            Variable('E4', None): 5,
            Variable('E5', None): 6,
            Variable('E6', None): 4,
            Variable('E7', None): 1,
            Variable('E8', None): 3,
            Variable('E9', None): 8,

            Variable('F1', None): 1,
            Variable('F2', None): 3,
            Variable('F3', None): 6,
            Variable('F4', None): 7,
            Variable('F5', None): 9,
            Variable('F6', None): 8,
            Variable('F7', None): 2,
            Variable('F8', None): 4,
            Variable('F9', None): 5,

            Variable('G1', None): 3,
            Variable('G2', None): 7,
            Variable('G3', None): 2,
            Variable('G4', None): 6,
            Variable('G5', None): 8,
            Variable('G6', None): 9,
            Variable('G7', None): 5,
            Variable('G8', None): 1,
            Variable('G9', None): 4,

            Variable('H1', None): 8,
            Variable('H2', None): 1,
            Variable('H3', None): 4,
            Variable('H4', None): 2,
            Variable('H5', None): 5,
            Variable('H6', None): 3,
            Variable('H7', None): 7,
            Variable('H8', None): 6,
            Variable('H9', None): 9,

            Variable('I1', None): 6,
            Variable('I2', None): 9,
            Variable('I3', None): 5,
            Variable('I4', None): 4,
            Variable('I5', None): 1,
            Variable('I6', None): 7,
            Variable('I7', None): 3,
            Variable('I8', None): 8,
            Variable('I9', None): 2
        }
        self.assert_all_constraints_satisfied(actual_variables, csp.constraints, solution_assignment)


if __name__ == "__main__":
    unittest.main()
