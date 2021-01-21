import unittest
import os
import numpy as np

from dedop.proc.sar.acdc.sl_f0_model import SlF0ModelAlgorithm
from dedop.conf import CharacterisationFile, ConstantsFile, ConfigurationFile, ACDCConfiguration
from dedop.util.unittest_helper import UnitTestHelper
from dedop.conf.enums import RangeIndexMethod
from tests.testing import TestDataLoader

class testSlF0ModelACDC(unittest.TestCase):

    def test_sl_f0_model_ACDC01(self):
        # Initialisation
        testHelper = UnitTestHelper()
        fileDir = os.path.dirname(os.path.realpath('__file__'))

        # Input file
        model_data = TestDataLoader(os.path.join(fileDir, 'test_data/acdc/test_model/test_model01/inputs/model_data01.txt'), delim=' ')
        rangeIndexMethod = RangeIndexMethod(model_data["range_index_method"])

        # Cnf, Chd, Cst files
        cst = ConstantsFile()
        chd = CharacterisationFile(cst,
                                   uso_freq_nom_chd = model_data["uso_freq_nom_chd"],
                                   alt_freq_multiplier_chd = model_data["alt_freq_multiplier_chd"],
                                   bw_ku_chd = model_data["bw_ku_chd"])

        cnf = ConfigurationFile(zp_fact_range_cnf = model_data["zp_fact_range_cnf"])

        acdcConfig = ACDCConfiguration(LUT_ximin = model_data["LUT_ximin"],
                                       LUT_ximax = model_data["LUT_ximax"],
                                       LUT_step = model_data["LUT_step"],
                                       range_index_method = rangeIndexMethod)

        # Algorithm initialisation
        slF0ModelAlg = SlF0ModelAlgorithm(chd,cst,cnf,acdcConfig)

        # Input arrays
        k = testHelper.readArray1D(os.path.join(fileDir, 'test_data/acdc/test_model/test_model01/inputs/k_model.dat'))

        # LUT in binary format
        f = open(os.path.join(fileDir, 'test_data/acdc/test_model/test_model01/inputs/lut_binary.dat'), 'rb')
        func_f0 = np.fromfile(f, np.double)
        f.close()

        # Expected output
        waveform_ml_ACDC_expected = testHelper.readArray1D(os.path.join(fileDir, 'test_data/acdc/test_model/test_model01/expected/waveform_ml_ACDC_model.dat'))

        # Code
        waveform_ml_ACDC = slF0ModelAlg(model_data["fit_params"], k, model_data["ThN"], func_f0)

        # Tests
        self.assertTrue(testHelper.assertTestArray1D(waveform_ml_ACDC, waveform_ml_ACDC_expected, model_data["err"]))

    def test_sl_f0_model_ACDC02(self):
        # Initialisation
        testHelper = UnitTestHelper()
        fileDir = os.path.dirname(os.path.realpath('__file__'))

        # Input file
        model_data = TestDataLoader(os.path.join(fileDir, 'test_data/acdc/test_model/test_model02/inputs/model_data02.txt'), delim=' ')
        rangeIndexMethod = RangeIndexMethod(model_data["range_index_method"])

        # Cnf, Chd, Cst files
        cst = ConstantsFile()
        chd = CharacterisationFile(cst,
                                   uso_freq_nom_chd = model_data["uso_freq_nom_chd"],
                                   alt_freq_multiplier_chd = model_data["alt_freq_multiplier_chd"],
                                   bw_ku_chd = model_data["bw_ku_chd"])

        cnf = ConfigurationFile(zp_fact_range_cnf = model_data["zp_fact_range_cnf"])

        acdcConfig = ACDCConfiguration(LUT_ximin = model_data["LUT_ximin"],
                                       LUT_ximax = model_data["LUT_ximax"],
                                       LUT_step = model_data["LUT_step"],
                                       range_index_method = rangeIndexMethod)

        # Algorithm initialisation
        slF0ModelAlg = SlF0ModelAlgorithm(chd,cst,cnf,acdcConfig)

        # Input
        k = testHelper.readArray1D(os.path.join(fileDir, 'test_data/acdc/test_model/test_model02/inputs/k_model.dat'))

        # LUT in binary format
        f = open(os.path.join(fileDir, 'test_data/acdc/test_model/test_model02/inputs/lut_binary.dat'), 'rb')
        func_f0 = np.fromfile(f, np.double)
        f.close()

        # Expected output
        waveform_ml_ACDC_expected = testHelper.readArray1D(os.path.join(fileDir, 'test_data/acdc/test_model/test_model02/expected/waveform_ml_ACDC_model.dat'))

        # Code
        waveform_ml_ACDC = slF0ModelAlg(model_data["fit_params"], k, model_data["ThN"], func_f0)

        # Tests
        self.assertTrue(testHelper.assertTestArray1D(waveform_ml_ACDC, waveform_ml_ACDC_expected, model_data["err"]))

    def test_sl_f0_model_ACDC03(self):
        # Initialisation
        testHelper = UnitTestHelper()
        fileDir = os.path.dirname(os.path.realpath('__file__'))

        # Input file
        model_data = TestDataLoader(os.path.join(fileDir, 'test_data/acdc/test_model/test_model03/inputs/model_data03.txt'), delim=' ')
        rangeIndexMethod = RangeIndexMethod(model_data["range_index_method"])

        # Cnf, Chd, Cst files
        cst = ConstantsFile()
        chd = CharacterisationFile(cst,
                                   uso_freq_nom_chd = model_data["uso_freq_nom_chd"],
                                   alt_freq_multiplier_chd = model_data["alt_freq_multiplier_chd"],
                                   bw_ku_chd = model_data["bw_ku_chd"])

        cnf = ConfigurationFile(zp_fact_range_cnf = model_data["zp_fact_range_cnf"])

        acdcConfig = ACDCConfiguration(LUT_ximin = model_data["LUT_ximin"],
                                       LUT_ximax = model_data["LUT_ximax"],
                                       LUT_step = model_data["LUT_step"],
                                       range_index_method = rangeIndexMethod)

        # Algorithm initialisation
        slF0ModelAlg = SlF0ModelAlgorithm(chd,cst,cnf,acdcConfig)

        # Input
        k = testHelper.readArray1D(os.path.join(fileDir, 'test_data/acdc/test_model/test_model03/inputs/k_model.dat'))

        # LUT in binary format
        f = open(os.path.join(fileDir, 'test_data/acdc/test_model/test_model03/inputs/lut_binary.dat'), 'rb')
        func_f0 = np.fromfile(f, np.double)
        f.close()

        # Expected output
        waveform_ml_ACDC_expected = testHelper.readArray1D(os.path.join(fileDir, 'test_data/acdc/test_model/test_model03/expected/waveform_ml_ACDC_model.dat'))

        # Code
        waveform_ml_ACDC = slF0ModelAlg(model_data["fit_params"], k, model_data["ThN"], func_f0)

        # Tests
        self.assertTrue(testHelper.assertTestArray1D(waveform_ml_ACDC, waveform_ml_ACDC_expected, model_data["err"]))

    def test_sl_f0_model_ACDC04(self):
        # Initialisation
        testHelper = UnitTestHelper()
        fileDir = os.path.dirname(os.path.realpath('__file__'))

        # Input file
        model_data = TestDataLoader(os.path.join(fileDir, 'test_data/acdc/test_model/test_model04/inputs/model_data04.txt'), delim=' ')
        rangeIndexMethod = RangeIndexMethod(model_data["range_index_method"])

        # Cnf, Chd, Cst files
        cst = ConstantsFile()
        chd = CharacterisationFile(cst,
                                   uso_freq_nom_chd = model_data["uso_freq_nom_chd"],
                                   alt_freq_multiplier_chd = model_data["alt_freq_multiplier_chd"],
                                   bw_ku_chd = model_data["bw_ku_chd"])

        cnf = ConfigurationFile(zp_fact_range_cnf = model_data["zp_fact_range_cnf"])

        acdcConfig = ACDCConfiguration(LUT_ximin = model_data["LUT_ximin"],
                                       LUT_ximax = model_data["LUT_ximax"],
                                       LUT_step = model_data["LUT_step"],
                                       range_index_method = rangeIndexMethod)

        # Algorithm initialisation
        slF0ModelAlg = SlF0ModelAlgorithm(chd,cst,cnf,acdcConfig)

        # Input
        k = testHelper.readArray1D(os.path.join(fileDir, 'test_data/acdc/test_model/test_model04/inputs/k_model.dat'))

        # LUT in binary format
        f = open(os.path.join(fileDir, 'test_data/acdc/test_model/test_model04/inputs/lut_binary.dat'), 'rb')
        func_f0 = np.fromfile(f, np.double)
        f.close()

        # Expected output
        waveform_ml_ACDC_expected = testHelper.readArray1D(os.path.join(fileDir, 'test_data/acdc/test_model/test_model04/expected/waveform_ml_ACDC_model.dat'))

        # Code
        waveform_ml_ACDC = slF0ModelAlg(model_data["fit_params"], k, model_data["ThN"], func_f0)

        # Tests
        self.assertTrue(testHelper.assertTestArray1D(waveform_ml_ACDC, waveform_ml_ACDC_expected, model_data["err"]))

if __name__ == '__main__':
    unittest.main()