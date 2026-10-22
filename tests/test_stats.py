import numpy as np
import pytest

from dexter.stats import (
    RV, Sample, Normal, Uniform, Binomial, Geometric, NegativeBinomial,
    Poisson, Exponential, Gamma, ChiSquare, P, E, recognize,
)


def test_expected_value():
    assert RV(Binomial(10, 0.4)).expected_value == 4
    assert RV(Binomial(25, 0.6)).expected_value == 25 * 0.6


def test_add_binomial():
    rv_sum = RV(Binomial(25, 0.6)) + RV(Binomial(10, 0.6))

    assert isinstance(rv_sum, RV)
    assert isinstance(rv_sum.distribution, Binomial)
    assert rv_sum.expected_value == 35 * 0.6


def test_add_poisson():
    rv_sum = RV(Poisson(5)) + RV(Poisson(8))

    assert isinstance(rv_sum.distribution, Poisson)
    assert rv_sum.expected_value == 13


def test_add_exponential_same_rate_is_gamma():
    rv_sum = RV(Exponential(3)) + RV(Exponential(3))

    assert isinstance(rv_sum.distribution, Gamma)
    assert rv_sum.expected_value == pytest.approx(2 / 3)


def test_add_exponential_different_rates_has_no_closed_form():
    with pytest.raises(TypeError):
        RV(Exponential(3)) + RV(Exponential(4))


def test_add_normal_and_scale():
    total = Normal(1, 2) + Normal(3, 4)
    assert (total.mean, total.var) == (4, 6)

    scaled = 2 * Normal(1, 2)
    assert (scaled.mean, scaled.var) == (2, 8)


def test_geometric_sums_to_negative_binomial():
    total = Geometric(0.5) + Geometric(0.5)

    assert isinstance(total, NegativeBinomial)
    assert total.expectation == 4
    assert total.dist.mean() == pytest.approx(4)


def test_gamma_and_chisquare():
    assert Gamma(theta=2, r=3).dist.mean() == pytest.approx(6)
    assert (ChiSquare(2) + ChiSquare(3)).df == 5
    assert ChiSquare(4).pdf(1.0) > 0


def test_pdf_and_mgf():
    assert Normal(0, 1).pdf(0) == pytest.approx(1 / np.sqrt(2 * np.pi))
    assert Binomial(1, 0.3).pdf(1) == pytest.approx(0.3)
    assert Normal(0, 1).mgf(1) == pytest.approx(np.exp(0.5))
    assert Uniform(0, 1).mgf(0) == 1.0


def test_draw():
    rv = Normal(mean=0, var=1).draw()
    assert isinstance(rv, RV)
    assert str(rv).startswith("X")

    sample = Uniform(a=0, b=1).draw(n=5)
    assert isinstance(sample, Sample)
    assert len(sample) == 5
    assert str(sample).startswith("Sample(")
    assert 0 <= E(sample) <= 1


def test_funcs():
    rv = RV(Normal(0, 1))
    assert P(rv, 0) == pytest.approx(Normal(0, 1).pdf(0))

    rng = np.random.default_rng(0)
    name, _, p_value = recognize(rng.normal(size=500))
    assert name == "norm"
    assert 0 <= p_value <= 1
