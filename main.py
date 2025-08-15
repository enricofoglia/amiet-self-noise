import os.path as osp

import numpy as np
import matplotlib.pyplot as plt

import amiet_self_noise as asn


def main():
    input_data = asn.io_utils.InputData("config.yaml", normalize=True)
    input_data.print_summary()

    # Initialize the AmietModel
    model = asn.amiet_model.AmietModel(input_data)
    # Compute the PSD
    f, psd = model.compute_psd()

    f, phi_pp = model.compute_wps()

    p_ref = 2e-5  # Reference pressure in Pa
    fig, ax = plt.subplots()
    for i in range(psd.shape[1]):
        ax.semilogx(f, 10 * np.log10(psd[:, i] / p_ref**2), label=f"Obs {i + 1}")
    ax.set_xlabel(r"$f$ [Hz]")
    ax.set_ylabel(r"$10\log(S_{pp}/p^2_{\mathrm{ref}})$ [dB]")
    ax.grid()
    ax.legend()
    plt.savefig(osp.join(input_data.config.out_dir, "figures", "psd_plot.png"))

    fig, ax = plt.subplots()
    ax.semilogx(f, 10 * np.log(phi_pp / p_ref ** 2))
    ax.set_xlabel(r"$f$ [Hz]")
    ax.set_ylabel(r"$\Phi_{pp}$")
    ax.grid()
    ax.legend()
    plt.savefig(osp.join(input_data.config.out_dir, "figures", "phi_pp.png"))


if __name__ == "__main__":
    main()
