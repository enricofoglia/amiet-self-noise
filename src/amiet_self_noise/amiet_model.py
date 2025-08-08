import numpy as np

import amiet_self_noise.preproc as preproc
import amiet_self_noise.radiation_integral as ri

class AmietModel:
    def __init__(
            self,
            input_data,
    ):
        self.input_data = input_data

    def compute_psd(
            self
    ):
        f, phi_pp = self.compute_wps()
        _, ly = self.compute_coherence()
        

        psd = np.zeros([len(f), self.input_data.config.n_obs])
        for i, observer in enumerate(self.input_data.config.obs):

            I = np.abs(self.compute_radiation_integral(f, observer)) ** 2
            beta2 = 1 - self.input_data.config.M0**2
            S02 = observer[0]**2 + beta2 * (observer[1]**2 + observer[2]**2)
            directivity = (observer[2]*f*self.input_data.config.b / 
                           self.input_data.config.c0 / S02)**2 
            psd[:, i] = directivity * 2 * self.input_data.config.L * phi_pp * ly * I

        return f, psd
    
    def compute_wps(
            self
    ):
        f, phi_pp = preproc.spectrum(
            self.input_data.pressure,
            fs = self.input_data.fs,
            filter = False,
            avg = 0
        )

        return f, phi_pp
    
    def compute_coherence(
            self
    ):
        f, ly = preproc.coherence_length(
            self.input_data.pressure,
            z = self.input_data.pos[:, 2],
            ref_index = self.input_data.pos.shape[0] // 2,
            fs = self.input_data.fs,
            filter = False,
        )
        return f, ly
    
    def compute_radiation_integral(
            self,
            f,
            observer
    ):
        beta2 = 1 - self.input_data.config.M0**2
        S0 = np.sqrt(observer[0]**2 + beta2 * (observer[1]**2 + observer[2]**2))
        I = ri.compute_radiation_integral(
            omega_array=f * 2 * np.pi,  # Convert frequency to angular frequency
            U0=self.input_data.config.U0,
            c0=self.input_data.config.c0,
            x1=observer[0],
            S0=S0,
            M0=self.input_data.config.M0,
            b=self.input_data.config.b,
            alpha = 0.7 # TODO: make this a parameter in the config

        )

        return I
