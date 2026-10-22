"""
Simulation Module

Provides a discrete event simulation framework using SimPy, and a simple
grid environment for agent experiments.
"""

from .sim_manager import SimManager
from .grid import Grid, GridApp

__all__ = ['SimManager', 'Grid', 'GridApp']
