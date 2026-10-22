"""
Script Name: rv.py
Author: Deniz
Created: 2024-05-15 14:33:20
Description: Random variable class that supports abstract r.v.s
"""


class RV:
    _ids = 0

    def __init__(self, distribution: "Distribution" = None, name=None):
        RV._ids += 1

        self._id = RV._ids
        self.distribution = distribution
        self.name = name if name else f"X{self._id}"

    @property
    def expected_value(self):
        return self.distribution.expectation

    def pdf(self, x):
        return self.distribution.pdf(x)

    def observe(self):
        return self.distribution.dist.rvs()

    def __add__(self, other):
        if self.distribution is None or other.distribution is None:
            raise TypeError("Both random variables need a distribution to be added.")
        # raises TypeError when the sum has no closed form
        return RV(self.distribution + other.distribution)

    def __str__(self):
        return str(self.name)
