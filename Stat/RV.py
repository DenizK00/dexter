from Distribution import *

class RV:
    def __init__(self, distr:"Distribution"):
        self.distribution = distr

    def realize(self):
        return self.distribution.dist.rvs()

    