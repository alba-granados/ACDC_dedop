import numpy as np

from dedop.conf import CharacterisationFile, ConstantsFile, ConfigurationFile, ACDCConfiguration
from ..base_algorithm import BaseAlgorithm

class DilationCompensationAlgorithm(BaseAlgorithm):

    def __init__(self, chd: CharacterisationFile, cst: ConstantsFile,
                 cnf: ConfigurationFile, acdcCnf: ACDCConfiguration):
        super().__init__(chd, cst, cnf)

        self.acdcConfig = acdcCnf

    def __call__(self, k, g, nf_p, SWH, look_indexation_ref):
        # ------------Computation of g0 - -----------------------------------------
        sigmaz = SWH / 4.0
        l_0 = look_indexation_ref
        g_0 = np.sqrt(2 * nf_p.alphag_a * nf_p.alphag_r / (nf_p.alphag_a + nf_p.alphag_r * 4 *
                                                        (nf_p.Lx / nf_p.Ly) ** 4 * l_0 ** 2 + 2 *
                                                        nf_p.alphag_a * nf_p.alphag_r * (sigmaz / nf_p.Lz) ** 2))

        # ---------- Scaling of the range bin index - -----------------------------
        k_scaled = g * k / g_0

        return k_scaled