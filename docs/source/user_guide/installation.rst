Installation
============
This page will guide you through the installation process for `thevenin`. Whether you are looking to install the package via `pip` from PyPI, `conda` from the conda-forge channel, or from the source distribution, this page has you covered.

Installing via PyPI
-------------------
Installing with `pip` will pull a distribution file from the Python Package Index (PyPI). We provide both binary and source distributions on `PyPI <https://pypi.org/project/thevenin>`_.

To install the latest release, simply run the following::

    pip install thevenin

Installing via conda-forge
--------------------------
To install via `conda`, you must specify the conda-forge channel. You can install the package with the following::

    conda install -c conda-forge thevenin

Be aware that our conda-forge releases are less likely to get patches than PyPI releases when it comes to older software versions. For example, if the software has moved on to v1.1, then a patch for v1.0 will likely not make its way to conda.

Python Version Support
----------------------
Please note that `thevenin` releases only support whichever Python versions are actively maintained at the time of the release. If you are using a version of Python that has reached the end of its life, as listed on the `official Python release page`_, you may need to install an older version of `thevenin` or upgrade your Python version. We recommend, however, upgrading your Python version instead of using an older version of `thevenin`.

.. _official Python release page: https://devguide.python.org/versions/

Developer Versions
------------------
The development version is ONLY hosted on GitHub. To install it, see the :doc:`/development/index` section. You should only do this if you:

* Want to try experimental features
* Need access to unreleased fixes
* Would like to contribute to the package
