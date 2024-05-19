import numpy as np
import math
from RV import RV
from Sample import Sample
import scipy.stats as sci


class Distribution:
    
    def plot_pdf(self):
        pass

    def plot_cdf(self):
        pass

    def draw(self, n=1):
        if n==1:
            return RV(distr=self)
        else:
            return Sample([RV(distr=self) for i in range(n)])


class Normal(Distribution):
    def __init__(self, mean:float, var:float):
        self.mean = mean
        self.var = var
        self.std = np.sqrt(self.var) #Add Handling negative variance
        self.dist = sci.norm(loc=self.mean, scale=self.std)
        self.support = (-np.inf, np.inf)

    def __str__(self):
        return f"N(mean={self.mean}, variance={self.var})"
    
    def pdf(self, x):
        return self.dist.pdf(x)
    
    def cdf(self, x):
        return self.dist.cdf(x)
    
    def mgf(self, t):
        return self.dist.mgf(t)
    
    def __add__(self, other):
        lhs, rhs = self.distribution, other.distribution
        match rhs.distribution:
            case Normal():
                return Normal(self.mean + other.mean, self.var + other.var)


class Uniform(Distribution):
    def __init__(self, a, b):
        self.a, self.b = a, b
        self.E = (self.a+self.b)/2
        self.dist = sci.uniform(loc=a, scale=b-a)
    
    def pdf(self, x):
        return self.dist.pdf(x)
    
    def cdf(self, x):
        return self.dist.cdf(x)
    
    def mgf(self, x):
        return self.dist.mgf(x)


class Binomial(Distribution):
    def __init__(self, n:int, p:float):
        self.n = n
        self.p = p
        self.dist = sci.binom(n=self.n, p=self.p)

    def pmf(self, x):
        return self.dist.pmf(x)
    
    def cdf(self, x):
        return self.dist.cdf(x)
    
    def __add__(self, other):
        lhs, rhs = self.distribution, other.distribution
        match rhs:
            case Binomial() if lhs.p == rhs.p:
                return Binomial(n=lhs.n+rhs.n, p=lhs.p)
                # check whether it's true also consider the case of unequal p's


class Poisson(Distribution):
    def __init__(self, mu):
        self.mu = mu
        self.dist = sci.poisson()

    def pmf(self, x):
        return self.dist.pmf(x)
    
    def cdf(self, x):
        return self.dist.cdf(x)


class Exponential(Distribution):
    def __init__(self, intensity: float):
        self.intensity = intensity
        self.dist = sci.expon(scale=1/intensity)

    def pdf(self, x):
        return self.dist.pdf(x)
    
    def cdf(self, x):
        return self.dist.cdf(x)

    def mgf(self, t):
        return self.intensity / (self.intensity - t)


class Gamma(Distribution):
    def __init__(self, theta, r):
        self.theta = theta
        self.r = r
        self.dist = sci.gamma(0, 1) # Change the parameters

    def pdf(self, x):
        return self.dist.pdf(x)
    
    def cdf(self, x):
        return self.dist.cdf(x)
    


Distr = Distribution
N = Normal

if __name__ == "__main__":
    X = RV(distr=Binomial(n=20, p=0.1))
    print(X.distribution)
