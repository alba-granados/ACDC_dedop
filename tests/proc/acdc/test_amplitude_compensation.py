import unittest
import os

from dedop.proc.sar.acdc.amplitude_compensation import AmplitudeCompensationAlgorithm
from dedop.conf import CharacterisationFile, ConstantsFile, ConfigurationFile, ACDCConfiguration
from dedop.util.unittest_helper import UnitTestHelper
from tests.testing import TestDataLoader

class testAmplitudeCompensation(unittest.TestCase):

    def test_amplitudeCompensation(self):
        # Initialisation
        testHelper = UnitTestHelper()
        fileDir = os.path.dirname(os.path.realpath('__file__'))

        # Input file
        ac_data = TestDataLoader(os.path.join(fileDir, 'test_data/acdc/test_ac/test_ac_01/inputs/ac_data.txt'), delim=' ')

        # Cnf, Chd, Cst files
        cst = ConstantsFile()
        chd = CharacterisationFile(cst)
        cnf = ConfigurationFile()
        acdcConfig = ACDCConfiguration(ini_rou = ac_data["ini_rou"])

        # Algorithm initialisation
        amplitudeCompensationAlg = AmplitudeCompensationAlgorithm(chd,cst,cnf,acdcConfig)

        # Input arrays
        nf_p = testHelper.readNFP(os.path.join(fileDir, 'test_data/acdc/test_ac/test_ac_01/inputs/nf_p_data.txt'))
        stack = testHelper.readArray2D(os.path.join(fileDir, 'test_data/acdc/test_ac/test_ac_01/inputs/stack.dat'), (265,256))

        # Expected output
        stack_ac_expected = testHelper.readArray2D(os.path.join(fileDir, 'test_data/acdc/test_ac/test_ac_01/expected/stack_ac.dat'), (265,256))
        k_expected = testHelper.readArray2D(os.path.join(fileDir, 'test_data/acdc/test_ac/test_ac_01/expected/k.dat'), (265,256))
        l_expected = testHelper.readArray2D(os.path.join(fileDir, 'test_data/acdc/test_ac/test_ac_01/expected/l.dat'), (265,256))
        g_expected = testHelper.readArray2D(os.path.join(fileDir, 'test_data/acdc/test_ac/test_ac_01/expected/g.dat'), (265,256))

        # Code
        stack_ac, k, l, g = amplitudeCompensationAlg(stack, ac_data["looks"], ac_data["range_index"], nf_p, ac_data["SWH"], ac_data["epoch"])

        # Tests
        self.assertTrue(testHelper.assertTestArray2D(stack_ac, stack_ac_expected, ac_data["err"]))
        self.assertTrue(testHelper.assertTestArray2D(k, k_expected, ac_data["err"]))
        self.assertTrue(testHelper.assertTestArray2D(l, l_expected, ac_data["err"]))
        self.assertTrue(testHelper.assertTestArray2D(g, g_expected, ac_data["err"]))

if __name__ == "__main__":
    unittest.main()