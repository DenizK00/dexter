"""
Pytest configuration and common fixtures for Dexter Toolkit tests
"""

import pytest
import numpy as np
import pandas as pd


@pytest.fixture
def sample_dataframe():
    """Sample DataFrame for testing"""
    return pd.DataFrame({
        'feature1': [1, 2, 3, 4, 5],
        'feature2': [2, 4, 6, 8, 10],
        'target': [0, 1, 0, 1, 1]
    })


@pytest.fixture
def sample_distributions():
    """Sample distributions for testing"""
    from dexter.stats.distribution import Normal, Uniform, Binomial
    
    return {
        'normal': Normal(mean=0, var=1),
        'uniform': Uniform(a=0, b=1),
        'binomial': Binomial(n=10, p=0.5)
    }


@pytest.fixture
def sample_grid():
    """Sample grid for testing"""
    from dexter.environment.grid import Grid
    
    grid = Grid(nrows=5, ncolumns=5)
    grid.set_agent(2, 2)
    grid.set_cell(1, 1, '#')
    grid.set_cell(3, 3, '#')
    
    return grid
