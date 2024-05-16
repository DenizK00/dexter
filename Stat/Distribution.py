import numpy as np
import math
from RV import *

class Distribution:

    def draw(self):
        return RV(distr=self)


class Normal(Distribution):
    def __init__(self, mean:float, var:float):
        self.mean = mean
        self.var = var
        self.std = np.sqrt(self.var) #Add Handling negative variance
    
    def __str__(self):
        return f"N(mean={self.mean}, variance={self.var})"
    
    def pdf(self):
        return
    
    def draw(sefl, n=1):
        return RV(pdf=self.pdf)


class Uniform(Distribution):
    def __init__(self, a, b):
        self.a, self,b = a, b
        self.E = (self.a+self.b)/2
    
    def pdf(self, x):
        if x < self.a or x > self.b:
            raise NameError(f"{x} is not in the support of pdf")
        return 1/(self.b-self.a)
    
    def CDF(self, x):
        return x/(self.b-self.a)
    
    

class Binomial(Distribution):
    def __init__(self, n:int, p:float):
        self.n = n
        self.p = p

    def pdf(self, x):
        return math.comb(self.n, x) * (self.p**x)(1 - self.p)^(self.n - x)

class Poisson(Distribution):
    def __init__(self, mu):
        pass

class Exponential(Distribution):
    def __init__(self, intensity):
        self.intensity = intensity
        self.Expectation = self.intensity

    def mgf(self, t):
        return self.intensity / (self.intensity - t)



Distr = Distribution
N = Normal


if __name__ == "__main__":
    X = RV(distr=Binomial(n=20, p=0.1))
    print(X.distribution)
