import unittest
import os
import numpy as np

from dedop.proc.sar.acdc.retracking import RetrackingAlgorithm
from dedop.conf import CharacterisationFile, ConstantsFile, ConfigurationFile, ACDCConfiguration
from dedop.util.unittest_helper import UnitTestHelper
from dedop.conf.enums import RangeIndexMethod
from tests.testing import TestDataLoader

class testRetrackingACDC(unittest.TestCase):

    def test_retracking_ACDC01(self):
        # Initialisation
        testHelper = UnitTestHelper()
        fileDir = os.path.dirname(os.path.realpath('__file__'))

        # Input file
        retracking_data = TestDataLoader(os.path.join(fileDir, 'test_data/acdc/test_retracking/test_retracking01/inputs/retracking_data01.txt'), delim=' ')
        nf_p = testHelper.readNFP(os.path.join(fileDir, 'test_data/acdc/test_retracking/test_retracking01/inputs/nf_p_data.txt'))
        rangeIndexMethod = RangeIndexMethod(retracking_data["range_index_method"])

        # Cnf, Chd, Cst files
        cst = ConstantsFile()
        chd = CharacterisationFile(cst,
                                   N_samples_sar_chd = retracking_data["N_samples_sar_chd"],
                                   uso_freq_nom_chd = retracking_data["uso_freq_nom_chd"],
                                   alt_freq_multiplier_chd = retracking_data["alt_freq_multiplier_chd"],
                                   bw_ku_chd = retracking_data["bw_ku_chd"])

        cnf = ConfigurationFile(zp_fact_range_cnf = retracking_data["zp_fact_range_cnf"])

        acdcConfig = ACDCConfiguration(weighting_win_type = retracking_data["weighting_win_type"],
                                       weighting_win_width = retracking_data["weighting_win_width"],
                                       wvfm_discard_samples = retracking_data["wvfm_discard_samples"],
                                       wvfm_discard_samples_begin = retracking_data["wvfm_discard_samples_begin"],
                                       wvfm_discard_samples_end = retracking_data["wvfm_discard_samples_end"],
                                       Thn_flag = retracking_data["Thn_flag"],
                                       fit_noise = retracking_data["fit_noise"],
                                       Thn_w_first = retracking_data["Thn_w_first"],
                                       Thn_w_width = retracking_data["Thn_w_width"],
                                       percent_leading_edge = retracking_data["percent_leading_edge"],
                                       threshold_noise = retracking_data["threshold_noise"],
                                       max_iter_noise = retracking_data["max_iter_noise"],
                                       fitting_options_ACDC_lb = retracking_data["fitting_options_ACDC_lb"],
                                       fitting_options_ACDC_ub = retracking_data["fitting_options_ACDC_ub"],
                                       LUT_ximin = retracking_data["LUT_ximin"],
                                       LUT_ximax = retracking_data["LUT_ximax"],
                                       LUT_step = retracking_data["LUT_step"],
                                       range_index_method = rangeIndexMethod)

        # Algorithm initialisation
        retrackingACDCAlg = RetrackingAlgorithm(chd,cst,cnf,acdcConfig)

        # Input arrays
        stack_ac = testHelper.readArray2D(os.path.join(fileDir, 'test_data/acdc/test_retracking/test_retracking01/inputs/stack_ac.dat'), (265,256))
        k_scaled = testHelper.readArray2D(os.path.join(fileDir, 'test_data/acdc/test_retracking/test_retracking01/inputs/k_scaled.dat'), (265,256))
        mask = testHelper.readArray2D(os.path.join(fileDir, 'test_data/acdc/test_retracking/test_retracking01/inputs/mask.dat'), (265,256))

        # LUT in binary format
        f = open(os.path.join(fileDir, 'test_data/acdc/test_retracking/test_retracking01/inputs/lut_binary.dat'), 'rb')
        func_f0 = np.fromfile(f, np.double)
        f.close()

        # Expected output
        waveform_ml_ACDC_expected = testHelper.readArray1D(os.path.join(fileDir, 'test_data/acdc/test_retracking/test_retracking01/expected/waveform_ml_ACDC_retracking.dat'))
        k_ml_ACDC_expected = testHelper.readArray1D(os.path.join(fileDir, 'test_data/acdc/test_retracking/test_retracking01/expected/k_ml_ACDC.dat'))
        ml_wav_fitted_expected = testHelper.readArray1D(os.path.join(fileDir, 'test_data/acdc/test_retracking/test_retracking01/expected/ml_wav_fitted.dat'))

        # Code
        waveform_ml_ACDC,k_ml_ACDC,estimates,flag_exit,ml_wav_fitted,start_sample,stop_sample = retrackingACDCAlg(stack_ac, k_scaled, nf_p, retracking_data["fit_params_ini"], retracking_data["look_index_ref"], func_f0, mask)

        # Tests
        self.assertEqual(flag_exit, 0)
        self.assertEqual(start_sample, retracking_data["start_sample"])
        self.assertEqual(stop_sample, retracking_data["stop_sample"])

        self.assertTrue(testHelper.assertTestArray1D(waveform_ml_ACDC, waveform_ml_ACDC_expected, retracking_data["errWave"]))
        self.assertTrue(testHelper.assertTestArray1D(k_ml_ACDC, k_ml_ACDC_expected, retracking_data["errWave"]))
        self.assertTrue(testHelper.assertTestArray1D(ml_wav_fitted, ml_wav_fitted_expected, retracking_data["errWaveFitted"]))

        self.assertTrue(testHelper.assertTestDouble(estimates[0], retracking_data["estimates_expected"][0], retracking_data["errEstimates"]))
        self.assertTrue(testHelper.assertTestDouble(estimates[1], retracking_data["estimates_expected"][1], retracking_data["errEstimates"]))
        self.assertTrue(testHelper.assertTestDouble(estimates[2], retracking_data["estimates_expected"][2], retracking_data["errEstimates"]))
        self.assertTrue(testHelper.assertTestDouble(estimates[3], retracking_data["estimates_expected"][3], retracking_data["errEstimates"]))
        #self.assertTrue(testHelper.assertTestDouble(estimates[4], retracking_data["estimates_expected"][4], retracking_data["errEstimates"])) #Fitting flag
        self.assertTrue(testHelper.assertTestDouble(estimates[5], retracking_data["estimates_expected"][5], retracking_data["errEstimates"]))

    def test_retracking_ACDC02(self):
        # Initialisation
        testHelper = UnitTestHelper()
        fileDir = os.path.dirname(os.path.realpath('__file__'))

        # Input file
        retracking_data = TestDataLoader(os.path.join(fileDir, 'test_data/acdc/test_retracking/test_retracking02/inputs/retracking_data02.txt'), delim=' ')
        nf_p = testHelper.readNFP(os.path.join(fileDir, 'test_data/acdc/test_retracking/test_retracking02/inputs/nf_p_data.txt'))
        rangeIndexMethod = RangeIndexMethod(retracking_data["range_index_method"])

        # Cnf, Chd, Cst files
        cst = ConstantsFile()
        chd = CharacterisationFile(cst,
                                   N_samples_sar_chd = retracking_data["N_samples_sar_chd"],
                                   uso_freq_nom_chd = retracking_data["uso_freq_nom_chd"],
                                   alt_freq_multiplier_chd = retracking_data["alt_freq_multiplier_chd"],
                                   bw_ku_chd = retracking_data["bw_ku_chd"])

        cnf = ConfigurationFile(zp_fact_range_cnf = retracking_data["zp_fact_range_cnf"])

        acdcConfig = ACDCConfiguration(weighting_win_type = retracking_data["weighting_win_type"],
                                       weighting_win_width = retracking_data["weighting_win_width"],
                                       wvfm_discard_samples = retracking_data["wvfm_discard_samples"],
                                       wvfm_discard_samples_begin = retracking_data["wvfm_discard_samples_begin"],
                                       wvfm_discard_samples_end = retracking_data["wvfm_discard_samples_end"],
                                       Thn_flag = retracking_data["Thn_flag"],
                                       fit_noise = retracking_data["fit_noise"],
                                       Thn_w_first = retracking_data["Thn_w_first"],
                                       Thn_w_width = retracking_data["Thn_w_width"],
                                       percent_leading_edge = retracking_data["percent_leading_edge"],
                                       threshold_noise = retracking_data["threshold_noise"],
                                       max_iter_noise = retracking_data["max_iter_noise"],
                                       fitting_options_ACDC_lb = retracking_data["fitting_options_ACDC_lb"],
                                       fitting_options_ACDC_ub = retracking_data["fitting_options_ACDC_ub"],
                                       LUT_ximin = retracking_data["LUT_ximin"],
                                       LUT_ximax = retracking_data["LUT_ximax"],
                                       LUT_step = retracking_data["LUT_step"],
                                       range_index_method = rangeIndexMethod)

        # Algorithm initialisation
        retrackingACDCAlg = RetrackingAlgorithm(chd,cst,cnf,acdcConfig)

        # Input arrays
        stack_ac = testHelper.readArray2D(os.path.join(fileDir, 'test_data/acdc/test_retracking/test_retracking02/inputs/stack_ac.dat'), (265,256))
        k_scaled = testHelper.readArray2D(os.path.join(fileDir, 'test_data/acdc/test_retracking/test_retracking02/inputs/k_scaled.dat'), (265,256))
        mask = testHelper.readArray2D(os.path.join(fileDir, 'test_data/acdc/test_retracking/test_retracking02/inputs/mask.dat'), (265,256))

        # LUT in binary format
        f = open(os.path.join(fileDir, 'test_data/acdc/test_retracking/test_retracking02/inputs/lut_binary.dat'), 'rb')
        func_f0 = np.fromfile(f, np.double)
        f.close()

        # Expected output
        waveform_ml_ACDC_expected = testHelper.readArray1D(os.path.join(fileDir, 'test_data/acdc/test_retracking/test_retracking02/expected/waveform_ml_ACDC_retracking.dat'))
        k_ml_ACDC_expected = testHelper.readArray1D(os.path.join(fileDir, 'test_data/acdc/test_retracking/test_retracking02/expected/k_ml_ACDC.dat'))
        ml_wav_fitted_expected = testHelper.readArray1D(os.path.join(fileDir, 'test_data/acdc/test_retracking/test_retracking02/expected/ml_wav_fitted.dat'))

        # Code
        waveform_ml_ACDC,k_ml_ACDC,estimates,flag_exit,ml_wav_fitted,start_sample,stop_sample = retrackingACDCAlg(stack_ac, k_scaled, nf_p, retracking_data["fit_params_ini"], retracking_data["look_index_ref"], func_f0, mask)

        # Tests
        self.assertEqual(flag_exit, 0)
        self.assertEqual(start_sample, retracking_data["start_sample"])
        self.assertEqual(stop_sample, retracking_data["stop_sample"])

        self.assertTrue(testHelper.assertTestArray1D(waveform_ml_ACDC, waveform_ml_ACDC_expected, retracking_data["errWave"]))
        self.assertTrue(testHelper.assertTestArray1D(k_ml_ACDC, k_ml_ACDC_expected, retracking_data["errWave"]))
        self.assertTrue(testHelper.assertTestArray1D(ml_wav_fitted, ml_wav_fitted_expected, retracking_data["errWaveFitted"]))

        self.assertTrue(testHelper.assertTestDouble(estimates[0], retracking_data["estimates_expected"][0], retracking_data["errEstimates"]))
        self.assertTrue(testHelper.assertTestDouble(estimates[1], retracking_data["estimates_expected"][1], retracking_data["errEstimates"]))
        self.assertTrue(testHelper.assertTestDouble(estimates[2], retracking_data["estimates_expected"][2], retracking_data["errEstimates"]))
        self.assertTrue(testHelper.assertTestDouble(estimates[3], retracking_data["estimates_expected"][3], retracking_data["errEstimates"]))
        #self.assertTrue(testHelper.assertTestDouble(estimates[4], retracking_data["estimates_expected"][4], retracking_data["errEstimates"])) #Fitting flag
        self.assertTrue(testHelper.assertTestDouble(estimates[5], retracking_data["estimates_expected"][5], retracking_data["errEstimates"]))


if __name__ == '__main__':
    unittest.main()