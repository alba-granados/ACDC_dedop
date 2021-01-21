import numpy as np

from dedop.conf import CharacterisationFile, ConstantsFile, ConfigurationFile, ACDCConfiguration
from ..base_algorithm import BaseAlgorithm

class AmplitudeCompensationAlgorithm(BaseAlgorithm):

    def __init__(self, chd: CharacterisationFile, cst: ConstantsFile,
                 cnf: ConfigurationFile, acdcCnf: ACDCConfiguration):
        super().__init__(chd, cst, cnf)

        self.acdcConfig = acdcCnf

    def __call__(self, stack, looks, range_index, nf_p, SWH, epoch):

        # ------------------- VARIABLES INITIALIZATION - --------------------------
        # ------------------ matrix notation of look and range indexes - ------------
        l = np.outer(looks, np.ones((1, len(range_index))))
        x = np.outer(np.ones((nf_p.Neff,1)), range_index)

        # ------------------ MSS initialization - -----------------------------------
        rou = self.acdcConfig.ini_rou

        # ------------dilation term - ------------------------------------------------
        sigmaz = SWH / 4.0
        g = np.sqrt(2 * nf_p.alphag_a * nf_p.alphag_r / (nf_p.alphag_a + nf_p.alphag_r * 4 *
                                                         (nf_p.Lx / nf_p.Ly) ** 4 * l ** 2 + 2 *
                                                         nf_p.alphag_a * nf_p.alphag_r * (sigmaz / nf_p.Lz) ** 2))

        # --------------Variables ----------------------------------------------------
        k = (x - epoch)
        xl = nf_p.Lx * l
        alpha_sigma = 1 / (nf_p.h ** 2 * rou)
        yk = nf_p.Ly * np.sqrt(np.abs(k))

        yk = np.where(k < 0, 0, yk)

        # --------- COMPUTATION OF THE ANTENNA / SURFACE -----------------------------
        # --------- Constant Term - --------------------------------------------------
        Bkl = 2.0 * np.exp(-nf_p.alphax * (xl - nf_p.xp) ** 2 - alpha_sigma * xl ** 2 - nf_p.alphay * nf_p.yp ** 2 -
                           (nf_p.alphay + alpha_sigma) * (yk ** 2) * np.cosh(2 * nf_p.alphay * nf_p.yp * yk))

        # -------------- COMPENSATION OF BKL AND FUNF0 - --------------------------
        stack_ac = stack / (np.sqrt(g) * Bkl)

        return stack_ac, k, l, g