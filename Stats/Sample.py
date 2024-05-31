from .utils import *

class Sample:
    def __init__(self, rvs:list["RV"]):
        self.rvs = rvs

    def observe(self):
        return np.array([rv.observe() for rv in self.rvs])

    def __str__(self):
        return []
