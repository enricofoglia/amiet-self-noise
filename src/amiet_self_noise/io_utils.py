import os
import h5py
import yaml
from typing import Tuple

from dataclasses import dataclass, field

import numpy as np

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown


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
    data_path: str | None = None
    mesh_path: str | None = None
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
        self.n_obs = self.obs.shape[0]


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
    """Class to hold input data for the Amiet self-noise model.
    This is the main entry point for the ``amiet_self_noise`` package. This class reads
    the configuration from a YAML file and loads the data based on the specified type.
    
    .. note::
        The user should only really need to modify the configuration file to run all the 
        desired analyses. If this is not the case, please contact the developers.
    
    .. warning::
        This class currently only supports DNS data. Other data types may be added in 
        the future.

    Parameters
    ----------
    config_path: str
        The path to the configuration file in YAML format. An example of the
        configuration file is:

        .. code-block:: yaml

            L: 10.0
            T: 300.0
            U0: 340.29
            b: 1.0
            data_path: /PATH/TO/DATA.h5
            data_type: dns
            mesh_path: /PATH/TO/MESH.h5
            obs:
            - [0.0, 0.0, 0.0]
            - [1.0, 1.0, 0.0]
            xprobes: 0
            yprobes: null # use all probes in y direction

        More information on the configuration file can be found in the :ref:`dedicated 
        page <target-to-input-files>` in the documentation.
    
    Attributes
    ----------
    config: ConfigData
        The configuration data as a :mod:`ConfigData <amiet_self_noise.io_utils.ConfigData>` object.
    pos: np.array
        The positions of the sensors as a numpy array, shape (n_sensors, 3).
    pressure: np.array
        The pressure data as a numpy array, shape (n_time_steps, n_sensors).
    fs: float
        The sampling frequency in Hz, derived from the data file.

    """
    def __init__(
        self,
        config_path: str,
    ):
        self._read_config(config_path)
        self._read_data(self.config.data_type)


    def _read_data(self, data_type: str):
        match data_type:
            case "dns":
                self.data = self._read_dns_data(
                    self.config.mesh_path,
                    self.config.data_path,
                    xprobes=self.config.xprobes,
                    yprobes=self.config.yprobes,
                )
            case _:
                raise ValueError(f"Unknown data type: {data_type}")

    def _read_config(self, path: str):
        """Read the configuration from a YAML file. Output is an
        :mod:`ConfigData <amiet_self_noise.io_utils.ConfigData>` object."""
        with open(path, "r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)

        config["obs"] = np.array(config["obs"])

        self.config = ConfigData(**config)

    def _read_dns_data(
        self,
        mesh_path,
        data_path,
        xprobes: int | None = None,
        yprobes: int | None = None,
    ):
        x_idx = slice(None) if xprobes is None else xprobes
        y_idx = slice(None) if yprobes is None else yprobes
        self.pos = self._read_mesh_file_dns(mesh_path, x_idx, y_idx)
        self.pressure, self.fs = self._read_pressure_file_dns(data_path, x_idx, y_idx)

    def _read_mesh_file_dns(self, path: str, x_idx, y_idx) -> Tuple[np.array, np.array]:
        """Read the mesh file and return the x and y coordinates as numpy arrays."""
        with h5py.File(path, "r") as f:
            x = f["x"][x_idx, y_idx]
            y = f["y"][x_idx, y_idx]
            z = f["z"][x_idx, y_idx]
        return np.array([x, y, z]).T

    def _read_pressure_file_dns(
        self, path: str, x_idx, y_idx
    ) -> Tuple[np.array, np.array]:
        with h5py.File(path, "r") as f:
            p = f["pressure"][:, x_idx, y_idx]
            p_avg = f["pressure_mean"][x_idx, y_idx]
            fs = 1.0 / f["T_s"][()]  # adimensional time step

        return p.T, fs

    def print_summary(self, console: Console = None) -> None:
        """Print a detailed summary of the InputData configuration and loaded data.

        Parameters
        ----------
        console : rich.console.Console, optional
            Console instance to use for printing. If None, creates a new one.
        """
        if console is None:
            console = Console(width=80)

        # Title
        console.print(
            Markdown("# InputData Summary"), justify="center", style="bold green"
        )

        # Flow conditions section
        flow_panel = Panel(
            f"  Temperature:          [cyan]{self.config.T:.1f} K[/cyan]\n"
            f"  Free stream velocity: [cyan]{self.config.U0:.2f} m/s[/cyan]\n"
            f"  Speed of sound:       [cyan]{self.config.c0:.1f} m/s[/cyan]\n"
            f"  Mach number:          [cyan]{self.config.M0:.4f}[/cyan]",
            title="[bold]Flow Conditions[/bold]",
            title_align="left",
            highlight=True,
        )
        console.print(flow_panel)

        # Geometry section
        # Observer position
        if len(self.config.obs) <= 3:
            obs_str = f"[{', '.join(f'{x}' for x in self.config.obs)}]"
        else:
            obs_str = f"array({self.config.obs.shape})"
        geometry_panel = Panel(
            f"  Half chord (b):       [cyan]{self.config.b:.4f} m[/cyan]\n"
            f"  Full chord:           [cyan]{2 * self.config.b:.4f} m[/cyan]\n"
            f"  Span (L):             [cyan]{self.config.L:.4f} m[/cyan]\n"
            f"  Observer position:    [cyan]{obs_str} m[/cyan]",
            title="[bold]Geometry[/bold]",
            title_align="left",
            highlight=True,
        )
        console.print(geometry_panel)

        # Data section
        if hasattr(self, "pressure") and hasattr(self, "pos"):
            # Time series info
            nt, nsensors = self.pressure.shape
            duration = nt / self.fs

            # Pressure statistics
            p_rms = np.sqrt(np.mean(self.pressure**2))
            p_min, p_max = np.min(self.pressure), np.max(self.pressure)
            p_std = np.std(self.pressure)

            # Sensor spatial info
            x_range = [np.min(self.pos[:, 0]), np.max(self.pos[:, 0])]
            y_range = [np.min(self.pos[:, 1]), np.max(self.pos[:, 1])]
            z_range = [np.min(self.pos[:, 2]), np.max(self.pos[:, 2])]

            # Memory usage
            data_size_mb = (self.pressure.nbytes + self.pos.nbytes) / 1024**2
            if data_size_mb < 1:
                size_str = f"{data_size_mb * 1024:.1f} KB"
            elif data_size_mb < 1024:
                size_str = f"{data_size_mb:.1f} MB"
            else:
                size_str = f"{data_size_mb / 1024:.1f} GB"
            data_panel = Panel(
                f"  Time steps:           [cyan]{nt:,}[/cyan]\n"
                f"  Sensors:              [cyan]{nsensors}[/cyan]\n"
                f"  Sampling frequency:   [cyan]{self.fs:.0f} Hz[/cyan]\n"
                f"  Duration:             [cyan]{duration:.3f} s[/cyan]\n"
                f"  Time resolution:      [cyan]{1 / self.fs * 1000:.2f} ms[/cyan]\n"
                f"  Pressure RMS:         [cyan]{p_rms:.4e} Pa[/cyan]\n"
                f"  Pressure std:         [cyan]{p_std:.4e} Pa[/cyan]\n"
                f"  Pressure range:       [cyan][{p_min:.3e}, {p_max:.3e}] Pa[/cyan]\n"
                f"  Sensor X range:       [cyan][{x_range[0]:.3f}, {x_range[1]:.3f}] m[/cyan]\n"
                f"  Sensor Y range:       [cyan][{y_range[0]:.3f}, {y_range[1]:.3f}] m[/cyan]\n"
                f"  Sensor Z range:       [cyan][{z_range[0]:.3f}, {z_range[1]:.3f}] m[/cyan]\n"
                f"  Memory usage:         [red]{size_str}[/red]",
                title=f"[bold]Data Summary ({self.config.data_type.upper()})[/bold]",
                title_align="left",
                highlight=True,
            )
            console.print(data_panel)
        else:
            console.print("  [bold red]Status: Data not loaded[/bold red]")

        # File paths section
        if (hasattr(self.config, "mesh_path") and self.config.mesh_path) or (
            hasattr(self.config, "data_path") and self.config.data_path
        ):
            file_string = []
            if hasattr(self.config, "mesh_path") and self.config.mesh_path:
                file_string.append(
                    f"Mesh file: [green]{self.config.mesh_path}[/green]\n"
                )
            if hasattr(self.config, "data_path") and self.config.data_path:
                file_string.append(f"Data file: [green]{self.config.data_path}[/green]")
            file_panel = Panel(
                "".join(file_string),
                title="[bold]File Paths[/bold]",
                title_align="left",
                highlight=True,
            )
            console.print(file_panel)

        # Probe selection
        if (hasattr(self.config, "xprobes") and self.config.xprobes is not None) or (
            hasattr(self.config, "yprobes") and self.config.yprobes is not None
        ):
            probe_string = []
            if hasattr(self.config, "xprobes"):
                if self.config.xprobes is None:
                    xprobes = "[bold]All[/bold]"
                else:
                    xprobes = self.config.xprobes
                probe_string.append(f"  X probes:             [cyan]{xprobes}[/cyan]\n")
            if hasattr(self.config, "yprobes"):
                if self.config.yprobes is None:
                    yprobes = "[bold]All[/bold]"
                else:
                    yprobes = self.config.yprobes
                probe_string.append(f"  Y probes:             [cyan]{yprobes}[/cyan]")
            probe_panel = Panel(
                "".join(probe_string),
                title="[bold]Probe Selection[/bold]",
                title_align="left",
                highlight=True,
            )
            console.print(probe_panel)
        console.print("")  # Extra line at end


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
