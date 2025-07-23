import os

from dataclasses import dataclass, field

import numpy as np


@dataclass
class InputData:
    """Class to hold input data.
    
    Parameters
    ----------
    
    b: float
        Half the chord of the airfoil, in meters.
    T: float
        The temperature in Kelvin.
    L: float
        The span of the airfoil, in meters.
    obs: np.array
        Observers location, as a numpy array.
    """
    b: float
    T: float
    L: float
    obs: np.array
    c0: float = field(init=False) #
    """The speed of sound at the given temperature, calculated as :math:`\\sqrt{\\gamma R T}` 
    where :math:`R=287.05\\;\\mathrm{J\\cdot kg^{-1}\\cdot K^{-1}}` and :math:`\\gamma=1.4`."""

    def __post_init__(self):
        self.c0 = np.sqrt(1.4 * 287.05 * self.T)  