import os.path as osp

import yaml

import numpy as np
import matplotlib.pyplot as plt

import amiet_self_noise as asn

from rich import print

OUTPUT_DIR = (
    "/home/daep/e.foglia/Documents/2A/01_cours/UdeS/02_aeroscoustics/project/out/"
)
FIG_DIR = osp.join(OUTPUT_DIR, "figures")
p_ref = 2e-5  # Reference pressure in Pa


def test_stats():
    input_data = asn.io_utils.InputData("config_test_amiet_model.yaml")

    # Initialize the AmietModel
    model = asn.amiet_model.AmietModel(input_data)

    f, phi_pp = model.compute_wps()
    f, ly = model.compute_coherence()

    span = np.abs(input_data.pos[-1, 2] - input_data.pos[0, 2])

    fig, axs = plt.subplots(1, 2, layout="tight")
    axs[0].semilogx(f, 10 * np.log10(phi_pp / p_ref**2))
    axs[0].set_title("WPS")
    axs[0].set_xlabel("Frequency (Hz)")
    axs[0].set_ylabel(r"PSD (dB/Hz)")
    axs[0].grid()
    axs[1].semilogx(f, ly / span)
    axs[1].set_title("Coherence Length")
    axs[1].set_xlabel("Frequency (Hz)")
    axs[1].set_ylabel(r"$l_y/L$ (-)")
    axs[1].grid()

    plt.savefig(osp.join(FIG_DIR, "stats_test_plot.png"))

    assert f.shape[0] > 0, "Frequency array should not be empty."
    assert phi_pp.shape[0] > 0, "WPS should not be empty."
    assert ly.shape[0] > 0, "Coherence length array should not be empty."
    print("[bold green]Stats test passed![/bold green]")


def test_amiet_model():
    # Create mock input data

    input_data = asn.io_utils.InputData("config_test_amiet_model.yaml")
    input_data.print_summary()

    # Initialize the AmietModel
    model = asn.amiet_model.AmietModel(input_data)

    # Compute the PSD
    f, psd = model.compute_psd()

    # Assertions to check if the output is as expected
    assert f.shape[0] > 0, "Frequency array should not be empty."
    assert psd.shape[0] > 0, "PSD should not be empty."

    print("[bold green]AmietModel test passed![/bold green]")

    input_data = asn.io_utils.InputData("config_test_amiet_model.yaml", normalize=True)
    model = asn.amiet_model.AmietModel(input_data)
    f_norm, psd_norm = model.compute_psd()

    input_data = asn.io_utils.InputData("config_test_amiet_model.yaml", normalize=False)
    model = asn.amiet_model.AmietModel(input_data)
    f_adim, psd_adim = model.compute_psd()

    fig, ax = plt.subplots()
    for i in range(psd.shape[1]):
        ax.semilogx(f, 10 * np.log10(psd[:, i] / p_ref**2), label=f"Obs {i + 1}")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("PSD")
    ax.legend()
    plt.savefig(osp.join(FIG_DIR, "amiet_model_test_plot.png"))

    fig, ax = plt.subplots()
    ax.semilogx(f_norm, 10 * np.log10(psd_norm[:, 0] / p_ref**2), label="Dimensional")
    ax.semilogx(f_adim, 10 * np.log10(psd_adim[:, 0] / p_ref**2), label="Adimensional")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("PSD")
    ax.legend()
    plt.savefig(osp.join(FIG_DIR, "amiet_model_test_plot_norm.png"))


def test_radiation_integral():
    omega_vals = np.linspace(100, 2000, 100)  # fréquences en rad/s
    U = 50  # m/s
    T = 300.0  # K
    c0 = np.sqrt(1.4 * 287 * T)  # m/s
    x1 = 10.0  # position observateur
    M = U / c0  # nombre de Mach
    S0 = np.sqrt(x1**2 + (1 - M**2) * (0.0**2 + 0.0**2))  # S0 pour l'observateur
    b = 1.0

    I_values = asn.radiation_integral.compute_radiation_integral(
        omega_vals, U, c0, x1, S0, M, b, alpha=0.7
    )

    config = {
        "L": 10.0,
        "b": b,  # demi-envergure
        "T": 300.0,  # température en K
        "obs": [[x1, 0.0, 0.0]],  # position de l'observateur
        "U0": U,  # vitesse du vent en m/s
        "rho": 1.225,
        "data_path": "/home/daep/e.foglia/Documents/2A/13_gibbs/data/SherFWHsolid1_p_raw_data_250.h5",
        "data_type": "dns",
        "mesh_path": "/home/daep/e.foglia/Documents/2A/13_gibbs/data/SherFWHsolid1_grid.h5",
        "xprobes": 0,
        "yprobes": 0,
    }

    yaml.dump(config, open("config_test_radiation_integral.yaml", "w"))
    input_data = asn.io_utils.InputData("config_test_radiation_integral.yaml")
    model = asn.amiet_model.AmietModel(input_data)
    I = model.compute_radiation_integral(
        omega_vals / 2 / np.pi, input_data.config.obs[0]
    )

    fig, ax = plt.subplots(1, 2, layout="tight")
    ax[0].plot(omega_vals, I_values.real, label="Re(I)")
    ax[0].plot(omega_vals, I_values.imag, label="Im(I)")
    ax[0].plot(omega_vals, I.real, linestyle="--", color="tab:blue", label="Re(I)")
    ax[0].plot(omega_vals, I.imag, linestyle="--", color="tab:orange", label="Im(I)")
    ax[0].set_xlabel(r"$\omega$ (rad/s)")
    ax[0].set_ylabel(r"$I(\omega)$")
    ax[0].legend()
    ax[0].grid()
    ax[1].plot(
        omega_vals, 10 * np.log10(np.abs(I_values) ** 2 / p_ref**2), label="|I|^2"
    )
    ax[1].plot(
        omega_vals,
        10 * np.log10(np.abs(I) ** 2 / p_ref**2),
        label="|I|^2",
        linestyle="--",
        color="tab:blue",
    )
    ax[1].set_xlabel(r"$\omega$ (rad/s)")
    ax[1].set_ylabel(r"$\vert I(\omega)\vert^2$")
    ax[1].legend()
    ax[1].grid()

    plt.savefig(osp.join(FIG_DIR, "radiation_integral_test_plot.png"))
    assert I_values.shape == omega_vals.shape, (
        "Output shape should match input omega shape."
    )
    print("[bold green]Radiation integral test passed![/bold green]")


if __name__ == "__main__":
    test_radiation_integral()
    test_amiet_model()
    test_stats()
    print("All tests passed.")
