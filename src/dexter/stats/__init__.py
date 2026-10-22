"""
Statistics Module

Provides probability distributions, random variables, and statistical utilities.
"""

from typing import TYPE_CHECKING

from .._lazy import lazy_exports

_EXPORTS = {
    'Distribution': ('distribution', "Base class: pdf(), cdf(), draw(); sums of distributions"),
    'Normal': ('distribution', "Normal(mean, var)"),
    'Uniform': ('distribution', "Uniform(a, b)"),
    'Binomial': ('distribution', "Binomial(n, p)"),
    'Geometric': ('distribution', "Geometric(p): trials up to the first success"),
    'NegativeBinomial': ('distribution', "NegativeBinomial(r, p): trials up to the r-th success"),
    'Poisson': ('distribution', "Poisson(mu)"),
    'Exponential': ('distribution', "Exponential(intensity)"),
    'Gamma': ('distribution', "Gamma(theta, r) with scale theta and shape r"),
    'ChiSquare': ('distribution', "ChiSquare(df)"),
    'Unknown': ('distribution', "Distribution from a mean, variance and custom pdf"),
    'RV': ('rv', "Random variable over a distribution; observe(), pdf()"),
    'Sample': ('sample', "Collection of random variables; observe(), expected_value"),
    'P': ('funcs', "P(rv, c): probability (density) of rv at c"),
    'E': ('funcs', "E(rv): expected value of an RV or Sample"),
    'recognize': ('funcs', "Best-fitting distribution for data as (name, params, p_value)"),
}

__all__ = list(_EXPORTS)
__getattr__, __dir__, help = lazy_exports(__name__, _EXPORTS)

if TYPE_CHECKING:
    from .distribution import (
        Distribution, Normal, Uniform, Binomial, Geometric,
        NegativeBinomial, Poisson, Exponential, Gamma, ChiSquare, Unknown
    )
    from .rv import RV
    from .sample import Sample
    from .funcs import P, E, recognize
