__author__ = 'Christopher Raleigh and Anthony Ferrero'

import unittest

from csp_solver import *


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
        actual = solve_csp('test_uland.txt', '1')
        # Doesn't output exactly what the assignment says it should, but it's still technically correct.
        expected = 'ME=0\nShortz=2\nUland=1'
        self.assertEqual(actual, expected)


class CSPSolveUlandNoForwardChecking(unittest.TestCase):
    def test_csp_from_file_uland(self):
        actual = solve_csp('test_uland.txt', '0')
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


class TestCSPFromFile(unittest.TestCase):
    def test_this(self):
        forward_checking = False
        csp = CSP.from_file('Test.txt')
        solution = csp.solve(forward_checking)
        print(Solution.as_string(solution))


if __name__ == "__main__":
    unittest.main()
