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
        "obs": [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
        "U0": 340.29,
    }

    path = "test_config.yaml"
    yaml.dump(config_data, open(path, "w"))

    config = io.read_config(path)
    os.remove(path)
    print(config)


def test_memory():
    time = np.linspace(0, 1, 100)
    p1 = np.random.rand(100)
    p2 = np.random.rand(100)

    sensor1 = io.SensorData(pressure=p1, time=time)
    sensor2 = io.SensorData(pressure=p2, time=time)

    print(hex(id(sensor1.time)))
    print(hex(id(sensor2.time)))
    print(hex(id(sensor1.pressure)))
    print(hex(id(sensor2.pressure)))


def test_input_data_dns():
    mesh_path = "/home/daep/e.foglia/Documents/2A/13_gibbs/data/SherFWHsolid1_grid.h5"
    data_path = (
        "/home/daep/e.foglia/Documents/2A/13_gibbs/data/SherFWHsolid1_p_raw_data_250.h5"
    )

    config = {
        "b": 1.0,
        "T": 300.0,
        "L": 10.0,
        "obs": [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
        "U0": 340.29,
        "data_type": "dns",
        "mesh_path": mesh_path,
        "data_path": data_path,
        "xprobes": 0,
        "yprobes": None,
    }
    yaml.dump(config, open("test_config_dns.yaml", "w"))

    input_data = io.InputData("test_config_dns.yaml")

    input_data.print_summary()


if __name__ == "__main__":
    # test_read_pressure_data()
    # test_read_config()
    # test_memory()
    test_input_data_dns()
    print("[bold green]All tests passed![/bold green]")
