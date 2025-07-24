import os
import h5py
import yaml

import numpy as np

from rich import print

import amiet_self_noise.io_utils as io


def test_read_pressure_data():
    pressure = np.random.rand(100, 1)
    time = np.linspace(0, 1, 100).reshape(-1, 1)

    path = "test_pressure_data.h5"
    with h5py.File(path, "w") as f:
        f.create_dataset("pressure", data=pressure)
        f.create_dataset("time", data=time)
    print(f"[bold green]Created test file {path}[/bold green]")
    pressure_out, time_out = io.read_pressure_data(path)
    print(f"[bold green]Read pressure data from {path}[/bold green]")
    assert pressure_out.ndim == 1
    assert time_out.ndim == 1  # removed empty dimension
    print(f"[bold green]Test passed![/bold green]")
    os.remove(path)

def test_read_config():
    config_data = {
        "b": 1.0,
        "T": 300.0,
        "L": 10.0,
        "obs": [0.0, 0.0, 0.0],
        "U0": 340.29
    }

    path = "test_config.yaml"
    yaml.dump(config_data, open(path, "w"))
    
    config = io.read_config(path)
    os.remove(path)
    print(config)
    

if __name__ == "__main__":
    test_read_pressure_data()
    test_read_config()
    print("[bold green]All tests passed![/bold green]")
