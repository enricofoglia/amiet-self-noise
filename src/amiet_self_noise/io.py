import os
import h5py
from typing import Tuple

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
    U0: float
        The free stream velocity, in meters per second.
    """

    b: float
    T: float
    L: float
    obs: np.array
    U0: float

    # post init fields
    c0: float = field(init=False)  #
    """The speed of sound at the given temperature, calculated as :math:`\\sqrt{\\gamma R T}` 
    where :math:`R=287.05\\;\\mathrm{J\\cdot kg^{-1}\\cdot K^{-1}}` and :math:`\\gamma=1.4`."""
    M0: float = field(init=False)
    """Mach number relative to the free stream velocity"""

    def __post_init__(self):
        self.c0 = np.sqrt(1.4 * 287.05 * self.T)
        self.M0 = self.U0 / self.c0


def read_pressure_data(
    path: str, pressure_key: str = "pressure", time_key: str = "time"
) -> Tuple[np.array, np.array]:
    """Read pressure data from a .h5 file and return the data as a numpy array.

    Parameters
    ----------
    path: str
        The path to the .h5 file.
    pressure_key: str
        The key for the pressure data in the .h5 file. Default is 'pressure'.
    time_key: str
        The key for the time data in the .h5 file. Default is 'time'.

    Returns
    -------
    pressure: np.array
        The pressure data as a numpy array.
    time: np.array
        The time data as a numpy array.
    """
    with h5py.File(path, "r") as f:
        pressure = f[pressure_key][:]
        time = f[time_key][:]

    pressure = np.array(pressure)
    time = np.array(time)

    return pressure.squeeze(), time.squeeze()
