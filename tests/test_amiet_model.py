import numpy as np
import matplotlib.pyplot as plt

import amiet_self_noise as asn

from rich import print

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

    fig, ax = plt.subplots()
    ax.plot(f, psd)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("PSD")
    plt.show()
if __name__ == "__main__":
    test_amiet_model()
    print("All tests passed.")