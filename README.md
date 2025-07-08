# amiet-self-noise
## Airfoil trailing edge noise computation code. GMC729 final project

This code implements the Amiet model for airfoil trailing edge noise prediction, based on measured or simulated turbulent boundary layer statistics. The user should provide all input statistics in a `.h5` file, containing a `f` field for the acquisition frequencies, `phi_pp` for the pressure spectrum $\Phi_{pp}$, `coherence` for the span-wise coherence length $\ell_y$, and `u_c` for the convection velocity $U_c$. All these fields mush be one dimensional arrays. HDF5 (`.h5`) files are preferable to other types of files, like `.txt` files, for numerous reasons. First, they are binary files, so they are more compact, especially when the data size gets large. Secondly, they allow to store meta-data along with the actual data, which can be extremely important if the original files will be reused in the future. Finally, they make you look like a pro, without being more difficult to read or write from any programming language (like python).

## Possible features
1. We can implement a data processing module if the user has only time measurements at different microphones.
2. We can implement a data visualization module.
