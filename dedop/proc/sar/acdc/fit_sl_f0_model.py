import numpy as np
import scipy.optimize as spo

from dedop.conf import CharacterisationFile, ConstantsFile, ConfigurationFile, ACDCConfiguration
from ..base_algorithm import BaseAlgorithm
from .sl_f0_model import SlF0ModelAlgorithm

class FitSlF0ModelAlgorithm(BaseAlgorithm):

    def __init__(self, chd: CharacterisationFile, cst: ConstantsFile,
                 cnf: ConfigurationFile, acdcCnf: ACDCConfiguration):
        super().__init__(chd, cst, cnf)

        self.acdcConfig = acdcCnf

        self.sl_f0_model = SlF0ModelAlgorithm(chd, cst, cnf, acdcCnf)

    def __call__(self, waveform, k, nf_p, fit_params_ini, look_index_ref, func_f0):
        # -------------------- NORMALIZATION OF DATA - ----------------------------
        # --------------------------------------------------------------------------
        max_waveform = np.amax(waveform)
        fit_data = waveform / max_waveform

        # -------------------- PROVIDE initial fittings conversion - ----------------
        sigmaz = fit_params_ini[1] / 4
        fit_params_ini[1] = np.sqrt(2 * nf_p.alphag_a * nf_p.alphag_r / (nf_p.alphag_a + nf_p.alphag_r * 4 * (
                            nf_p.Lx / nf_p.Ly) ** 4 * look_index_ref ** 2 + 2 * nf_p.alphag_a * nf_p.alphag_r * (
                            sigmaz / nf_p.Lz) ** 2))  # define the gl parameter to use in fitting


        # -------------------- PRE - PROCESSING & NOISE ESTIMATION - ----------------
        # -------------------------------------------------------------------------
        # Pre - processing
        # -------------------------------------------------------------------------
        if self.acdcConfig.Thn_flag and self.acdcConfig.fit_noise:
            # used to estimate the initial value of the epoch
            # & eventually if desired the noise floor
            peak_pow = np.amax(fit_data)
            idx_max_peak = np.argmax(fit_data)
            idx_leading_edge = np.where(np.where(fit_data <= self.acdcConfig.percent_leading_edge / 100.0 * peak_pow)[0] < idx_max_peak)[0]
            idx_leading_edge = idx_leading_edge[len(idx_leading_edge)-1]
            if idx_leading_edge < 1:
                # if there is no leading edge or the waveform has displaced that
                # much from the window to the left select the peak as leading
                # edge
                idx_leading_edge = idx_max_peak

            # noise floor estimation
            idx_noise = []
            temp_noise_thr = self.acdcConfig.threshold_noise
            iter_noise = 1
            while len(idx_noise) == 0 and iter_noise < self.acdcConfig.max_iter_noise:
                idx_noise_pot = np.where(np.abs(np.diff(fit_data)) <= temp_noise_thr)[0]

                for i in range(0,len(idx_noise_pot)):
                    if idx_noise_pot[i] < idx_leading_edge:
                        idx_noise.append(idx_noise_pot[i])

                temp_noise_thr *= 1.5
                iter_noise += 1

            if iter_noise < self.acdcConfig.max_iter_noise:
                ThN = np.mean(fit_data[idx_noise])
            else:
                ThN = np.amin(fit_data)
        #--------------------- Using the same noise window for all surfaces -------
        elif self.acdcConfig.Thn_flag and not self.acdcConfig.fit_noise:
            ThN = np.mean(fit_data[self.acdcConfig.Thn_w_first:self.acdcConfig.Thn_w_first+self.acdcConfig.Thn_w_width-1])
        else:
            ThN = 0.0

        ## ------------------------ FITTING - --------------------------------------
        # -------------------------------------------------------------------------
        # DEFINE FITTING MODEL & CALL FITTING ROUTINE

        # -------------------------------------------------------------------------
        # -------------------------------------------------------------
        # --------- DEFINE FITTING FUNCTION MODEL ---------------------
        # -------------------------------------------------------------

        mpfun     =   lambda params, x, y: np.sum((self.sl_f0_model(params, x, ThN, func_f0) - y)**2)

        if len(self.acdcConfig.fitting_options_ACDC_lb) != 0:
            lb = self.acdcConfig.fitting_options_ACDC_lb
        else:
            lb = [np.NINF for x in range(0,3)]
        if len(self.acdcConfig.fitting_options_ACDC_ub) != 0:
            ub = self.acdcConfig.fitting_options_ACDC_ub
        else:
            ub = [np.Inf for x in range(len(lb))]


        # run
        resultFitting = spo.least_squares(mpfun, args=(k, fit_data), x0=fit_params_ini, bounds=(lb, ub)) #Algorithm = 'trf'

        estimates = resultFitting.x
        fittingFlag = resultFitting.status

        # --------- DEFINE THE OUTPUT PARAMETERS - --------------------------------
        # -------------------------------------------------------------------------
        # ----------- computation of the correlation coefficient - ----------------
        ml_wav = self.sl_f0_model(estimates, k, ThN, func_f0)

        correlation_fit = np.corrcoef(fit_data, ml_wav)

        # estimates[0]: refers to the error in epoch estimation
        # estimates[1]: significant waveheight to be extracted from gl estimated
        estimates[1] = 4 * np.sqrt(nf_p.Lz ** 2 / (2 * nf_p.alphag_a * nf_p.alphag_r) *
                                (2 * nf_p.alphag_a * nf_p.alphag_r / (estimates[1] ** 2)
                                 - nf_p.alphag_a - nf_p.alphag_r * 4 * (nf_p.Lx / nf_p.Ly) **
                                 4 * look_index_ref ** 2))

        estimates[2] = 10 * np.log10(estimates[2] * max_waveform)  # dB
        estimates = np.append(estimates, correlation_fit[0, 1] * 100)

        # fitting flag
        estimates = np.append(estimates, fittingFlag)

        return estimates, ml_wav