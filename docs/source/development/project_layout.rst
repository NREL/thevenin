Project Layout
==============
The ``thevenin`` project is organized to provide clarity and structure, making it easy for developers to navigate and contribute. Below is an outline of the key directories and files, along with guidelines for working within them.

Root Directory
--------------
The root directory contains the most important files and folders necessary for development:

* **src/:** The core package code resides in this directory. This is the primary folder developers will interact with when modifying or adding features.
* **pyproject.toml:** This file contains the project's build system configurations and dependencies. If you need to add or modify dependencies, you should do so in this file.
* **noxfile.py:** Contains automation scripts for tasks like testing, linting, formatting, and building documentation. Developers should use nox sessions as needed to ensure code quality and consistency.
* **tests/:** This is where all unit tests and integration tests are stored. Any new functionality should include appropriate tests here.
* **docs/:** Contains documentation files for the project. Developers contributing to the documentation should work here, particularly if adding or improving developer guides or API references.

Source Directory
----------------
The ``src/`` directory contains the main package code. Using this structure ensures that local imports during development come from the installed package rather than accidental imports from the source files themselves.

Top-level Package
^^^^^^^^^^^^^^^^^
The core classes of the ``thevenin`` package reside at the top level of the src/ directory and include:

* ``IDASolver``: Handles solving the differential algebraic equations used in circuit models.
* ``Model``: Represents the equivalent circuit model itself, allowing for flexible setup of different configurations.
* ``Experiment``: Manages experiments, including dynamic or static load profiles.
* ``StepSolution`` and ``CycleSolution``: Provide a structured way to return and analyze the results of simulations.

Each of these classes typically resides in its own file, following a philosophy of keeping files manageable in size. If multiple classes or functions share significant overlap in purpose, they may be grouped in the same file, but care is taken to keep files concise and easy to navigate.

Subpackages
^^^^^^^^^^^
There are two subpackages that handle specific functionality:

* ``plotutils/``: Contains utilities for visualizing simulation results. Any helper functions for plotting or figure generation live here to keep the core logic separate from visualization tasks.
* ``loadfns/``: Contains functions to assist users in building dynamic load profiles. These functions are especially useful for users looking to simulate different load scenarios in their models.
