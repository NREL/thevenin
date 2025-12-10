What is ``thevenin``?
=====================
``thevenin`` is a Python package designed for running equivalent circuit models, a widely used approach for modeling the electrical behavior of complex systems, such as batteries and other electrochemical devices. The package allows users to simulate circuits that consist of a voltage source, a series resistor, and some number of resistor-capacitor (RC) pairs, which represent different dynamic behaviors of the system. With ``thevenin``, users can specify the number of RC pairs to tailor the model to their needs. An example circuit is shown in the figure below with two RC elements, but the model can be set to have as few as zero and as many as :math:`N`. The package also offers the flexibility to run the model either isothermally (with constant temperature) or with temperature dependence, making it suitable for a wide range of applications.

.. figure:: figures/2RC_circuit.png
   :align: center
   :alt: Two-RC-pair Thevenin circuit.
   :width: 75%

The model allows each of the circuit elements to have functional parameters, i.e., values that depend on the state of the system. Resistance and capacitance values can be expressed in terms of both state of charge and temperature. To calibrate the model to a specific system, it is common to fit each of these values to cell data at different temperatures and states of charge (SOC) and then to use those fits to find algebraic expressions that describe their dependence on SOC and temperature. Alternatively, a parameterized table can also be used for interpolation to provide circuit element parameters after fitting. While this package does not natively include a fitting strategy, the model is fast and can easily be set up with optimization routines. We recommend the `scipy.optimize <https://docs.scipy.org/doc/scipy/reference/optimize.html>`_ package for those looking to take this approach.

Use Cases
=========
The thevenin package is particularly useful for battery modeling and simulation, where predicting voltage response to varying loads is crucial. Engineers and researchers can use it to simulate state-of-charge-dependent behavior or investigate the effects of temperature fluctuations on system performance. The package is ideal for designing and testing control algorithms, predicting system performance under dynamic loads, or conducting model-based diagnostics and state estimation in energy storage applications.

Acknowledgements
================
This work was authored by the National Laboratory of the Rockies (NLR), operated by Alliance for Energy Innovation, LLC, for the U.S. Department of Energy (DOE). The views expressed in the package and its documentation do not necessarily represent the views of the DOE or the U.S. Government.

The motivation and funding for this project came from the Rapid Operational Validation Initiative (ROVI) sponsored by the Office of Electricity. The focus of ROVI is "to greatly reduce time required for emerging energy storage technologies to go from lab to market by developing new tools that will accelerate the testing and validation process needed to ensure commercial success." If interested, you can read more about ROVI `here <https://www.energy.gov/oe/rapid-operational-validation-initiative-rovi>`_.
