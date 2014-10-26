__author__ = 'dash'

import unittest

from csp_solver import *


class VariableHashing(unittest.TestCase):
    def test_hashes_based_on_name(self):
        name = "Variable Name"
        name_hash = hash(name)
        var = Variable(name, None)
        var_hash = hash(var)

        self.assertEqual(name_hash, var_hash, "You're not hashing Variables based on their names!")


class ConstraintsArcsInvolvingHasArcs(unittest.TestCase):
    def test_arcs_involving_returns_arcs_when_has_arcs(self):
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


class ConstraintsArcsInvolvingHasNoArcs(unittest.TestCase):
    def test_arcs_involving_returns_no_arcs_when_has_no_arcs(self):
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
        expected = "X = 5\nY = 20"
        or_expected = "Y = 20\nX = 5"  # Ordering seems to be non-deterministic.
        actual = Assignment.as_string(test_assignment)
        self.assertTrue(expected == actual or or_expected == actual)


class CSPSolveEmptyCSP(unittest.TestCase):
    def test_csp_solve_empty_csp(self):
        test_csp = CSP([], Constraints())
        expected = {}
        actual = test_csp.solve(False)
        self.assertDictEqual(expected, actual)


class TestCSPFromFile(unittest.TestCase):
    def test_this(self):
        forward_checking = False
        with open('Test.txt', 'r') as problem_file:
            csp = CSP.from_file(problem_file)
            solution = csp.solve(forward_checking)
            print(Assignment.as_string(solution))


if __name__ == "__main__":
    unittest.main()
