class Sample:
    def __init__(self, rvs:list["RV"]):
        self.rvs = rvs

    def observe(self):
        return np.array([rv.realize() for rv in self.rvs])

    def __str__(self):
        return []
