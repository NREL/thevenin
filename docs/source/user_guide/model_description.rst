Model Description
=================
This page outlines the underlying mathematics of the Thevenin equivalent circuit model. The index :math:`j` is used throughout the documentation to gernalize the fact that the model can be run with a variable number of resistor-capacitor (RC) elements. When zero RC pairs are specified, the model collapses into the simpler Rint model, discussed :doc:`here <equivalent_circuit_models>`. However, the model also allows any nonzero number of RC pairs, within reason. The figure below illustrates an example Thevenin circuit with two RC pairs.

.. figure:: figures/2RC_circuit.png
   :align: center
   :alt: Two-RC-pair Thevenin circuit.
   :width: 75%

The Thevenin circuit is governed by the evolution of the state of charge (soc, -), RC overpotentials (:math:`V_j`, V), cell voltage (:math:`V_{\rm cell}`, V), and temperature (:math:`T_{\rm cell}`, K). soc and :math:`V_j` evolve in time as

.. math::

    \begin{align}
      &\frac{d\rm soc}{dt} = \frac{-I}{3600 Q_{\rm max}}, \\
      &\frac{dV_j}{dt} = -\frac{V_j}{R_jC_j} + \frac{I}{C_j},
    \end{align}

where :math:`I` is the load current (A), :math:`Q_{\rm max}` is the maximum nominal cell capacity (Ah), and :math:`R_j` and :math:`C_j` are the resistance (Ohm) and capacitance (F) of each RC pair :math:`j`. Note that the sign convention for :math:`I` is chosen such that positive :math:`I` discharges the battery (reduces soc) and negative :math:`I` charges the battery (increases soc). This convention is consistent with common physics-based models, e.g., the single particle model or pseudo-2D model. While not explicitly included in the equations above, :math:`R_j` and :math:`C_j` are functions of soc and :math:`T_{\rm cell}`. The temperature increases while the cell is active according to

.. math:: 
    
    \begin{equation}
      mC_p\frac{dT_{\rm cell}}{dt} = \dot{Q}_{\rm gen} + \dot{Q}_{\rm conv},
    \end{equation}

where :math:`m` is mass (kg), :math:`C_p` is specific heat capacity (J/kg/K), :math:`\dot{Q}_{\rm gen}` is the heat generation (W), and :math:`\dot{Q}_{\rm conv}` is the convective heat loss (W). Heat generation and convection are defined by

.. math:: 

    \begin{align}
      &\dot{Q}_{\rm gen} = I \times (V_{\rm ocv}({\rm soc}) - V_{\rm cell}), \\
      &\dot{Q}_{\rm conv} = hA(T_{\infty} - T_{\rm cell}),
    \end{align}

where :math:`h` is the convecitive heat transfer coefficient (W/m\ :sup:`2`/K), :math:`A` is heat loss area (m\ :sup:`2`), and :math:`T_{\infty}` is the air/room temperature (K). :math:`V_{\rm ocv}` is the open circuit voltage (V) and is a function of soc.

The overall cell voltage is

.. math:: 

    \begin{equation}
      V_{\rm cell} = V_{\rm ocv}({\rm soc}) - \sum_j V_j - IR_0,
    \end{equation}

where :math:`R_0` the lone series resistance (Ohm), as shown in Figure 1. Just like the other resistive elements, :math:`R_0` is a function of soc and :math:`T_{\rm cell}`.