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


def test_import_is_lazy():
    heavy = ('sklearn', 'tkinter', 'PyQt5', 'dash', 'pyomo', 'scipy', 'sympy', 'pandas', 'plotly', 'simpy')
    code = f"import sys, dexter; print([m for m in {heavy!r} if m in sys.modules])"
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


@pytest.mark.parametrize("package", ["dexter", "dexter.ml", "dexter.optimization", "dexter.simulation",
                                     "dexter.stats", "dexter.visualization"])
def test_help_lists_exports_without_heavy_imports(package):
    heavy = ('sklearn', 'pyomo', 'scipy', 'sympy', 'pandas', 'plotly', 'simpy')
    code = (f"import sys, importlib; m = importlib.import_module({package!r}); m.help(); "
            f"print([h for h in {heavy!r} if h in sys.modules]); print(m.__all__)")
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True).stdout
    *help_text, loaded, names = out.strip().splitlines()
    assert loaded == "[]"
    for name in eval(names):
        assert f"  {name} " in "\n".join(help_text)


def test_star_import_does_not_shadow_builtin_help():
    assert "help" not in dexter.__all__
