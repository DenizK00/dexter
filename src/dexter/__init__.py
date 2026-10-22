"""
Dexter Toolkit - Data Experimentation and Tinkering Kit

A small Python toolkit for optimization, simulation, statistics,
visualization and model selection experiments.

Subpackages and the classes below are imported on first use, so
`import dexter` does not load pyomo, scipy, sympy, pandas or plotly.
Call dexter.help() for an overview.
"""

from typing import TYPE_CHECKING

from ._lazy import lazy_exports

__version__ = "2.0.0"
__author__ = "Deniz"
__email__ = "denizkurtaran00@gmail.com"

_EXPORTS = {
    # Submodules
    'ml': (None, "Automated classifier selection (needs the [ml] extra)"),
    'optimization': (None, "Linear programs from equation strings, solved with Pyomo"),
    'simulation': (None, "Discrete event simulation (SimPy) and a grid world"),
    'stats': (None, "Probability distributions and random variables"),
    'visualization': (None, "3D plotting of vectors, surfaces and matrices (Plotly)"),

    # Common classes
    'pick_classifier': ('ml', "Pick and tune the best classifier for a DataFrame"),
    'Problem': ('optimization', "Optimization problem: objective plus constraints"),
    'Equation': ('optimization', "Linear (in)equality parsed from a string"),
    'Solution': ('optimization', "Variable values returned by Problem.solve()"),
    'SimManager': ('simulation', "Run SimPy processes and resources"),
    'Grid': ('simulation', "Text grid with an agent, for agent experiments"),
    'Normal': ('stats', "Normal distribution"),
    'Uniform': ('stats', "Continuous uniform distribution"),
    'Binomial': ('stats', "Binomial distribution"),
    'Poisson': ('stats', "Poisson distribution"),
    'Exponential': ('stats', "Exponential distribution"),
    'Space': ('visualization', "Interactive 3D Plotly space"),
}

__all__ = list(_EXPORTS)
__getattr__, __dir__, help = lazy_exports(__name__, _EXPORTS)

if TYPE_CHECKING:  # lets IDEs and type checkers see the real names
    from . import ml, optimization, simulation, stats, visualization
    from .ml import pick_classifier
    from .optimization import Problem, Equation, Solution
    from .simulation import SimManager, Grid
    from .stats import Normal, Uniform, Binomial, Poisson, Exponential
    from .visualization import Space
