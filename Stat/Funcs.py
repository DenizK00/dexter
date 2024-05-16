import RV

def P(rv:RV, c):
    return rv.pdf(c)

def E(rv:RV):
    return rv.expectation

