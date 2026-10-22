import subprocess
import sys

import numpy as np
import pandas as pd
import pytest

import dexter
from dexter.visualization import Space, Matrix3D


def test_top_level_exports():
    for name in dexter.__all__:
        assert getattr(dexter, name) is not None


def test_import_does_not_load_ml_or_gui():
    code = "import sys, dexter; print([m for m in ('sklearn', 'tkinter', 'PyQt5', 'dash') if m in sys.modules])"
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True)
    assert out.stdout.strip() == "[]"


def test_space_traces():
    space = Space()
    space.add_vector([1, 2, 3])
    space.add_surface(z_data=np.ones((2, 3)))
    assert len(space.fig.data) == 2
    assert space.fig.data[1].x.shape == (2, 3)


def test_matrix_decompositions():
    m = Matrix3D([[1, 2], [3, 4]])
    T, Q = m.schur_decomposition()
    np.testing.assert_allclose(Q @ T @ Q.T, m.matrix, atol=1e-10)
    w, _ = m.eigen_decomposition()
    assert w.shape == (2,)


def test_pick_classifier_non_interactive():
    pytest.importorskip("sklearn")
    pytest.importorskip("hyperopt")
    rng = np.random.default_rng(0)
    X = rng.normal(size=(80, 2))
    df = pd.DataFrame({"a": X[:, 0], "b": X[:, 1], "target": (X[:, 0] + X[:, 1] > 0).astype(int)})

    model = dexter.pick_classifier(df, "target", choice="k_neighbors", random_state=0, fold_count=3, max_evals=3)

    assert hasattr(model, "predict")
