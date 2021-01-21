import unittest
import os
import numpy as np

from dedop.proc.sar.acdc.fit_sl_f0_model import FitSlF0ModelAlgorithm
from dedop.conf import CharacterisationFile, ConstantsFile, ConfigurationFile, ACDCConfiguration
from dedop.util.unittest_helper import UnitTestHelper
from dedop.conf.enums import RangeIndexMethod
from tests.testing import TestDataLoader

class testFitSlF0ModelACDC(unittest.TestCase):

    def test_fit_sl_f0_model_ACDC01(self):
        # Initialisation
        testHelper = UnitTestHelper()
        fileDir = os.path.dirname(os.path.realpath('__file__'))

        # Input file
        fit_data = TestDataLoader(os.path.join(fileDir, 'test_data/acdc/test_fit_model/test_fit01/inputs/fit_data01.txt'), delim=' ')
        nf_p = testHelper.readNFP(os.path.join(fileDir, 'test_data/acdc/test_fit_model/test_fit01/inputs/nf_p_data.txt'))
        rangeIndexMethod = RangeIndexMethod(fit_data["range_index_method"])

        # Cnf, Chd, Cst files
        cst = ConstantsFile()
        chd = CharacterisationFile(cst,
                                   uso_freq_nom_chd = fit_data["uso_freq_nom_chd"],
                                   alt_freq_multiplier_chd = fit_data["alt_freq_multiplier_chd"],
                                   bw_ku_chd = fit_data["bw_ku_chd"])

        cnf = ConfigurationFile(zp_fact_range_cnf = fit_data["zp_fact_range_cnf"])

        acdcConfig = ACDCConfiguration(Thn_flag = fit_data["Thn_flag"],
                                       fit_noise = fit_data["fit_noise"],
                                       Thn_w_first = fit_data["Thn_w_first"],
                                       Thn_w_width = fit_data["Thn_w_width"],
                                       percent_leading_edge = fit_data["percent_leading_edge"],
                                       threshold_noise = fit_data["threshold_noise"],
                                       max_iter_noise = fit_data["max_iter_noise"],
                                       fitting_options_ACDC_lb = fit_data["fitting_options_ACDC_lb"],
                                       fitting_options_ACDC_ub = fit_data["fitting_options_ACDC_ub"],
                                       LUT_ximin = fit_data["LUT_ximin"],
                                       LUT_ximax = fit_data["LUT_ximax"],
                                       LUT_step = fit_data["LUT_step"],
                                       range_index_method = rangeIndexMethod)

        # Algorithm initialisation
        fitSlF0ModelACDCAlg = FitSlF0ModelAlgorithm(chd,cst,cnf,acdcConfig)

        # Input arrays
        k = testHelper.readArray1D(os.path.join(fileDir, 'test_data/acdc/test_fit_model/test_fit01/inputs/k_model.dat'))
        waveform = testHelper.readArray1D(os.path.join(fileDir, 'test_data/acdc/test_fit_model/test_fit01/inputs/waveform.dat'))

        # LUT in binary format
        f = open(os.path.join(fileDir, 'test_data/acdc/test_fit_model/test_fit01/inputs/lut_binary.dat'), 'rb')
        func_f0 = np.fromfile(f, np.double)
        f.close()

        # Expected output
        ml_wav_expected = testHelper.readArray1D(os.path.join(fileDir, 'test_data/acdc/test_fit_model/test_fit01/expected/ml_wav.dat'))

        # Code
        estimates, ml_wav = fitSlF0ModelACDCAlg(waveform, k, nf_p, fit_data["fit_params_ini"], fit_data["look_index_ref"], func_f0)

        # Tests
        self.assertTrue(testHelper.assertTestArray1D(ml_wav, ml_wav_expected, fit_data["errWave"]))

        self.assertTrue(testHelper.assertTestDouble(estimates[0], fit_data["estimates_expected"][0], fit_data["errEstimates"]))
        self.assertTrue(testHelper.assertTestDouble(estimates[1], fit_data["estimates_expected"][1], fit_data["errEstimates"]))
        self.assertTrue(testHelper.assertTestDouble(estimates[2], fit_data["estimates_expected"][2], fit_data["errEstimates"]))
        self.assertTrue(testHelper.assertTestDouble(estimates[3], fit_data["estimates_expected"][3], fit_data["errEstimates"]))
        #self.assertTrue(testHelper.assertTestDouble(estimates[4], fit_data["estimates_expected"][4], fit_data["errEstimates"])) #Fitting flag

    def test_fit_sl_f0_model_ACDC02(self):
        # Initialisation
        testHelper = UnitTestHelper()
        fileDir = os.path.dirname(os.path.realpath('__file__'))

        # Input file
        fit_data = TestDataLoader(os.path.join(fileDir, 'test_data/acdc/test_fit_model/test_fit02/inputs/fit_data02.txt'), delim=' ')
        nf_p = testHelper.readNFP(os.path.join(fileDir, 'test_data/acdc/test_fit_model/test_fit02/inputs/nf_p_data.txt'))
        rangeIndexMethod = RangeIndexMethod(fit_data["range_index_method"])

        # Cnf, Chd, Cst files
        cst = ConstantsFile()
        chd = CharacterisationFile(cst,
                                   uso_freq_nom_chd = fit_data["uso_freq_nom_chd"],
                                   alt_freq_multiplier_chd = fit_data["alt_freq_multiplier_chd"],
                                   bw_ku_chd = fit_data["bw_ku_chd"])

        cnf = ConfigurationFile(zp_fact_range_cnf = fit_data["zp_fact_range_cnf"])

        acdcConfig = ACDCConfiguration(Thn_flag = fit_data["Thn_flag"],
                                       fit_noise = fit_data["fit_noise"],
                                       Thn_w_first = fit_data["Thn_w_first"],
                                       Thn_w_width = fit_data["Thn_w_width"],
                                       percent_leading_edge = fit_data["percent_leading_edge"],
                                       threshold_noise = fit_data["threshold_noise"],
                                       max_iter_noise = fit_data["max_iter_noise"],
                                       fitting_options_ACDC_lb = fit_data["fitting_options_ACDC_lb"],
                                       fitting_options_ACDC_ub = fit_data["fitting_options_ACDC_ub"],
                                       LUT_ximin = fit_data["LUT_ximin"],
                                       LUT_ximax = fit_data["LUT_ximax"],
                                       LUT_step = fit_data["LUT_step"],
                                       range_index_method = rangeIndexMethod)

        # Algorithm initialisation
        fitSlF0ModelACDCAlg = FitSlF0ModelAlgorithm(chd,cst,cnf,acdcConfig)

        # Input arrays
        k = testHelper.readArray1D(os.path.join(fileDir, 'test_data/acdc/test_fit_model/test_fit02/inputs/k_model.dat'))
        waveform = testHelper.readArray1D(os.path.join(fileDir, 'test_data/acdc/test_fit_model/test_fit02/inputs/waveform.dat'))

        # LUT in binary format
        f = open(os.path.join(fileDir, 'test_data/acdc/test_fit_model/test_fit02/inputs/lut_binary.dat'), 'rb')
        func_f0 = np.fromfile(f, np.double)
        f.close()

        # Expected output
        ml_wav_expected = testHelper.readArray1D(os.path.join(fileDir, 'test_data/acdc/test_fit_model/test_fit02/expected/ml_wav.dat'))

        # Code
        estimates, ml_wav = fitSlF0ModelACDCAlg(waveform, k, nf_p, fit_data["fit_params_ini"], fit_data["look_index_ref"], func_f0)

        # Tests
        self.assertTrue(testHelper.assertTestArray1D(ml_wav, ml_wav_expected, fit_data["errWave"]))

        self.assertTrue(testHelper.assertTestDouble(estimates[0], fit_data["estimates_expected"][0], fit_data["errEstimates"]))
        self.assertTrue(testHelper.assertTestDouble(estimates[1], fit_data["estimates_expected"][1], fit_data["errEstimates"]))
        self.assertTrue(testHelper.assertTestDouble(estimates[2], fit_data["estimates_expected"][2], fit_data["errEstimates"]))
        self.assertTrue(testHelper.assertTestDouble(estimates[3], fit_data["estimates_expected"][3], fit_data["errEstimates"]))
        #self.assertTrue(testHelper.assertTestDouble(estimates[4], fit_data["estimates_expected"][4], fit_data["errEstimates"])) #Fitting flag

    def test_fit_sl_f0_model_ACDC03(self):
        # Initialisation
        testHelper = UnitTestHelper()
        fileDir = os.path.dirname(os.path.realpath('__file__'))

        # Input file
        fit_data = TestDataLoader(os.path.join(fileDir, 'test_data/acdc/test_fit_model/test_fit03/inputs/fit_data03.txt'), delim=' ')
        nf_p = testHelper.readNFP(os.path.join(fileDir, 'test_data/acdc/test_fit_model/test_fit03/inputs/nf_p_data.txt'))
        rangeIndexMethod = RangeIndexMethod(fit_data["range_index_method"])

        # Cnf, Chd, Cst files
        cst = ConstantsFile()
        chd = CharacterisationFile(cst,
                                   uso_freq_nom_chd = fit_data["uso_freq_nom_chd"],
                                   alt_freq_multiplier_chd = fit_data["alt_freq_multiplier_chd"],
                                   bw_ku_chd = fit_data["bw_ku_chd"])

        cnf = ConfigurationFile(zp_fact_range_cnf = fit_data["zp_fact_range_cnf"])

        acdcConfig = ACDCConfiguration(Thn_flag = fit_data["Thn_flag"],
                                       fit_noise = fit_data["fit_noise"],
                                       Thn_w_first = fit_data["Thn_w_first"],
                                       Thn_w_width = fit_data["Thn_w_width"],
                                       percent_leading_edge = fit_data["percent_leading_edge"],
                                       threshold_noise = fit_data["threshold_noise"],
                                       max_iter_noise = fit_data["max_iter_noise"],
                                       fitting_options_ACDC_lb = fit_data["fitting_options_ACDC_lb"],
                                       fitting_options_ACDC_ub = fit_data["fitting_options_ACDC_ub"],
                                       LUT_ximin = fit_data["LUT_ximin"],
                                       LUT_ximax = fit_data["LUT_ximax"],
                                       LUT_step = fit_data["LUT_step"],
                                       range_index_method = rangeIndexMethod)

        # Algorithm initialisation
        fitSlF0ModelACDCAlg = FitSlF0ModelAlgorithm(chd,cst,cnf,acdcConfig)

        # Input arrays
        k = testHelper.readArray1D(os.path.join(fileDir, 'test_data/acdc/test_fit_model/test_fit03/inputs/k_model.dat'))
        waveform = testHelper.readArray1D(os.path.join(fileDir, 'test_data/acdc/test_fit_model/test_fit03/inputs/waveform.dat'))

        # LUT in binary format
        f = open(os.path.join(fileDir, 'test_data/acdc/test_fit_model/test_fit03/inputs/lut_binary.dat'), 'rb')
        func_f0 = np.fromfile(f, np.double)
        f.close()

        # Expected output
        ml_wav_expected = testHelper.readArray1D(os.path.join(fileDir, 'test_data/acdc/test_fit_model/test_fit03/expected/ml_wav.dat'))

        # Code
        estimates, ml_wav = fitSlF0ModelACDCAlg(waveform, k, nf_p, fit_data["fit_params_ini"], fit_data["look_index_ref"], func_f0)

        # Tests
        self.assertTrue(testHelper.assertTestArray1D(ml_wav, ml_wav_expected, fit_data["errWave"]))

        self.assertTrue(testHelper.assertTestDouble(estimates[0], fit_data["estimates_expected"][0], fit_data["errEstimates"]))
        self.assertTrue(testHelper.assertTestDouble(estimates[1], fit_data["estimates_expected"][1], fit_data["errEstimates"]))
        self.assertTrue(testHelper.assertTestDouble(estimates[2], fit_data["estimates_expected"][2], fit_data["errEstimates"]))
        self.assertTrue(testHelper.assertTestDouble(estimates[3], fit_data["estimates_expected"][3], fit_data["errEstimates"]))
        #self.assertTrue(testHelper.assertTestDouble(estimates[4], fit_data["estimates_expected"][4], fit_data["errEstimates"])) #Fitting flag

if __name__ == '__main__':
    #import matplotlib.pyplot as plt
    unittest.main()