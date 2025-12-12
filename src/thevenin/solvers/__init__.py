"""
The `solvers` module provides interfaces for solving the systems of ordinary
differential equations that govern equivalent circuit models. The solvers are
taken from `scikit-sundae`_, a wrapper for `SUNDIALS`_. Specifically, both the
IDA (for differential-algebraic equations) and CVODE (for ordinary differential
equations) interfaces are included.

These solvers offer robust numerical methods with settings to adjust the
accuracy, stability, and performance. While the implementations from from the
`scikit-sundae` package, they are included here to centralize documentation
and streamline solver configuration within the ECM framework.

.. _scikit-sundae: https://scikit-sundae.readthedocs.io
.. _SUNDIALS: https://sundials.readthedocs.io

"""

from ._cvode import CVODEResult, CVODESolver
from ._ida import IDAResult, IDASolver

__all__ = [
    'CVODEResult',
    'CVODESolver',
    'IDAResult',
    'IDASolver',
]
