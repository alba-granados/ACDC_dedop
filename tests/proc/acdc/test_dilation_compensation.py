import unittest
import os

from dedop.proc.sar.acdc.dilation_compensation import DilationCompensationAlgorithm
from dedop.conf import CharacterisationFile, ConstantsFile, ConfigurationFile, ACDCConfiguration
from dedop.util.unittest_helper import UnitTestHelper
from tests.testing import TestDataLoader

class testDilationCompensation(unittest.TestCase):

    def test_dilationCompensation(self):
        # Initialisation
        testHelper = UnitTestHelper()
        fileDir = os.path.dirname(os.path.realpath('__file__'))

        # Input file
        dc_data = TestDataLoader(os.path.join(fileDir, 'test_data/acdc/test_dc/test_dc_01/inputs/dc_data.txt'), delim=' ')

        # Cnf, Chd, Cst files
        cst = ConstantsFile()
        chd = CharacterisationFile(cst)
        cnf = ConfigurationFile()
        acdcConfig = ACDCConfiguration()

        # Algorithm initialisation
        dilationCompensationAlg = DilationCompensationAlgorithm(chd,cst,cnf,acdcConfig)

        # Input arrays
        nf_p = testHelper.readNFP(os.path.join(fileDir, 'test_data/acdc/test_dc/test_dc_01/inputs/nf_p_data.txt'))
        k = testHelper.readArray2D(os.path.join(fileDir, 'test_data/acdc/test_dc/test_dc_01/inputs/k.dat'), (265,256))
        g = testHelper.readArray2D(os.path.join(fileDir, 'test_data/acdc/test_dc/test_dc_01/inputs/g.dat'), (265,256))

        # Expected output
        k_scaled_expected = testHelper.readArray2D(os.path.join(fileDir, 'test_data/acdc/test_dc/test_dc_01/expected/k_scaled.dat'), (265,256))

        # Code
        k_scaled = dilationCompensationAlg(k, g, nf_p, dc_data["SWH"], dc_data["look_indexation_ref"])

        # Tests
        self.assertTrue(testHelper.assertTestArray2D(k_scaled, k_scaled_expected, dc_data["err"]))

if __name__ == "__main__":
    unittest.main()
