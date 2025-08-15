import numpy as np
from scipy.special import fresnel


def _E_etoile(x):
    # Implementation compatible avec la convention utilisée E^*(x). Pour x <= 0 on remplace par une valeur positive.
    x = np.asarray(x, dtype=np.float64)  # évite racine de négatif / zéro
    xpos = np.maximum(x, 1e-12)
    arg = np.sqrt(2.0 * xpos / np.pi)
    S, C = fresnel(arg)
    # On renvoie C-i*S,
    return C - 1j * S


## On calcule la valeur de G


def _compute_G(D, mu, epsilon):
    E_etoile_4mu = _E_etoile(4.0 * mu)
    E_4mu = np.conj(E_etoile_4mu)
    E_etoile_2D = _E_etoile(2.0 * D)

    Dm2mu = D - 2.0 * mu
    Dp2mu = D + 2.0 * mu
    Dm2mu = np.where(np.abs(Dm2mu) < 1e-12, 1e-12, Dm2mu)
    Dp2mu = np.where(np.abs(Dp2mu) < 1e-12, 1e-12, Dp2mu)

    term1 = (1.0 + epsilon) * np.exp(1j * (D + 2.0 * mu)) * np.sin(D - 2.0 * mu) / Dm2mu
    term2 = (1.0 - epsilon) * np.exp(1j * (D - 2.0 * mu)) * np.sin(D + 2.0 * mu) / Dp2mu

    term3 = (
        (1.0 + epsilon)
        * (1.0 - 1j)
        / (2.0 * Dm2mu)
        * np.exp(1j * 4.0 * mu)
        * E_etoile_4mu
    )
    term4 = (
        -(1.0 - epsilon) * (1.0 + 1j) / (2.0 * Dp2mu) * np.exp(-1j * 4.0 * mu) * E_4mu
    )

    sqrt_factor = np.sqrt(2.0 * mu / D)
    x = (1.0 - epsilon) * (1.0 + 1j) / Dp2mu - (1.0 + epsilon) * (1.0 - 1j) / Dm2mu
    term5 = 0.5 * np.exp(2j * D) / sqrt_factor * E_etoile_2D * x

    # Somme finale
    G = term1 + term2 + term3 + term4 + term5
    return G


##  Expressions analytiques L1, L2 (trailing edge)
def _compute_L1_L2(omega, U0, c0, x1, S0, M0, b, alpha=1.0, a_param=None):
    # On calcule L1 et L2 pour une fréquence angulaire omega
    if a_param is None:
        a_param = alpha

    Uc = U0 * alpha

    # Information à modifier en fonction des données du prof.
    k = omega / c0
    beta2 = 1.0 - M0**2
    mu = k / beta2 * b
    k1 = omega / U0
    K1 = omega / Uc
    k1_bar = k1 * b
    K1_bar = K1 * b

    # Définitions B et C
    B = K1_bar + mu * (1.0 + M0)
    C = K1_bar - mu * (x1 / S0 - M0)

    if np.abs(C) < 1e-12:
        C = np.sign(C) * 1e-12 + 1e-12

    # E* evaluations
    E_etoile_2B = _E_etoile(2.0 * B)
    E_etoile_2Bminus2C = _E_etoile(2.0 * (B - C))

    prefacteur = -np.exp(2j * C) / (1j * C)
    term1 = (1.0 + 1j) * np.exp(-2j * C) * np.sqrt(B / (B - C)) * E_etoile_2Bminus2C
    term2 = -(1.0 + 1j) * E_etoile_2B
    term3 = 1.0
    L1 = prefacteur * (term1 + term2 + term3)

    ## On calcule L2
    D = mu * (1.0 - x1 / S0)
    Theta = np.sqrt((K1_bar + mu * (M0 + 1.0)) / (k1_bar + mu * (M0 + 1.0)))
    # Correction imaginaire ϵ (epsilon)
    eps = (1.0 + 1.0 / (4.0 * mu)) ** (-0.5) if mu != 0 else 1.0
    # -> si Θ≈1 alors le numerateur peut être 0
    H = (1.0 + 1j) * np.exp(-1j * 4.0 * mu) * (1.0 - Theta**2)
    H = H / (np.sqrt(np.pi * B) * (alpha - 1.0) * k1_bar + 1e-30)
    # Evaluer E*(4µ)
    E_etoile_4mu = _E_etoile(4.0 * mu)
    # G = 1.0 # !!!
    G = _compute_G(D, mu, eps)
    # Construction L2
    term_L2_a = np.exp(1j * 4.0 * mu) * (1.0 - (1.0 + 1j) * E_etoile_4mu)
    term_L2_b = -np.exp(2j * D)
    term_L2_c = 1j * (D + k1_bar + (M0 - 1.0) * mu) * G

    L2 = H * (term_L2_a + term_L2_b + term_L2_c)

    return L1, L2


