"""
Simulation Module

Provides a discrete event simulation framework using SimPy, and a simple
grid environment for agent experiments.
"""

from typing import TYPE_CHECKING

from .._lazy import lazy_exports

_EXPORTS = {
    'SimManager': ('sim_manager', "Register SimPy resources and processes, then run() or step()"),
    'Grid': ('grid', "Text grid with walls and one agent; set_cell(), set_agent()"),
    'GridApp': ('grid', "Tkinter window that shows and updates a Grid"),
}

__all__ = list(_EXPORTS)
__getattr__, __dir__, help = lazy_exports(__name__, _EXPORTS)

if TYPE_CHECKING:
    from .sim_manager import SimManager
    from .grid import Grid, GridApp
