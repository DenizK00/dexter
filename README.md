# Dexter Toolkit
**Data Experimentation and Tinkering Kit**

A small Python toolkit for optimization, simulation, statistics, visualization and model selection experiments.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Installation

```bash
git clone https://github.com/DenizK00/Dexter.git
cd Dexter

pip install .            # core: optimization, simulation, stats, visualization
pip install ".[ml]"      # adds dexter.ml (scikit-learn, hyperopt, matplotlib, seaborn)
make install-dev         # editable install with the ml and dev extras
```

`Problem.solve()` needs an LP solver that Pyomo can find, GLPK by default (`brew install glpk`, `apt install glpk-utils` or `conda install glpk`).

## Quick start

```python
from dexter import Problem, SimManager, Normal, Space, pick_classifier

# Optimization
problem = Problem("min 2*x + 3*y", ["x + y >= 10"])
solution = problem.solve()

# Statistics
rv = Normal(mean=0, var=1).draw()

# Simulation
sim = SimManager()
sim.run(until=100)
```

## Package structure

```
src/dexter/
├── ml/              # pick_classifier: model comparison + hyperopt tuning ([ml] extra)
├── optimization/    # Equation, Problem, Solution (Pyomo + SymPy)
├── simulation/      # SimManager (SimPy), Grid environment
├── stats/           # distributions, RV, Sample, P, E, recognize
└── visualization/   # Space, Matrix3D and decomposition plots (Plotly)
```

## Modules

### ML: model selection

Compares classifiers on a train/test split, then tunes the one you pick with hyperopt. Pass `choice` to skip the interactive prompt.

```python
from dexter.ml import pick_classifier

model = pick_classifier(df, target="label", mode="extensive", choice="random_forest", random_state=0)
```

### Optimization

Linear programs written as strings. Variables are non-negative.

```python
from dexter.optimization import Problem

problem = Problem("max 3*x + 2*y", ["x + y <= 4", "x + 3*y <= 6"])
solution = problem.solve()
problem(solution)          # objective value
problem.constraint_matrix  # numpy array, one row per constraint
```

### Simulation

```python
import simpy
from dexter.simulation import SimManager, Grid

sim = SimManager()
sim.add_resource("service", simpy.Resource(sim.env, capacity=2))
sim.run(until=100)

grid = Grid(nrows=10, ncolumns=10)
grid.set_cell(3, 3, "#")
grid.set_agent(5, 5)
print(grid)
```

`GridApp` shows a grid in a Tkinter window and needs a Python build with Tk.

### Statistics

Distributions wrap `scipy.stats`. Adding two independent distributions returns the distribution of the sum when it has a closed form (Normal, Binomial, Poisson, Geometric, Negative Binomial, Exponential, Gamma, Chi-square) and raises `TypeError` otherwise.

```python
from dexter.stats import Normal, Uniform, Binomial, RV, E

total = RV(Binomial(25, 0.6)) + RV(Binomial(10, 0.6))
E(total)                      # 21.0
sample = Uniform(0, 1).draw(n=100)
```

### Visualization

```python
from dexter.visualization import Space, visualize_eigenvectors

space = Space(x_size=10, y_size=10, z_size=10)
space.add_vector([1, 2, 3], color="red")
space.show()

visualize_eigenvectors([[2, 0, 0], [0, 3, 4], [0, 4, 9]])
```

## Development

```bash
make install-dev   # editable install with [ml,dev]
make test          # pytest with coverage
make lint          # flake8
make format        # black
make build         # sdist + wheel
```

## License

MIT, see [LICENSE](LICENSE).

## Author

**Deniz** - [denizkurtaran00@gmail.com](mailto:denizkurtaran00@gmail.com)
