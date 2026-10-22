"""
Script Name: linalg.py
Author: Deniz
Created: 2024-08-26 18:01:57
Description: Matrix decompositions and their 3D visualizations
"""

import numpy as np
import plotly.graph_objs as go
from scipy.linalg import schur, eig

from .space import Space


class Matrix3D:
    def __init__(self, matrix):
        """
        Initializes a Matrix3D object.

        Parameters:
        matrix (array-like): The matrix to be encapsulated by this class.
        """
        self.matrix = np.array(matrix)

    def schur_decomposition(self):
        """
        Computes the Schur decomposition of the matrix.

        Returns:
        T (ndarray): The upper triangular matrix.
        Q (ndarray): The orthogonal matrix.
        """
        return schur(self.matrix)

    def eigen_decomposition(self):
        """
        Computes the eigenvalue decomposition of the matrix.

        Returns:
        w (ndarray): The eigenvalues of the matrix.
        v (ndarray): The eigenvectors of the matrix.
        """
        return eig(self.matrix)

    def visualize_matrix(self, space=None):
        """
        Visualizes the matrix as a 3D surface plot in the given space.

        Parameters:
        space (Space): Optional. The Space object where the matrix will be visualized.
        """
        space = space if space is not None else Space()
        space.add_surface(z_data=self.matrix)
        space.show()


def visualize_eigenvectors(matrix, space=None):
    """
    Visualizes the eigenvectors of a matrix in a 3D space.

    Parameters:
    matrix (array-like): The matrix whose eigenvectors will be visualized.
    space (Space): Optional. The Space object where the eigenvectors will be visualized.
                   If not provided, a new Space will be created.
    """
    _, eigenvectors = Matrix3D(matrix).eigen_decomposition()
    space = space if space is not None else Space()

    for vec in eigenvectors.T:
        space.add_vector(np.real(vec), color='blue')

    space.show()


def visualize_schur_decomposition(matrix, space=None):
    """
    Visualizes the Schur decomposition of a matrix in a 3D space.

    Parameters:
    matrix (array-like): The matrix to be decomposed and visualized.
    space (Space): Optional. The Space object where the matrix will be visualized.
                   If not provided, a new Space will be created.
    """
    T, Q = Matrix3D(matrix).schur_decomposition()
    space = space if space is not None else Space()

    # Visualize orthogonal matrix Q as vectors
    for vec in Q.T:
        space.add_vector(np.real(vec), color='green')

    # Visualize the upper triangular matrix T as a surface
    space.add_surface(z_data=T)

    space.show()


# Example usage
if __name__ == "__main__":
    matrix = np.array([[1, 2], [3, 4]])

    T, Q = Matrix3D(matrix).schur_decomposition()
    print("Schur Decomposition:")
    print("T =", T)
    print("Q =", Q)

    visualize_eigenvectors(matrix)
    visualize_schur_decomposition(matrix)
