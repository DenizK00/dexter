"""
Script Name: sample.py
Author: Deniz
Created: 2024-05-22 22:05:13
Description: A collection of random variables
"""

import numpy as np


class Sample:
    trials = 120  # observations averaged by expected_value

    def __init__(self, rvs: list["RV"]):
        self.rvs = rvs

    def __len__(self):
        return len(self.rvs)

    @property
    def expected_value(self):
        return np.mean([np.mean(self.observe()) for _ in range(self.trials)])

    def observe(self):
        return np.array([rv.observe() for rv in self.rvs])

    def __str__(self):
        return f"Sample({', '.join(str(rv) for rv in self.rvs)})"
