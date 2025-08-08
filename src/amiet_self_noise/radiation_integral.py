import numpy as np
from scipy.special import fresnel

def E_etoile(x):
#Implementation compatible avec la convention utilisée E^*(x). Pour x <= 0 on remplace par une valeur positive.
    x = np.asarray(x, dtype=np.float64)    # évite racine de négatif / zéro
    xpos = np.maximum(x, 1e-12)
    arg = np.sqrt(2.0 * xpos / np.pi)
    S, C = fresnel(arg)      
# On renvoie C-i*S,
    return C-1j*S

## On calcule la valeur de G

def compute_G(D, mu, epsilon):
    E_etoile_4mu = E_etoile(4.0 * mu)        
    E_4mu = np.conj(E_etoile_4mu)            
    E_etoile_2D = E_etoile(2.0 * D)          

    Dm2mu = D - 2.0 * mu
    Dp2mu = D + 2.0 * mu
    Dm2mu = np.where(np.abs(Dm2mu) < 1e-12, 1e-12, Dm2mu)
    Dp2mu = np.where(np.abs(Dp2mu) < 1e-12, 1e-12, Dp2mu)

    term1 = (1.0 + epsilon) * np.exp(1j * (D + 2.0 * mu)) * np.sin(D - 2.0 * mu) / Dm2mu
    term2 = (1.0 - epsilon) * np.exp(1j * (D - 2.0 * mu)) * np.sin(D + 2.0 * mu) / Dp2mu

    term3 = (1.0 + epsilon) * (1.0 - 1j) / (2.0 * Dm2mu) * np.exp(1j * 4.0 * mu) * E_etoile_4mu
    term4 = -(1.0 - epsilon) * (1.0 + 1j) / (2.0 * Dp2mu) * np.exp(-1j * 4.0 * mu) * E_4mu

    sqrt_factor = np.sqrt(2.0 * mu / D)
    x = ( (1.0 - epsilon) * (1.0 + 1j) / Dp2mu - (1.0 + epsilon) * (1.0 - 1j) / Dm2mu )
    term5 = 0.5 * np.exp(2j * D) / sqrt_factor * E_etoile_2D * x

# Somme finale
    G = term1 + term2 + term3 + term4 + term5
    return G

##  Expressions analytiques L1, L2 (trailing edge)
def compute_L1_L2(omega, U0, c0, x1, S0, M0, b, alpha=1.0, a_param=None):

# On calcule L1 et L2 pour une fréquence angulaire omega
    if a_param is None:
        a_param = alpha

    Uc = U0 * alpha
   
# Information à modifier en fonction des données du prof.
    k = omega / c0                
    beta2 = 1.0 - M0**2
    mu = k / beta2 *b               
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
    E_etoile_2B = E_etoile(2.0 * B)
    E_etoile_2Bminus2C = E_etoile(2.0 * (B - C))
   
    prefacteur = - np.exp(2j * C) / (1j * C)
    term1 = (1.0 + 1j) * np.exp(-2j * C) * np.sqrt(B / (B - C)) * E_etoile_2Bminus2C
    term2 = - (1.0 + 1j) * E_etoile_2B
    term3 = 1.0 
    L1 = prefacteur * (term1 + term2 + term3)
   
 
## On calcule L2
    D = mu * (1.0 - x1 / S0)
    Theta = np.sqrt((K1_bar + mu * (M0 + 1.0)) / (k1_bar + mu * (M0 + 1.0)))
# Correction imaginaire ϵ (epsilon)
    eps = (1.0 + 1.0 / (4.0 * mu))**(-0.5) if mu != 0 else 1.0
# -> si Θ≈1 alors le numerateur peut être 0
    H = (1.0 + 1j) * np.exp(-1j * 4.0 * mu) * (1.0 - Theta**2)
    H = H / (np.sqrt(np.pi * B) * (alpha - 1.0) * k1_bar + 1e-30)
# Evaluer E*(4µ)
    E_etoile_4mu = E_etoile(4.0 * mu)
    # G = 1.0 # !!!
    G = compute_G(D, mu, eps) 
# Construction L2
    term_L2_a = np.exp(1j * 4.0 * mu) * (1.0 - (1.0 + 1j) * E_etoile_4mu)  
    term_L2_b = - np.exp(2j * D)
    term_L2_c = 1j * (D + k1_bar + (M0 - 1.0) * mu) * G
   
    L2 = H * (term_L2_a + term_L2_b + term_L2_c)
   
    return L1, L2


##  Fonction principale
def compute_radiation_integral(omega_array, U0, c0, x1, S0, M0, b, alpha=1.0, a_param=None):
    omegas = np.asarray(omega_array, dtype=float)
    I_list = []
    for omega in omegas:
        if omega == 0:
            I_list.append(0.0) # TODO: implement correct asymptotic behavior
            continue
        L1, L2 = compute_L1_L2(omega, U0, c0, x1, S0, M0, b, alpha=alpha, a_param=a_param)
        I = L1 + L2
        I_list.append(I)
    return np.array(I_list)