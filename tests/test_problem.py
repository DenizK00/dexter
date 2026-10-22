import numpy as np
import pytest

from dexter.optimization import Problem, Solution


@pytest.fixture
def problem():
    return Problem("max 3*x + 2*y", ["x + y <= 4", "x + 3*y <= 6"])


def test_construct(problem):
    assert problem.goal == "max"
    assert problem.variables == ["x", "y"]
    np.testing.assert_array_equal(problem.constraint_matrix, [[1, 1], [1, 3]])


def test_objective_value_from_dict(problem):
    assert problem({"x": 4, "y": 0}) == 12


def test_objective_value_from_solution(problem):
    assert problem(Solution(["x", "y"], [1, 2])) == 7


def test_solution_lookup():
    sol = Solution.from_dict({"x": 4.0, "y": 0.0})

    assert sol["x"] == 4.0
    assert sol[1] == 0.0
    assert "y" in sol
    assert sol.basis == [0]
    assert sol.feasibility()
    assert not Solution(["x"], [-1]).feasibility()
