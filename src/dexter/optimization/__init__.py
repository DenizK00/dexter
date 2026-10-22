"""
Optimization Module

Provides mathematical optimization tools using Pyomo framework.
"""

from typing import TYPE_CHECKING

from .._lazy import lazy_exports

_EXPORTS = {
    'Problem': ('problem', "Build a model from objective and constraint strings; solve(), sensitivity()"),
    'Equation': ('equation', "Linear (in)equality from a string; coefficients, add_slack(), visualize()"),
    'Solution': ('solution', "Variable values of a solved problem; feasibility(), to_numpy_array()"),
}

__all__ = list(_EXPORTS)
__getattr__, __dir__, help = lazy_exports(__name__, _EXPORTS)

if TYPE_CHECKING:
    from .problem import Problem
    from .equation import Equation
    from .solution import Solution
