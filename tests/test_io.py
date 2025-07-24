import os
import h5py


import numpy as np

from rich import print as rprint

import amiet_self_noise.io as io


def test_read_pressure_data():
    pressure = np.random.rand(100, 1)
    time = np.linspace(0, 1, 100).reshape(-1, 1)

    path = "test_pressure_data.h5"
    with h5py.File(path, "w") as f:
        f.create_dataset("pressure", data=pressure)
        f.create_dataset("time", data=time)
    rprint(f"[bold green]Created test file {path}[/bold green]")
    pressure_out, time_out = io.read_pressure_data(path)
    rprint(f"[bold green]Read pressure data from {path}[/bold green]")
    assert pressure_out.ndim == 1
    assert time_out.ndim == 1  # removed empty dimension
    rprint(f"[bold green]Test passed![/bold green]")
    os.remove(path)


if __name__ == "__main__":
    test_read_pressure_data()
    rprint("[bold green]All tests passed![/bold green]")
