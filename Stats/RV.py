
class RV:
    _ids = 0

    def __init__(self, distribution:"Distribution"=None, name=None):
        RV._ids += 1

        self._id = RV._ids
        self.distribution = distribution
        self.name = name if name else self._id

        # actually either a pdf and support OR distribution is required

    def observe(self):
        return self.distribution.dist.rvs()

    
    def __add__(self, other):
        lhs, rhs = self.distribution, other.distribution
        match (lhs, rhs):
            case (None, None):
                pass
            case _:
                lhs.__add__(rhs) # can be wrong
            


    def __str__(self):
        return self.name