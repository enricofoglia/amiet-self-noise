import numpy as np
from scipy.special import fresnel
from scipy.integrate import quad

# E^*(x) = Fresnel
def E_star(x):
    x = np.maximum(x, 1e-10) 
    S, C = fresnel(np.sqrt(2 * x / np.pi))
    return C - 1j * S

# f1 = main trailing-edge term
def f1(X, k1_bar, m_bar, k_bar, M):
    B = k1_bar + M * m_bar + k_bar
    return (1 + 1j) * E_star(-B * X) - 1

# f2 = leading-edge back-scattering correction
def f2(X, k1_bar, m_bar, k_bar, M, a):
    B = k1_bar + M * m_bar + k_bar
    Y = np.sqrt((k1_bar + M * m_bar + k_bar) / B)
    H = ((1 + 1j) * np.exp(-4j * k_bar) / (2 * np.sqrt(np.pi))) * (1 - Y**2) / (a - 1) / B

    phase_exp = np.exp(1j * (k1_bar + M * m_bar - k_bar) * X)
    E_term = lambda x: np.exp(2j * k_bar * x) * (1 - (1 + 1j) * E_star(2 * k_bar * x))

    dE_dX = lambda X: (E_term(X + 2) - E_term(X + 2 - 1e-5)) / 1e-5  # finite difference

    curly = E_term(X + 2)
    dcurly = dE_dX(X)

    return H * phase_exp * (1j * (k1_bar + M * m_bar - k_bar) * curly + dcurly)

# total f = f1 + f2
def f_total(X, k1_bar, m_bar, k_bar, M, x1, S0, a):
    return f1(X, k1_bar, m_bar, k_bar, M) + f2(X, k1_bar, m_bar, k_bar, M, a)

# function
def phase(X, k1_bar, m_bar, M, x1, S0):
    C = k1_bar - m_bar * x1 / S0 - M
    return np.exp(-1j * C * X)

# total
def integrand(X, k1_bar, m_bar, k_bar, M, x1, S0, a):
    return f_total(X, k1_bar, m_bar, k_bar, M, x1, S0, a) * phase(X, k1_bar, m_bar, M, x1, S0)

# compute I(ω) for a list of ω values :
def compute_radiation_integral(omega_array, U, c0, x1, S0, M, a=None):
    if a is None:
        a = U / (0.7 * U)  # default: U_c = 0.7*U

    I_array = []

    for omega in omega_array:
        k = omega / c0
        K = omega / U
        beta2 = 1 - M**2
        m_bar = K * M / beta2
        b = 1  # non dimensionalization by half-chord
        k1_bar = K * b
        k_bar = m_bar  # for K2 = 0

        # numerical integration over X in [-2, 0]
        real_part = quad(lambda X: np.real(integrand(X, k1_bar, m_bar, k_bar, M, x1, S0, a)), -2, 0)[0]
        imag_part = quad(lambda X: np.imag(integrand(X, k1_bar, m_bar, k_bar, M, x1, S0, a)), -2, 0)[0]
        I_array.append(real_part + 1j * imag_part)

    return np.array(I_array)

