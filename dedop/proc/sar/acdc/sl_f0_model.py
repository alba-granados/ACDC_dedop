import math as m
import numpy as np

from dedop.conf import CharacterisationFile, ConstantsFile, ConfigurationFile, ACDCConfiguration
from ..base_algorithm import BaseAlgorithm
from dedop.conf.enums import RangeIndexMethod

class SlF0ModelAlgorithm(BaseAlgorithm):

    def __init__(self, chd: CharacterisationFile, cst: ConstantsFile,
                 cnf: ConfigurationFile, acdcCnf: ACDCConfiguration):
        super().__init__(chd, cst, cnf)

        self.acdcConfig = acdcCnf

    def __call__(self, params, k, ThN, func_f0):

        gk = (k - params[0]) * params[1]
        waveform_ml_ACDC = np.zeros_like(gk)

        for i in range(0, gk.size):
            if self.acdcConfig.LUT_ximin <= gk[i] <= self.acdcConfig.LUT_ximax:
                ind2func_f0 = m.floor((gk[i] - self.acdcConfig.LUT_ximin) / self.acdcConfig.LUT_step)
                waveform_ml_ACDC[i] = func_f0[ind2func_f0]

            elif gk[i] > self.acdcConfig.LUT_ximax:
                waveform_ml_ACDC[i] = np.sqrt(np.pi / (2.0 * gk[i])) * (1 + 3 / (8 * (gk[i]) ** 2) + 105 / (16 * 8 * (gk[i]) ** 4))

        # N_samples_sar_chd corresponds to non-zero padded ones
        if self.acdcConfig.range_index_method == RangeIndexMethod.conventional:
            waveform_ml_ACDC = np.sqrt(1 / self.chd.t0_nom / self.chd.bw_ku) * np.sqrt(self.cnf.zp_fact_range) * params[2] * waveform_ml_ACDC + ThN
        elif self.acdcConfig.range_index_method == RangeIndexMethod.resampling:
            waveform_ml_ACDC = np.sqrt(1 / self.chd.t0_nom / self.chd.bw_ku) * params[2] * waveform_ml_ACDC + ThN

        return waveform_ml_ACDC