Project Overview
================

Introduction
------------
`thevenin` is a Python package designed to offer a simple, robust, and flexible interface for running Thevenin equivalent circuit models. Its primary focus is on simulating battery performance under various load conditions, making it an invaluable tool for researchers and scientists working on battery technologies. Whether you need to generate synthetic data, optimize parameters for real-world systems, or integrate fast, accurate models into control algorithms, `thevenin` is built to handle it all.

The package provides a balance between simplicity and capability, supporting both constant and dynamic loads, and is scalable enough to fit into real-time systems.

Key Features
^^^^^^^^^^^^
* **Flexible Circuit Elements:** All circuit elements, including resistors and capacitors, can either be constant or depend on state of charge (SOC) and temperature.
* **Customizable RC Pairs:** The model supports any number of RC (resistor-capacitor) pairs, from zero to :math:`N`, allowing the model to scale from simple to more complex systems.
* **Thermal Modeling:** The package can operate in isothermal conditions or simulate thermal effects using a lumped thermal model for greater accuracy.
* **Versatile Experiment Interface:** The API allows for intuitive and flexible simulation of any type of load, including constant and dynamic loads driven by current, voltage, and/or power.
* **Cross-platform Support:** Written in Python, the package runs on any platform that supports Python and is continuously tested across multiple Python versions.

Use Cases
---------
`thevenin` is designed for a variety of applications in the battery research space:

* **Parameter Optimization:** The packaged models can integrate with optimization routines, enabling fast model calibration to real-world battery systems.
* **Synthetic Data Generation:** Researchers can generate synthetic data for analysis, algorithm development, or system testing.
* **Battery Model Integration:** `thevenin` is designed for integration with control systems, such as those using Kalman filter algorithms for real-time state estimation and battery management.

Target Audience
---------------
`thevenin` is built for scientists and researchers in the battery industry. Its primary applications focus on:

* Battery performance simulation
* State of health (SOH) estimation
* Real-time control integration

Users who require accurate, fast models that can be integrated into control algorithms and optimization frameworks will find `thevenin` especially valuable.

Technology Stack
----------------
* **Language:** Python
* **Compatibility:** Runs on any hardware that supports Python. Multiple versions are supported.

Project Origins
---------------
`thevenin` was developed by researchers at the **National Laboratory of the Rockies (NLR)** as part of the **Rapid Operational Validation Initiative (ROVI)**, a project funded by the **Office of Electricity**. The ROVI project aims to streamline the process of validating new battery technologies and chemistries as they enter the market. `thevenin` contributes to this effort by providing a tool that models battery performance with flexibility and speed. If interested, you can read more about ROVI `here <https://www.energy.gov/oe/rapid-operational-validation-initiative-rovi>`_.

Roadmap and Future Directions
-----------------------------
`thevenin` has several exciting long-term goals:

* **Optimization Submodule:** A future release will include an optimization submodule for automated parameter fitting to experimental data.
* **Integration with Kalman filters:** The package is currently being exercised with `moirae <https://github.com/ROVI-org/auto-soh>`_, a separate package containing Kalman filter algorithms. This will demonstrate how `thevenin` can be used for online state estimation, improving real-time battery management.

Contributions
-------------
The `thevenin` project is hosted and actively maintained on `GitHub <https://github.com/NREL/thevenin>`_. Developers interested in contributing are encouraged to review the Code structure and Workflow sections for detailed information on the branching strategy, code review process, and how to get involved. All contributions are welcome.
