import numpy as np
import pytest
import sympy

from dexter.optimization import Equation


def test_parsing_1():
    eq = Equation("2*x + 5*y + 3*z_1 >= 5", name="example")

    assert eq.name == "example"
    assert eq.var_to_coef == {"x": 2, "y": 5, "z_1": 3}
    assert eq["y"] == 5
    assert eq["missing"] == 0


def test_parsing_2():
    rand_coefs = np.linspace(1, 20, 10)
    eq_str = " + ".join(f"{round(coef)}*x_{i}" for i, coef in enumerate(rand_coefs, 1)) + " <= 250"

    eq = Equation(eq_str)

    assert eq.var_to_coef == {f"x_{i}": round(rand_coefs[i - 1]) for i in range(1, 11)}


def test_invalid_operator():
    with pytest.raises(ValueError):
        Equation("x + y")


def test_incomplete_equation():
    with pytest.raises(sympy.SympifyError):
        Equation("3*x_1 + 5*x_2 + ")


def test_add_slack():
    eq = Equation("x + y <= 4").add_slack()

    assert isinstance(eq.expr, sympy.Eq)
    assert eq["slack"] == 1
