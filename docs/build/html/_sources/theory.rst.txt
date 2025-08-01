Theoretical reference
=====================

This page provides a brief overview of the theoretical background of the Amiet model for trailing-edge noise. While it is not strictly necessary to know the theory to use tha package, having a clear understading of the underlying physics and assumptions can help in evaluating the results and choosing the appropriate parameters for the model, as well as understading some parts of the documentation. For an in depth description of the model, we advise to refer to the original paper by Amiet (1975) and the subsequent extension by Roger & Moreau (2005).

On a fundamental level, noise is generated at the trailing edge of an airfoil because the pressure fluctuations induced by the turbulent boundary layer get  scattered by the trailing edge. In the original paper, the airfoil is considered as a semi-infinite flat plate, and a correction to take into account the presence of the leading-edge was later introduced by Roger & Moreau (2005). While it is understood that the ultime sound source is the turbulent boundary layer, the Amiet model uses the pressure fluctuations at the trailing edge as a proxy for the sound source. The presence of the trailing edge is then modeled as a linear filter that modifies the pressure fluctuations to produce the sound radiation. 

In the simplified form used for the present package, the Amiet model's prediction of the sound power spectral density at a point in space :math:`\mathbf{x}` and frequency :math:`\omega` is given by:

.. math::
    :label: amiet-model

    S_{pp}^{te}(\mathbf{x},\omega) = \left(\frac{\omega x_3 c}{2\pi c_0 S_0^2}\right)^2 \frac2L\Phi_{pp}(\omega)\ell_y\left(\frac{kx_2}{S_0},\omega\right)\left\vert\mathcal L\left(\frac{\omega}{U_c},\frac{kx_2}{S_0}\right)\right\vert^2

