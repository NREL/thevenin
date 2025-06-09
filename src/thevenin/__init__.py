"""
Summary
=======
The Thevenin equivalent circuit model is a common low-fidelity battery model
consisting of a single resistor in series with any number of RC pairs, i.e.,
parallel resistor-capacitor pairs. This Python package contains an API for
building and running experiments using Thevenin models. When referring to the
model itself, we use capitalized "Thevenin", and for the package lowercase
``thevenin``.

Accessing the Documentation
---------------------------
Documentation is accessible via Python's ``help()`` function which prints
docstrings from a package, module, function, class, etc. You can also access
the documentation by visiting the website, hosted on Read the Docs. The website
includes search functionality and more detailed examples.

"""

# core package
from ._ida_solver import IDASolver, IDAResult
from ._experiment import Experiment
from ._model import Model
from ._solutions import StepSolution, CycleSolution

# submodules
from . import loadfns
from . import plotutils

__version__ = '0.1.3'

__all__ = [
    'IDASolver',
    'IDAResult',
    'Experiment',
    'Model',
    'StepSolution',
    'CycleSolution',
    'loadfns',
    'plotutils',
]
