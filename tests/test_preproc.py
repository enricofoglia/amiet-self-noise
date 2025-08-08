import os.path as osp

import numpy as np
import matplotlib.pyplot as plt

import amiet_self_noise.preproc as preproc

from rich import print

OUTPUT_DIR = (
    "/home/daep/e.foglia/Documents/2A/01_cours/UdeS/02_aeroscoustics/project/out/"
)
FIG_DIR = osp.join(OUTPUT_DIR, "figures")


def test_wps():
    print("[bold blue]Testing WPS computation...[/bold blue]")
    # Generate synthetic pressure data
    fs = 1000  # Sampling frequency
    t = np.linspace(0, 1, fs, endpoint=False)  # Time vector
    pressure = [
        np.sin(2 * np.pi * 100 * t) + np.random.normal(0, 0.5, fs) for _ in range(20)
    ]
    pressure = np.array(pressure)  # Shape (10, fs)

    # Compute the power spectral density using the spectrum function
    f, spp = preproc.spectrum(pressure, fs=fs, filter=False, avg=None)
    _, spp_avg = preproc.spectrum(pressure, fs=fs, filter=False, avg=0)

    # Plot the results
    fig, ax = plt.subplots()
    for i in range(spp.shape[0]):
        ax.semilogx(
            f, 10 * np.log10(spp[i] / 2e-12), linewidth=0.5, color="black", alpha=0.5
        )
    ax.semilogx(
        f, 10 * np.log10(np.mean(spp, axis=0) / 2e-12), linewidth=2, color="black"
    )
    ax.semilogx(f, 10 * np.log10(spp_avg / 2e-12), linewidth=2, color="red")
    ax.set_title("Power Spectral Density")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel(r"PSD (dB/Hz)")
    ax.grid()
    plt.savefig(osp.join(FIG_DIR, "wps_test_plot.png"))
    plt.close()

    print("Saved WPS test plot as wps_test_plot.png")

    assert spp.ndim == 2, "spp should be a 2D array"
    assert spp_avg.ndim == 1, "spp_avg should be a 1D array"
    assert np.allclose(np.mean(spp, axis=0), spp_avg), (
        "Mean of spp should equal spp_avg"
    )

    print("[bold blue]WPS computation test passed![/bold blue]")


def test_coherence_length():
    print("[bold blue]Testing coherence length computation...[/bold blue]")
    # Generate synthetic pressure data
    fs = 1000  # Sampling frequency
    t = np.linspace(0, 1, fs, endpoint=False)  # Time vector
    pressure = [
        np.sin(2 * np.pi * 100 * t) + np.random.normal(0, 0.5, fs) for _ in range(50)
    ]
    pressure = np.array(pressure)  # Shape (10, fs)
    z = np.linspace(0, 1, pressure.shape[0])  # Sensor positions

    # Compute the power spectral density using the spectrum function
    f, ly = preproc.coherence_length(
        pressure, z, ref_index=z.shape[0] // 2, fs=fs, filter=False
    )

    # Plot the results
    fig, ax = plt.subplots()
    ax.semilogx(f, ly, linewidth=2, color="black")
    ax.set_title("Coherence Length")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel(r"$\ell_y$ (-)")
    ax.grid()
    plt.savefig(osp.join(FIG_DIR, "coherence_legth_test_plot.png"))
    plt.close()

    print("Saved WPS test plot as coherence_length_test_plot.png")

    assert ly.ndim == 1, "ly should be a 1D array"
    assert ly.shape[0] == f.shape[0], "ly and f should have the same length"
    assert np.all(ly >= 0), "Coherence length should be non-negative"

    print("[bold blue]Coherence length computation test passed![/bold blue]")


if __name__ == "__main__":
    test_wps()
    test_coherence_length()
    print("[bold green]Test completed successfully.[/bold green]")
