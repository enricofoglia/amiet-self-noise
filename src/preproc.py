from typing import Tuple

import numpy as np
import scipy.signal as ss

def spectrum(
        data: np.array,
        filter: bool = False,
        average: bool = True,
        **kwargs
) -> Tuple[np.array, np.array]:
    '''Compute the power spectral density of a signal.
    
    Parameters
    ----------
    data: np.array
        input data. Can be one or two dimensional.
    filter: bool
        if True, prefilter the signal (default False).
    average: bool
        if True and a data is a multidimensional array, compute the average over the extra dimension (default True)

    Return
    ------
    f: np.array
        Frequency array
    spp: np.array
        Power spectral density array
    '''
    pass