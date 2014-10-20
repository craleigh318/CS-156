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
        constraints.add_constraint(first_var, None, second_var)

        expected = [(first_var, second_var)]
        actual = constraints.arcs_involving(first_var)
        self.assertSequenceEqual(expected, actual)

        actual = constraints.arcs_involving(second_var)
        self.assertSequenceEqual(expected, actual)


class ConstraintsArcsInvolvingHasNoArcs(unittest.TestCase):
    def test_arcs_involving_returns_no_arcs_when_has_no_arcs(self):
        constraints = Constraints()
        unconstrained_var = Variable("Not Constrained", None)
        expected = []
        actual = constraints.arcs_involving(unconstrained_var)
        self.assertSequenceEqual(expected, actual)


class ConstraintsConstraintSatisfiedHasConstraint(unittest.TestCase):
    def test_constraints_satisfied_returns_true_when_relation_is_true(self):
        constraints = Constraints()
        first_var = Variable("First!", None)
        second_var = Variable("Second!", None)
        relation = Relation.as_function(Relation.greater_than)
        constraints.add_constraint(first_var, relation, second_var)

        result = constraints.constraint_satisfied(first_var, 9999999999999, second_var, 0)
        self.assertTrue(result)


class ConstraintsConstraintNotSatisfiedHasConstraint(unittest.TestCase):
    def test_constraints_satisfied_returns_false_when_relation_is_false(self):
        constraints = Constraints()
        first_var = Variable("First!", None)
        second_var = Variable("Second!", None)
        relation = Relation.as_function(Relation.greater_than)
        constraints.add_constraint(first_var, relation, second_var)

        result = constraints.constraint_satisfied(first_var, 0, second_var, 48932749874)
        self.assertFalse(result)


class ConstraintsConstaintSatisfiedHasNoConstraint(unittest.TestCase):
    def test_constraints_satisfied_raises_value_error_when_has_no_constraint(self):
        constraints = Constraints()
        first_var = Variable("First!", None)
        second_var = Variable("Second!", None)
        self.assertRaises(ValueError, constraints.constraint_satisfied, first_var, 0, second_var, 0)


class TestCSPFromFile(unittest.TestCase):
    def test_this(self):
        forward_checking = sys.argv[2]
        with open('test.txt', 'r') as problem_file:
            csp = CSP.from_file(problem_file)
            solution = csp.solve(False)
            for variable in solution:
                print(variable.name)


if __name__ == "__main__":
    unittest.main()