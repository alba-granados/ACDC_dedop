import numpy as np
import traceback

from dedop.conf import CharacterisationFile, ConstantsFile, ConfigurationFile, ACDCConfiguration
from ..base_algorithm import BaseAlgorithm
from .fit_sl_f0_model import FitSlF0ModelAlgorithm

class RetrackingAlgorithm(BaseAlgorithm):

    def __init__(self, chd: CharacterisationFile, cst: ConstantsFile,
                 cnf: ConfigurationFile, acdcCnf: ACDCConfiguration):
        super().__init__(chd, cst, cnf)

        self.acdcConfig = acdcCnf

        self.fit_sl_f0_model = FitSlF0ModelAlgorithm(chd, cst, cnf, acdcCnf)


    def __call__(self, stack_ac, k_scaled, nf_p, fit_params_ini, look_index_ref, func_f0, mask):
        try:
            # -------------------- FIRST LEVEL FITTING ACDC STACK - -------------------
            # --------------------------------------------------------------------------
            # Re - order the AC stack
            stack_1D = np.reshape(stack_ac, (1, nf_p.Neff * (self.chd.n_samples_sar * self.cnf.zp_fact_range)))[0]
            mask_1D = np.reshape(mask, (1, nf_p.Neff * (self.chd.n_samples_sar * self.cnf.zp_fact_range)))[0]
            mask_1D = np.array([bool(x) for x in mask_1D])
            stack_1D = stack_1D[mask_1D]
            N_samples_sar_chd_stack_1D = len(np.where(mask_1D == 1)[0])
            # Re - order the scaled range
            k_scaled_1D = np.reshape(k_scaled, (1, nf_p.Neff * (self.chd.n_samples_sar * self.cnf.zp_fact_range)))[0]
            k_scaled_1D = k_scaled_1D[mask_1D]

            # -------------------- MULTILOOKING OF THE ACDC - -------------------------
            # -------------------------------------------------------------------------
            kmin = np.floor(np.amin(k_scaled_1D))
            kmax = np.floor(np.amax(k_scaled_1D))
            if self.acdcConfig.weighting_win_type.lower() == 'gaussian':
                k_ml_ACDC = np.arange(kmin, kmax+self.acdcConfig.weighting_win_width, self.acdcConfig.weighting_win_width)
                N_samples_sar_chd_ACDC = len(k_ml_ACDC)

                matrix_weighting = np.exp(-(1.0 *(np.ones((N_samples_sar_chd_ACDC, 1)) * k_scaled_1D -
                                    (np.outer(k_ml_ACDC.transpose(), np.ones((1, N_samples_sar_chd_stack_1D)))))) ** 2 /
                                    (2 * self.acdcConfig.weighting_win_width ** 2))

                matrix_weighting = matrix_weighting / np.matmul(np.matmul(matrix_weighting,
                                                                          np.ones((N_samples_sar_chd_stack_1D, 1))),
                                                                          np.ones((1, N_samples_sar_chd_stack_1D)))

                waveform_ml_ACDC = np.matmul(matrix_weighting, stack_1D.transpose()).transpose()

            else:
                print('No valid weighting function')
                return [],[],[],-1,[],0,0

            # -------------------- FILTER SAMPLES BEGINNING/END FITTING --------------
            if self.acdcConfig.wvfm_discard_samples:
                N_samples_sar_chd_ACDC_ml = len(k_ml_ACDC)
                start_sample = np.min([0 + self.acdcConfig.wvfm_discard_samples_begin, N_samples_sar_chd_ACDC_ml])
                stop_sample = np.max([0, N_samples_sar_chd_ACDC_ml - self.acdcConfig.wvfm_discard_samples_end])

                k_ml_ACDC_int = k_ml_ACDC[start_sample : stop_sample]
                waveform_ml_ACDC_int = waveform_ml_ACDC[start_sample : stop_sample]

            else:
                k_ml_ACDC_int = k_ml_ACDC
                waveform_ml_ACDC_int = waveform_ml_ACDC
                start_sample = 0
                stop_sample = len(waveform_ml_ACDC)


            # -------------------- FITTING OF THE MULTILOOKED ACDC - ------------------
            # --------------------------------------------------------------------------
            estimates, ml_wav_fitted = self.fit_sl_f0_model(waveform_ml_ACDC_int, k_ml_ACDC_int, nf_p,
                                                 [fit_params_ini[3],fit_params_ini[1],fit_params_ini[2]], look_index_ref, func_f0)


            # differential error of the epoch
            estimates = np.append(estimates, estimates[0])

            # epoch: add the estimated error over the initial epoch
            estimates[0] = estimates[0] + fit_params_ini[0]

            return waveform_ml_ACDC,k_ml_ACDC,estimates,0,ml_wav_fitted,start_sample,stop_sample

        except Exception as exp:
            print("Exception:",exp)
            traceback.print_exc()
            return [],[],[],-1,[],0,0