"""
Visualization Module

Provides 3D visualization, plotting, and interactive graphics tools.
"""

from .space import Space
from .linalg import Matrix3D, visualize_eigenvectors, visualize_schur_decomposition

__all__ = ['Space', 'Matrix3D', 'visualize_eigenvectors', 'visualize_schur_decomposition']
