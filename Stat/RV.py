from Distribution import *

class RV:
    def __init__(self, distr:"Distribution", name=None):
        self.distribution = distr
        self.name = name

    def realize(self):
        return self.distribution.dist.rvs()
    
    def __str__(self):
        return self.name