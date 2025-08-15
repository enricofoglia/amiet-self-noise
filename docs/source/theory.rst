Theoretical reference
=====================

This page provides a brief overview of the theoretical background of the Amiet model for trailing-edge noise. While it is not strictly necessary to know the theory to use tha package, having a clear understading of the underlying physics and assumptions can help in evaluating the results and choosing the appropriate parameters for the model, as well as understading some parts of the documentation. For an in depth description of the model, we advise to refer to the original paper by Amiet (1975) [1]_ and the subsequent extension by Roger & Moreau (2005) [2]_.

On a fundamental level, noise is generated at the trailing edge of an airfoil because the pressure fluctuations induced by the turbulent boundary layer get  scattered by the trailing edge. In the original paper, the airfoil is considered as a semi-infinite flat plate, and a correction to take into account the presence of the leading-edge was later introduced by Roger & Moreau (2005). While it is understood that the ultime sound source is the turbulent boundary layer, the Amiet model uses the pressure fluctuations at the trailing edge as a proxy for the sound source. The presence of the trailing edge is then modeled as a linear filter that modifies the pressure fluctuations to produce the sound radiation. 

In the simplified form used for the present package, the Amiet model's prediction of the sound power spectral density at a point in space :math:`\mathbf{x}` and frequency :math:`\omega` is given by:

.. math::
    :label: amiet-model

    S_{pp}^{te}(\mathbf{x},\omega) = \left(\frac{\omega x_3 c}{2\pi c_0 S_0^2}\right)^2 L\Phi_{pp}(\omega)\ell_y\left(\omega\right)\left\vert\mathcal L\left(\frac{\omega}{U_c}\right)\right\vert^2

where:

- :math:`c = 2b` is the airfoil chord (m)
- :math:`c_0` is the speed of sound (m/s)
- :math:`S_0` is the corrected observer's distance (m)
- :math:`L` is the span of the airfoil (m)
- :math:`\Phi_{pp}` is the wall pressure fluctuations autospectrum (:math:`\mathrm{Pa}^2/\mathrm{Hz}`)
- :math:`\ell_y` is the span-wise coherence length (m)
- :math:`U_c` is the turbulent eddies' convection speed (m/s)
- :math:`\mathcal{L}` is the radiation integral.

References

.. [1] Amiet, R. K. (1975). Acoustic radiation from an airfoil in a 
           turbulent stream. Journal of Sound and Vibration, 41(4), 407-420.

.. [2] Roger, M., & Moreau, S. (2005). Back-scattering correction and 
           further extensions of Amiet's trailing-edge noise model. 
           Part 1: theory. Journal of Sound and Vibration, 286(3), 477-506.
    