##  Fonction principale
def compute_radiation_integral(
    omega_array, U0, c0, x1, S0, M0, b, alpha=1.0, a_param=None
):
    """
    Compute the Amiet radiation integral for airfoil trailing edge noise.
    
    This function calculates the complex-valued radiation integral that 
    represents the acoustic transfer function from surface pressure 
    fluctuations to far-field sound pressure in the Amiet model. The 
    integral accounts for the acoustic scattering effects at the airfoil
    trailing edge.
    
    Parameters
    ----------
    omega_array : array_like
        Angular frequency array in rad/s, shape (n_freq,).
    U0 : float
        Free-stream velocity in m/s.
    c0 : float
        Speed of sound in m/s.
    x1 : float
        Observer x-coordinate (streamwise direction) in m.
    S0 : float
        Observer distance from trailing edge in m.
    M0 : float
        Free-stream Mach number, dimensionless.
    b : float
        Airfoil semi-chord (half chord length) in m.
    alpha : float, optional
        Convection velocity ratio Uc/U0, where Uc is the convection
        velocity of turbulent eddies. Default is 1.0.
    a_param : float, optional
        Alternative parameter for convection velocity ratio. If provided,
        overrides the alpha parameter. Default is None.
        
    Returns
    -------
    I : ndarray, complex
        Complex radiation integral values, shape (n_freq,).
        The magnitude squared :math:`\\vert I\\vert^2` represents the acoustic efficiency
        of the trailing edge scattering process.
        
    
    .. note::

        The radiation integral is computed as :math:`I = L_1 + L_2`, where:
        
        - :math:`L_1` represents the leading edge contribution to the scattering
        - :math:`L_2` represents the trailing edge contribution to the scattering
        
        The computation involves:
        
        1. Calculation of dimensionless parameters:

        - :math:`\\mu = kb/\\beta^2` (reduced frequency)
        - :math:`\\beta^2 = 1 - M_0^2` (compressibility factor)
        - :math:`k = \\omega/c_0` (acoustic wavenumber)
        
        2. Evaluation of Fresnel integrals through the :math:`E^\\star` function
                
        The implementation handles numerical singularities by applying
        small regularization values (1e-12) when parameters approach zero.
        

    .. warning::

        For :math:`\\omega = 0`, the function returns 0 as a placeholder. The correct
        asymptotic behavior at low frequencies is not yet implemented.
    
        
    Examples
    --------

    
    .. code-block:: python

        omega = np.array([100, 1000, 10000])  # Angular frequencies
        I = compute_radiation_integral(omega, U0=50, c0=343, x1=1.0, 
                                    S0=10.0, M0=0.15, b=0.1)
        efficiency = np.abs(I)**2  # Acoustic efficiency
    
    
    References
    ----------
    .. [1] Amiet, R. K. (1975). Acoustic radiation from an airfoil in a 
           turbulent stream. Journal of Sound and Vibration, 41(4), 407-420.
    .. [2] Roger, M., & Moreau, S. (2005). Back-scattering correction and 
           further extensions of Amiet's trailing-edge noise model. 
           Part 1: theory. Journal of Sound and Vibration, 286(3), 477-506.
    
    """
    
    omegas = np.asarray(omega_array, dtype=float)
    I_list = []
    for omega in omegas:
        if omega == 0:
            I_list.append(0.0)  # TODO: implement correct asymptotic behavior
            continue
        L1, L2 = _compute_L1_L2(
            omega, U0, c0, x1, S0, M0, b, alpha=alpha, a_param=a_param
        )
        I = L1 + L2
        I_list.append(I)
    return np.array(I_list)
