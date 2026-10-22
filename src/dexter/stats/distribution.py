"""
Script Name: distribution.py
Author: Deniz
Created: 2024-05-10 20:34:05
Description: Abstract distributions
"""

import numpy as np
import scipy.stats as sci

# Everything assumes independence


class Distribution:
    """Base class. Subclasses set ``self.dist`` to a frozen scipy distribution
    and ``self.expectation``; adding two distributions returns the
    distribution of the sum when it has a closed form."""

    discrete = False

    def pdf(self, x):
        return self.dist.pmf(x) if self.discrete else self.dist.pdf(x)

    def cdf(self, x):
        return self.dist.cdf(x)

    def draw(self, n=1):
        from .rv import RV
        from .sample import Sample

        if n == 1:
            return RV(distribution=self)
        return Sample([RV(distribution=self) for _ in range(n)])

    def __add__(self, other):
        return NotImplemented


class Normal(Distribution):
    def __init__(self, mean: float, var: float):
        if var < 0:
            raise ValueError("Variance must be non-negative.")
        self.mean = mean
        self.var = var
        self.std = np.sqrt(self.var)
        self.dist = sci.norm(loc=self.mean, scale=self.std)
        self.expectation = self.mean
        self.support = (-np.inf, np.inf)

    def __str__(self):
        return f"N(mean={self.mean}, variance={self.var})"

    def mgf(self, t):
        return np.exp(self.mean * t + self.var * t**2 / 2)

    def __add__(self, other):
        match other:
            case Normal():
                return Normal(self.mean + other.mean, self.var + other.var)
            case float() | int():
                return Normal(self.mean + other, self.var)
        return NotImplemented

    def __mul__(self, other):
        if not isinstance(other, (float, int)):
            return NotImplemented
        return Normal(self.mean * other, self.var * other**2)

    __rmul__ = __mul__


class Uniform(Distribution):
    def __init__(self, a, b):
        self.a, self.b = a, b
        self.dist = sci.uniform(loc=a, scale=b - a)
        self.expectation = (self.a + self.b) / 2

    def mgf(self, t):
        if t == 0:
            return 1.0
        return (np.exp(t * self.b) - np.exp(t * self.a)) / (t * (self.b - self.a))


class Binomial(Distribution):
    discrete = True

    def __init__(self, n: int, p: float):
        self.n = n
        self.p = p
        self.dist = sci.binom(n=self.n, p=self.p)
        self.expectation = self.n * self.p

    def __add__(self, other):
        match other:
            case Binomial() if self.p == other.p:
                return Binomial(n=self.n + other.n, p=self.p)
        return NotImplemented


class Geometric(Distribution):
    """Number of trials up to and including the first success."""

    discrete = True

    def __init__(self, p):
        self.p = p
        self.dist = sci.geom(p)
        self.expectation = 1 / self.p

    def __add__(self, other):
        match other:
            case Geometric() if self.p == other.p:
                return NegativeBinomial(r=2, p=self.p)
            case NegativeBinomial() if self.p == other.p:
                return NegativeBinomial(r=other.r + 1, p=self.p)
        return NotImplemented


class NegativeBinomial(Distribution):
    """Number of trials up to and including the r-th success."""

    discrete = True

    def __init__(self, r, p):
        self.r = r
        self.p = p
        # scipy counts failures before the r-th success; shift by r to count trials
        self.dist = sci.nbinom(r, p, loc=r)
        self.expectation = self.r / self.p

    def __add__(self, other):
        match other:
            case NegativeBinomial() if self.p == other.p:
                return NegativeBinomial(r=self.r + other.r, p=self.p)
            case Geometric() if self.p == other.p:
                return NegativeBinomial(r=self.r + 1, p=self.p)
        return NotImplemented


class Poisson(Distribution):
    discrete = True

    def __init__(self, mu):
        self.mu = mu
        self.dist = sci.poisson(mu)
        self.expectation = self.mu

    def __add__(self, other):
        match other:
            case Poisson():
                return Poisson(mu=self.mu + other.mu)
        return NotImplemented


class Exponential(Distribution):
    def __init__(self, intensity: float):
        self.intensity = intensity
        self.dist = sci.expon(scale=1 / intensity)
        self.expectation = 1 / self.intensity

    def __add__(self, other):
        match other:
            case Exponential() if self.intensity == other.intensity:
                return Gamma(theta=1 / self.intensity, r=2)
            case Gamma() if 1 / self.intensity == other.theta:
                return Gamma(theta=other.theta, r=other.r + 1)
        return NotImplemented

    def mgf(self, t):
        return self.intensity / (self.intensity - t)


class Gamma(Distribution):
    """Gamma with scale ``theta`` and shape ``r``."""

    def __init__(self, theta, r):
        self.theta = theta
        self.r = r
        self.dist = sci.gamma(a=r, scale=theta)
        self.expectation = self.r * self.theta

    def __add__(self, other):
        match other:
            case Gamma() if self.theta == other.theta:
                return Gamma(theta=self.theta, r=self.r + other.r)
            case Exponential() if self.theta == 1 / other.intensity:
                return Gamma(theta=self.theta, r=self.r + 1)
        return NotImplemented

    def mgf(self, t):
        return (1 - self.theta * t) ** -self.r


class ChiSquare(Distribution):
    def __init__(self, df: int):
        self.df = df
        self.dist = sci.chi2(df)
        self.expectation = self.df

    def __add__(self, other):
        match other:
            case ChiSquare():
                return ChiSquare(df=self.df + other.df)
        return NotImplemented


class Unknown(Distribution):
    def __init__(self, mean: float, variance: float, pdf: "function"):
        self.mean = mean
        self.variance = variance
        self.expectation = mean
        self._pdf = pdf

    def pdf(self, x):
        return self._pdf(x)

    def cdf(self, x):
        raise NotImplementedError("Unknown distributions only define a pdf.")
