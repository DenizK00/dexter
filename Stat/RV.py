from Distribution import *
from itertools import count
    
class RV:
    _ids = count(0)
    def __init__(self, distribution:"Distribution", name=None):
        self.distribution = distribution
        self.name = name
        if self.name == None:
            self._id
        

    def observe(self):
        return self.distribution.dist.rvs()
    
    def __add__(self, other):
        lhs, rhs = self.distribution, other.distribution
        match (lhs, rhs):
            # Binomial
            case (Binomial(), Binomial()) if lhs.distribution.p == rhs.distribution.p:
                return RV(Binomial(n=(lhs.distribution.n + rhs.distribution.n), p=lhs.distribution.p))
                # check whether it's true also consider the case of unequal p's

            

    def __str__(self):
        return self.name