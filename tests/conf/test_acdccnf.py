import unittest
import os

from dedop.conf import ACDCConfiguration
from dedop.conf.enums import RangeIndexMethod, AzimuthWindowingMethod
from tests.testing import TestDataLoader


class TestACDCCNF(unittest.TestCase):
    _root = os.path.join(os.path.dirname(__file__), '..', '..')
    _folder = os.path.join(_root, "test_data", "conf", "test_acdccnf")

    _expected_file = os.path.join(
            _folder, "expected.txt"
    )
    _input_file = os.path.join(
            _folder, "acdccnf.json"
    )

    def setUp(self):
        self.expected = TestDataLoader(self._expected_file, delim=' ')
        self.actual = ACDCConfiguration(self._input_file)

    def test_num_iterations(self):
        expected = self.expected["num_iterations"]
        actual = self.actual.num_iterations

        self.assertEqual(expected, actual)

    def test_n_iterations_track(self):
        expected = self.expected["n_iterations_track"]
        actual = self.actual.n_iterations_track

        self.assertEqual(expected, actual)

    def test_wvfm_discard_samples(self):
        expected = self.expected["wvfm_discard_samples"]
        actual = self.actual.wvfm_discard_samples

        self.assertEqual(expected, actual)

    def test_wvfm_discard_samples_begin(self):
        expected = self.expected["wvfm_discard_samples_begin"]
        actual = self.actual.wvfm_discard_samples_begin

        self.assertEqual(expected, actual)

    def test_wvfm_discard_samples_end(self):
        expected = self.expected["wvfm_discard_samples_end"]
        actual = self.actual.wvfm_discard_samples_end

        self.assertEqual(expected, actual)

    def test_weighting_win_type(self):
        expected = self.expected["weighting_win_type"]
        actual = self.actual.weighting_win_type

        self.assertEqual(expected, actual)

    def test_weighting_win_width(self):
        expected = self.expected["weighting_win_width"]
        actual = self.actual.weighting_win_width

        self.assertEqual(expected, actual)

    def test_Thn_flag(self):
        expected = self.expected["Thn_flag"]
        actual = self.actual.Thn_flag

        self.assertEqual(expected, actual)

    def test_fit_noise(self):
        expected = self.expected["fit_noise"]
        actual = self.actual.fit_noise

        self.assertEqual(expected, actual)

    def test_Thn_w_first(self):
        expected = self.expected["Thn_w_first"]
        actual = self.actual.Thn_w_first

        self.assertEqual(expected, actual)

    def test_Thn_w_width(self):
        expected = self.expected["Thn_w_width"]
        actual = self.actual.Thn_w_width

        self.assertEqual(expected, actual)

    def test_threshold_noise(self):
        expected = self.expected["threshold_noise"]
        actual = self.actual.threshold_noise

        self.assertEqual(expected, actual)

    def test_max_iter_noise(self):
        expected = self.expected["max_iter_noise"]
        actual = self.actual.max_iter_noise

        self.assertEqual(expected, actual)

    def test_rou_flag(self):
        expected = self.expected["rou_flag"]
        actual = self.actual.rou_flag

        self.assertEqual(expected, actual)

    def test_rou(self):
        expected = self.expected["rou"]
        actual = self.actual.rou

        self.assertEqual(expected, actual)

    def test_Hs(self):
        expected = self.expected["Hs"]
        actual = self.actual.Hs

        self.assertEqual(expected, actual)

    def test_window_type_a(self):
        expected = AzimuthWindowingMethod(self.expected["window_type_a"])
        actual = self.actual.window_type_a

        self.assertEqual(expected, actual)

    def test_window_a_fixed_value(self):
        expected = self.expected["window_a_fixed_value"]
        actual = self.actual.window_a_fixed_value

        self.assertEqual(expected, actual)

    def test_window_type_r(self):
        expected = AzimuthWindowingMethod(self.expected["window_type_r"])
        actual = self.actual.window_type_r

        self.assertEqual(expected, actual)

    def test_window_r_fixed_value(self):
        expected = self.expected["window_r_fixed_value"]
        actual = self.actual.window_r_fixed_value

        self.assertEqual(expected, actual)

    def test_LUT_ximax(self):
        expected = self.expected["LUT_ximax"]
        actual = self.actual.LUT_ximax

        self.assertEqual(expected, actual)

    def test_LUT_ximin(self):
        expected = self.expected["LUT_ximin"]
        actual = self.actual.LUT_ximin

        self.assertEqual(expected, actual)

    def test_LUT_step(self):
        expected = self.expected["LUT_step"]
        actual = self.actual.LUT_step

        self.assertEqual(expected, actual)

    def test_percent_leading_edge(self):
        expected = self.expected["percent_leading_edge"]
        actual = self.actual.percent_leading_edge

        self.assertEqual(expected, actual)

    def test_ini_Epoch(self):
        expected = self.expected["ini_Epoch"]
        actual = self.actual.ini_Epoch

        self.assertEqual(expected, actual)

    def test_ini_Hs(self):
        expected = self.expected["ini_Hs"]
        actual = self.actual.ini_Hs

        self.assertEqual(expected, actual)

    def test_ini_Pu(self):
        expected = self.expected["ini_Pu"]
        actual = self.actual.ini_Pu

        self.assertEqual(expected, actual)

    def test_ini_rou(self):
        expected = self.expected["ini_rou"]
        actual = self.actual.ini_rou

        self.assertEqual(expected, actual)

    def test_ini_error_epoch(self):
        expected = self.expected["ini_error_epoch"]
        actual = self.actual.ini_error_epoch

        self.assertEqual(expected, actual)

    def test_initial_param_fit_feedback_flag(self):
        expected = self.expected["initial_param_fit_feedback_flag"]
        actual = self.actual.initial_param_fit_feedback_flag

        self.assertEqual(expected, actual)

    def test_win_smooth(self):
        expected = self.expected["win_smooth"]
        actual = self.actual.win_smooth

        self.assertEqual(expected, actual)

    def test_range_index_method(self):
        expected = RangeIndexMethod(self.expected["range_index_method"])
        actual = self.actual.range_index_method

        self.assertEqual(expected, actual)

    def test_ref_sample_wd(self):
        expected = self.expected["ref_sample_wd"]
        actual = self.actual.ref_sample_wd

        self.assertEqual(expected, actual)

    def test_fitting_options_ACDC_lb(self):
        expected = self.expected["fitting_options_ACDC_lb"]
        actual = self.actual.fitting_options_ACDC_lb

        self.assertEqual(expected, actual)

    def test_fitting_options_ACDC_ub(self):
        expected = self.expected["fitting_options_ACDC_ub"]
        actual = self.actual.fitting_options_ACDC_ub

        self.assertEqual(expected, actual)

    def test_LUT_f0_path(self):
        expected = self.expected["LUT_f0_path"]
        actual = self.actual.LUT_f0_path

        self.assertEqual(expected, actual)

    def test_mission(self):
        expected = self.expected["mission"]
        actual = self.actual.mission

        self.assertEqual(expected, actual)


