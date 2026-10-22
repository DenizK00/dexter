"""
Dexter Toolkit - Data Experimentation and Tinkering Kit

A small Python toolkit for optimization, simulation, statistics,
visualization and model selection experiments.
"""

__version__ = "2.0.0"
__author__ = "Deniz"
__email__ = "denizkurtaran00@gmail.com"

import importlib

from . import optimization, simulation, stats, visualization

# Convenience imports for commonly used classes
from .optimization import Problem, Equation, Solution
from .simulation import SimManager, Grid
from .stats import Normal, Uniform, Binomial, Poisson, Exponential
from .visualization import Space

__all__ = [
    # Submodules
    'ml',
    'optimization',
    'simulation',
    'stats',
    'visualization',

    # Common classes
    'pick_classifier',
    'Problem',
    'Equation',
    'Solution',
    'SimManager',
    'Grid',
    'Normal',
    'Uniform',
    'Binomial',
    'Poisson',
    'Exponential',
    'Space',
]


def __getattr__(name):
    # dexter.ml needs the optional [ml] extra, so it is only imported on use
    if name in ("ml", "pick_classifier"):
        ml = importlib.import_module(".ml", __name__)
        return ml if name == "ml" else ml.pick_classifier
    raise AttributeError(f"module 'dexter' has no attribute {name!r}")
