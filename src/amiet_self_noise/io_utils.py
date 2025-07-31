import os
import h5py
import yaml
from typing import Tuple

from dataclasses import dataclass, field

import numpy as np


@dataclass
class ConfigData:
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
        Observers location in cartesian coordinates, as a numpy array.
    U0: float
        The free stream velocity, in meters per second.
    data_type: str
        The type of data. Currently only 'dns' is supported.
    data_path: str
        The path to the data file.
    """

    b: float
    T: float
    L: float
    obs: np.array
    U0: float
    data_type: str
    mesh_path: str | None = None
    data_path: str | None = None
    xprobes: int | None = None
    yprobes: int | None = None

    # post init fields
    c0: float = field(init=False)  #
    """The speed of sound at the given temperature, calculated as :math:`\\sqrt{\\gamma R T}` 
    where :math:`R=287.05\\;\\mathrm{J\\cdot kg^{-1}\\cdot K^{-1}}` and :math:`\\gamma=1.4`."""
    M0: float = field(init=False)
    """Mach number relative to the free stream velocity"""


    def __post_init__(self):
        self.c0 = np.sqrt(1.4 * 287.05 * self.T)
        self.M0 = self.U0 / self.c0

@dataclass
class SensorData:
    """Class to hold sensor data.

    Parameters
    ----------
    pressure: np.array
        Pressure data as a numpy array.
    fs: float 
        Sampling frequency in Hz.
    position: np.array, optional
        Position as a numpy array. Default is None.
    """

    pressure: np.array
    fs: float 
    position: np.array = None



class InputData:
    def __init__(
            self,
            config_path: str,
    ):
        
        self.read_config(config_path)
        self.read_data(self.config.data_type)    

    def read_data(self, data_type: str):
        match data_type:
            case "dns":
                self.data = self.read_dns_data(self.config.mesh_path,
                                               self.config.data_path, 
                                               hprobes=self.config.hprobes, 
                                               vprobes=self.config.vprobes)
            case _:
                raise ValueError(f"Unknown data type: {data_type}")
            
        
    def read_config(
            self,
            path: str
    ):
        """Read the configuration from a YAML file. Output is an 
        :mod:`ConfigData <amiet_self_noise.io_utils.ConfigData>` object."""
        with open(path, 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        
        # Convert obs to numpy array if it's a list
        if isinstance(config['obs'], list):
            config['obs'] = np.array(config['obs'])

        self.config = ConfigData(**config)
            
    def read_dns_data(self, mesh_path, data_path, xprobes: int | None = None, yprobes: int | None= None):
        x_idx = slice(None) if xprobes is None else xprobes
        y_idx = slice(None) if yprobes is None else yprobes 
        self.pos = self._read_mesh_file_dns(mesh_path, x_idx, y_idx)
        self.pressure, self.fs = self._read_pressure_file_dns(data_path, x_idx, y_idx)
        

    def _read_mesh_file_dns(self, path: str, x_idx, y_idx ) -> Tuple[np.array, np.array]:
        """Read the mesh file and return the x and y coordinates as numpy arrays."""
        with h5py.File(path, "r") as f:
            x = f['x'][x_idx, y_idx]
            y = f['y'][x_idx, y_idx]
            z = f['z'][x_idx, y_idx]
        return np.array([x, y, z]).T
    
    def _read_pressure_file_dns(self, path: str, x_idx , y_idx) -> Tuple[np.array, np.array]:
        with h5py.File(path, "r") as f:
            p = f['pressure'][:, x_idx, y_idx]
            p_avg = f['pressure_mean'][x_idx, y_idx]
            fs = 1./f['T_s'][()]  # adimensional time step

        return p, fs


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

