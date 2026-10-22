"""
Visualization Module

Provides 3D visualization, plotting, and interactive graphics tools.
"""

from typing import TYPE_CHECKING

from .._lazy import lazy_exports

_EXPORTS = {
    'Space': ('space', "3D Plotly space; add_vector(), add_surface(), show()"),
    'Matrix3D': ('linalg', "Matrix with schur/eigen decompositions and visualize_matrix()"),
    'visualize_eigenvectors': ('linalg', "Plot a matrix's eigenvectors in a Space"),
    'visualize_schur_decomposition': ('linalg', "Plot a matrix's Schur vectors in a Space"),
}

__all__ = list(_EXPORTS)
__getattr__, __dir__, help = lazy_exports(__name__, _EXPORTS)

if TYPE_CHECKING:
    from .space import Space
    from .linalg import Matrix3D, visualize_eigenvectors, visualize_schur_decomposition
