"""
Script Name: funcs.py
Author: Deniz
Created: 2024-05-20 14:36:44
Description: Functions that use multiple objects
"""

import scipy.stats as sci


def P(rv: "RV", c):
    return rv.pdf(c)


def E(rv: "RV|Sample"):
    return rv.expected_value


def recognize(data):
    """Fit candidate distributions to ``data`` and return the best one by the
    Kolmogorov-Smirnov test, as ``(name, params, p_value)``."""
    distributions = [sci.norm, sci.expon, sci.uniform]

    best = None
    for dist in distributions:
        params = dist.fit(data)
        _, p_value = sci.kstest(data, dist.name, args=params)
        if best is None or p_value > best[2]:
            best = (dist.name, params, p_value)

    return best
