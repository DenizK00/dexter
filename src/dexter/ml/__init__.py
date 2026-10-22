"""
Machine Learning Module

Provides automated model selection, hyperparameter optimization, and ML utilities.
"""

from typing import TYPE_CHECKING

from .._lazy import lazy_exports

_EXPORTS = {
    'pick_classifier': ('pick', "Compare classifiers with cross-validation and tune one with hyperopt"),
}

__all__ = list(_EXPORTS)
__getattr__, __dir__, help = lazy_exports(__name__, _EXPORTS)

if TYPE_CHECKING:
    from .pick import pick_classifier
