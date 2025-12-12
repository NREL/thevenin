.. .. raw:: html

..    <embed>
..       </br>
..       <img alt='logo' class='onlight bg-transparent' src='_static/light.png'
..        style='width: 75%; min-width: 250px; max-width: 500px;'>
..       <img alt='logo' class='ondark bg-transparent' src='_static/dark.png'
..        style='width: 75%; min-width: 250px; max-width: 500px;'>
..       </br>
..       </br>
..    </embed>

=======
Summary
=======
The Thevenin equivalent circuit model is a common low-fidelity battery model consisting of a single resistor in series with any number of RC pairs, i.e., parallel resistor-capacitor pairs. This Python package contains an API for building and running experiments using Thevenin models. When referring to the model itself, we use capitalized "Thevenin", and for the package lowercase `thevenin`.

.. toctree:: 
   :caption: User Guide
   :hidden:
   :maxdepth: 2

   User Guide <user_guide/index>

.. toctree:: 
   :caption: API Reference
   :hidden:
   :maxdepth: 2

   API Reference <api/thevenin/index>

.. toctree:: 
   :caption: Examples
   :hidden:
   :maxdepth: 2

   Examples <examples/index>

.. toctree:: 
   :caption: Development
   :hidden:
   :maxdepth: 2

   Development <development/index>

**Version:** |version|

**Useful links:** 
`anaconda <https://www.anaconda.com/download>`_ |
`spyder <https://www.spyder-ide.org/>`_ |
`numpy <https://numpy.org/doc/stable/>`_  |  
`scikit-sundae <https://scikit-sundae.readthedocs.io/>`_ |
`matplotlib <https://matplotlib.org/stable/users/>`_

.. grid:: 1 2 2 2

   .. grid-item-card:: User Guide
         :class-footer: border-0
         :padding: 2

         Access installation instructions and in-depth
         information on solver concepts and settings.

         .. image:: _static/user_guide.svg
            :class: bg-transparent
            :align: center
            :height: 75px

         +++
         .. button-ref:: user_guide/index
            :expand:
            :color: primary
            :click-parent:

            To the user guide

   .. grid-item-card:: API Reference
      :class-footer: border-0
      :padding: 2

      Get detailed documentation on all of the modules,
      functions, classes, etc.

      .. image:: _static/api_reference.svg
         :class: bg-transparent
         :align: center
         :height: 75px

      +++
      .. button-ref:: api/thevenin/index
         :expand:
         :color: primary
         :click-parent:

         Go to the docs

   .. grid-item-card:: Examples
         :class-footer: border-0
         :padding: 2
           
         A great place to learn how to use the package and
         expand your skills.

         .. image:: _static/examples.svg
            :class: bg-transparent
            :align: center
            :height: 75px

         +++
         .. button-ref:: examples/index
            :expand:
            :color: primary
            :click-parent:

            See some examples

   .. grid-item-card:: Development
      :class-footer: border-0
      :padding: 2
         
      Trying to fix a typo in the documentation? Looking
      to improve or add a new feature?

      .. image:: _static/development.svg
         :class: bg-transparent
         :align: center
         :height: 75px

      +++
      .. button-ref:: development/index
         :expand:
         :color: primary
         :click-parent:

         Read contributor guidelines
