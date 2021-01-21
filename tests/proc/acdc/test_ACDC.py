import unittest
import os
import numpy as np
import scipy.io as scpio

from dedop.proc.sar.acdc.ACDC import ACDCAlgorithm
from dedop.conf import CharacterisationFile, ConstantsFile, ConfigurationFile, ACDCConfiguration
from dedop.util.unittest_helper import UnitTestHelper
from dedop.conf.enums import RangeIndexMethod, AzimuthWindowingMethod
from tests.testing import TestDataLoader
from dedop.model.surface_data import SurfaceData
from dedop.model.acdc_data import ACDCData


class testACDC(unittest.TestCase):

    def test_ACDC01(self):
        # Initialisation
        testHelper = UnitTestHelper()
        fileDir = os.path.dirname(os.path.realpath('__file__'))

        # Input file
        acdc_data = TestDataLoader(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc01/inputs/acdc_data01.txt'), delim=' ')
        rangeIndexMethod = RangeIndexMethod(acdc_data["range_index_method"])

        # Cnf, Chd, Cst files
        cst = ConstantsFile(semi_major_axis_cst = acdc_data["semi_major_axis_cst"],
                            semi_minor_axis_cst  = acdc_data["semi_minor_axis_cst"],
                            c_cst = acdc_data["c_cst"])
        chd = CharacterisationFile(cst, prf_sar_chd = acdc_data["prf_sar"],
                                    N_samples_sar_chd = acdc_data["N_samples_sar_chd"],
                                    uso_freq_nom_chd = acdc_data["uso_freq_nom_chd"],
                                    alt_freq_multiplier_chd = acdc_data["alt_freq_multiplier_chd"],
                                    bw_ku_chd = acdc_data["bw_ku_chd"],
                                    N_ku_pulses_burst_chd = acdc_data["N_ku_pulses_burst_chd"],
                                    freq_ku_chd = acdc_data["freq_ku_chd"])

        cnf = ConfigurationFile(zp_fact_range_cnf = acdc_data["zp_fact_range_cnf"])

        acdcConfig = ACDCConfiguration(range_index_method = rangeIndexMethod,
                                       initial_param_fit_feedback_flag = acdc_data["initial_param_fit_feedback_flag"],
                                       num_iterations = acdc_data["num_iterations"],
                                       mission = acdc_data["mission"],
                                       LUT_f0_path = os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc01/inputs/lut_binary.dat'),
                                       weighting_win_type = acdc_data["weighting_win_type"],
                                       weighting_win_width = acdc_data["weighting_win_width"],
                                       wvfm_discard_samples = acdc_data["wvfm_discard_samples"],
                                       wvfm_discard_samples_begin = acdc_data["wvfm_discard_samples_begin"],
                                       wvfm_discard_samples_end = acdc_data["wvfm_discard_samples_end"],
                                       Thn_flag = acdc_data["Thn_flag"],
                                       fit_noise = acdc_data["fit_noise"],
                                       Thn_w_first = acdc_data["Thn_w_first"],
                                       Thn_w_width = acdc_data["Thn_w_width"],
                                       percent_leading_edge = acdc_data["percent_leading_edge"],
                                       threshold_noise = acdc_data["threshold_noise"],
                                       max_iter_noise = acdc_data["max_iter_noise"],
                                       fitting_options_ACDC_lb = acdc_data["fitting_options_ACDC_lb"],
                                       fitting_options_ACDC_ub = acdc_data["fitting_options_ACDC_ub"],
                                       LUT_ximin = acdc_data["LUT_ximin"],
                                       LUT_ximax = acdc_data["LUT_ximax"],
                                       LUT_step = acdc_data["LUT_step"],
                                       ini_rou = acdc_data["rou"],
                                       rou = acdc_data["rou"],
                                       window_type_a = AzimuthWindowingMethod(acdc_data["window_type_a"]),
                                       window_a_fixed_value = acdc_data["window_a_fixed_value"],
                                       window_type_r = AzimuthWindowingMethod(acdc_data["window_type_r"]),
                                       window_r_fixed_value = acdc_data["window_r_fixed_value"],
                                       ini_Hs = acdc_data["ini_Hs"],
                                       ref_sample_wd = acdc_data["ref_sample_wd"])

        # Algorithm Initialisation
        ACDCalg = ACDCAlgorithm(chd,cst,cnf,acdcConfig)

        # Input arrays
        beams_masked = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc01/inputs/mat/beams_masked.mat'))['beams_masked']
        stack_mask = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc01/inputs/mat/stack_mask.mat'))['stack_mask']
        stack_mask_vector = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc01/inputs/mat/stack_mask_vector.mat'))['stack_mask_vector']
        lat_surf = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc01/inputs/mat/lat_surf.mat'))['lat_surf'].transpose()
        lon_surf = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc01/inputs/mat/lon_surf.mat'))['lon_surf'].transpose()
        alt_sat = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc01/inputs/mat/alt_sat.mat'))['alt_sat'].transpose()
        time_surf = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc01/inputs/mat/time_surf.mat'))['time_surf'].transpose()
        wfm_cor_i2q2_sar_ku = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc01/inputs/mat/wfm_cor_i2q2_sar_ku.mat'))['wfm_cor_i2q2_sar_ku']
        win_delay_surf = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc01/inputs/mat/win_delay_surf.mat'))['win_delay_surf'].transpose()
        x_vel_sat = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc01/inputs/mat/x_vel_sat.mat'))['x_vel_sat'].transpose()
        y_vel_sat = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc01/inputs/mat/y_vel_sat.mat'))['y_vel_sat'].transpose()
        z_vel_sat = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc01/inputs/mat/z_vel_sat.mat'))['z_vel_sat'].transpose()
        pitch_surf = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc01/inputs/mat/pitch_surf.mat'))['pitch_surf'].transpose()
        roll_surf = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc01/inputs/mat/roll_surf.mat'))['roll_surf'].transpose()
        look_ang_surf = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc01/inputs/mat/look_ang_surf.mat'))['look_ang_surf']
        wfm_scaling_factor_sar_ku = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc01/inputs/mat/wfm_scaling_factor_sar_ku.mat'))['wfm_scaling_factor_sar_ku'].transpose()
        alt_rate_sat = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc01/inputs/mat/alt_rate_sat.mat'))['alt_rate_sat'].transpose()

        # Expected output
        acdcLoaded = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc01/expected/ACDC1iter.mat'))['ACDC']
        acdcObject_expected = self.readACDCObject(acdcLoaded, acdc_data["i_surf"])

        # Code
        surface = SurfaceData(cst, chd, beams_masked = beams_masked[acdc_data["i_surf"],:,:], stack_mask = stack_mask[acdc_data["i_surf"],:,:],
                              stack_mask_vector =  stack_mask_vector[acdc_data["i_surf"]], waveform_multilooked = wfm_cor_i2q2_sar_ku[acdc_data["i_surf"]],
                              win_delay_surf = win_delay_surf[acdc_data["i_surf"]], time_surf = time_surf[acdc_data["i_surf"]],
                              lat_surf = lat_surf[acdc_data["i_surf"]], lon_surf = lon_surf[acdc_data["i_surf"]], alt_sat = alt_sat[acdc_data["i_surf"]],
                              x_vel_sat = x_vel_sat[acdc_data["i_surf"]], y_vel_sat = y_vel_sat[acdc_data["i_surf"]], z_vel_sat = z_vel_sat[acdc_data["i_surf"]],
                              pitch_sat = pitch_surf[acdc_data["i_surf"]], roll_sat = roll_surf[acdc_data["i_surf"]], look_angles_surf = look_ang_surf[acdc_data["i_surf"]],
                              t0_surf = acdc_data["t0_surf"], sigma0_scaling_factor = wfm_scaling_factor_sar_ku[acdc_data["i_surf"]],
                              alt_rate_sat = alt_rate_sat[acdc_data["i_surf"]])

        acdcObject, flag = ACDCalg(surface, np.double(acdc_data["lastSSH"]), np.double(acdc_data["lastHs"]))

        # Tests
        self.assertEqual(flag, 0)

        self.assertTrue(testHelper.assertTestArray1D(acdcObject.waveform, acdcObject_expected.waveform, acdc_data["errWave"]))
        self.assertTrue(testHelper.assertTestArray1D(acdcObject.ml_wav_fitted_ACDC, acdcObject_expected.ml_wav_fitted_ACDC, acdc_data["errFitted"]))
        self.assertTrue(testHelper.assertTestArray1D(acdcObject.range_index, acdcObject_expected.range_index, acdc_data["errWave"]))
        self.assertTrue(testHelper.assertTestDouble(acdcObject.Hs, acdcObject_expected.Hs, acdc_data["errParam"]))
        self.assertTrue(testHelper.assertTestDouble(acdcObject.epoch, acdcObject_expected.epoch, acdc_data["errParam"]))
        self.assertTrue(testHelper.assertTestDouble(acdcObject.SSH, acdcObject_expected.SSH, acdc_data["errParam"]))
        self.assertTrue(testHelper.assertTestDouble(acdcObject.retracking_cor, acdcObject_expected.retracking_cor, acdc_data["errParam"]))
        self.assertTrue(testHelper.assertTestDouble(acdcObject.tracker_range, acdcObject_expected.tracker_range, acdc_data["errParam"]))
        self.assertTrue(testHelper.assertTestDouble(acdcObject.corr_coeff, acdcObject_expected.corr_coeff, acdc_data["errParam"]))
        self.assertTrue(testHelper.assertTestDouble(acdcObject.Pu, acdcObject_expected.Pu, acdc_data["errParam"]))
        self.assertTrue(testHelper.assertTestDouble(acdcObject.amp_fit, acdcObject_expected.amp_fit, acdc_data["errParam"]))
        self.assertTrue(testHelper.assertTestDouble(acdcObject.sigma0, acdcObject_expected.sigma0, acdc_data["errParam"]))
        #self.assertTrue(testHelper.assertTestDouble(acdcObject.flag_fitting, acdcObject_expected.flag_fitting, acdc_data["errWave"])) #flag fitting
        self.assertEqual(acdcObject.lat_surf, acdcObject_expected.lat_surf)
        self.assertEqual(acdcObject.lon_surf, acdcObject_expected.lon_surf)
        self.assertEqual(acdcObject.time_sar_kue, acdcObject_expected.time_sar_kue)
        self.assertEqual(acdcObject.alt_rate_sat, acdcObject_expected.alt_rate_sat)

    def test_ACDC02(self):
        # Initialisation
        testHelper = UnitTestHelper()
        fileDir = os.path.dirname(os.path.realpath('__file__'))

        # Input file
        acdc_data = TestDataLoader(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc02/inputs/acdc_data02.txt'), delim=' ')
        rangeIndexMethod = RangeIndexMethod(acdc_data["range_index_method"])

        # Cnf, Chd, Cst files
        cst = ConstantsFile(semi_major_axis_cst = acdc_data["semi_major_axis_cst"],
                            semi_minor_axis_cst  = acdc_data["semi_minor_axis_cst"],
                            c_cst = acdc_data["c_cst"])
        chd = CharacterisationFile(cst, prf_sar_chd = acdc_data["prf_sar"],
                                    N_samples_sar_chd = acdc_data["N_samples_sar_chd"],
                                    uso_freq_nom_chd = acdc_data["uso_freq_nom_chd"],
                                    alt_freq_multiplier_chd = acdc_data["alt_freq_multiplier_chd"],
                                    bw_ku_chd = acdc_data["bw_ku_chd"],
                                    N_ku_pulses_burst_chd = acdc_data["N_ku_pulses_burst_chd"],
                                    freq_ku_chd = acdc_data["freq_ku_chd"])

        cnf = ConfigurationFile(zp_fact_range_cnf = acdc_data["zp_fact_range_cnf"])

        acdcConfig = ACDCConfiguration(range_index_method = rangeIndexMethod,
                                       initial_param_fit_feedback_flag = acdc_data["initial_param_fit_feedback_flag"],
                                       num_iterations = acdc_data["num_iterations"],
                                       mission = acdc_data["mission"],
                                       LUT_f0_path = os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc02/inputs/lut_binary.dat'),
                                       weighting_win_type = acdc_data["weighting_win_type"],
                                       weighting_win_width = acdc_data["weighting_win_width"],
                                       wvfm_discard_samples = acdc_data["wvfm_discard_samples"],
                                       wvfm_discard_samples_begin = acdc_data["wvfm_discard_samples_begin"],
                                       wvfm_discard_samples_end = acdc_data["wvfm_discard_samples_end"],
                                       Thn_flag = acdc_data["Thn_flag"],
                                       fit_noise = acdc_data["fit_noise"],
                                       Thn_w_first = acdc_data["Thn_w_first"],
                                       Thn_w_width = acdc_data["Thn_w_width"],
                                       percent_leading_edge = acdc_data["percent_leading_edge"],
                                       threshold_noise = acdc_data["threshold_noise"],
                                       max_iter_noise = acdc_data["max_iter_noise"],
                                       fitting_options_ACDC_lb = acdc_data["fitting_options_ACDC_lb"],
                                       fitting_options_ACDC_ub = acdc_data["fitting_options_ACDC_ub"],
                                       LUT_ximin = acdc_data["LUT_ximin"],
                                       LUT_ximax = acdc_data["LUT_ximax"],
                                       LUT_step = acdc_data["LUT_step"],
                                       ini_rou = acdc_data["rou"],
                                       rou = acdc_data["rou"],
                                       window_type_a = AzimuthWindowingMethod(acdc_data["window_type_a"]),
                                       window_a_fixed_value = acdc_data["window_a_fixed_value"],
                                       window_type_r = AzimuthWindowingMethod(acdc_data["window_type_r"]),
                                       window_r_fixed_value = acdc_data["window_r_fixed_value"],
                                       ini_Hs = acdc_data["ini_Hs"],
                                       ref_sample_wd = acdc_data["ref_sample_wd"])

        # Algorithm Initialisation
        ACDCalg = ACDCAlgorithm(chd,cst,cnf,acdcConfig)

        # Input arrays
        beams_masked = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc02/inputs/mat/beams_masked.mat'))['beams_masked']
        stack_mask = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc02/inputs/mat/stack_mask.mat'))['stack_mask']
        stack_mask_vector = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc02/inputs/mat/stack_mask_vector.mat'))['stack_mask_vector']
        lat_surf = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc02/inputs/mat/lat_surf.mat'))['lat_surf'].transpose()
        lon_surf = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc02/inputs/mat/lon_surf.mat'))['lon_surf'].transpose()
        alt_sat = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc02/inputs/mat/alt_sat.mat'))['alt_sat'].transpose()
        time_surf = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc02/inputs/mat/time_surf.mat'))['time_surf'].transpose()
        wfm_cor_i2q2_sar_ku = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc02/inputs/mat/wfm_cor_i2q2_sar_ku.mat'))['wfm_cor_i2q2_sar_ku']
        win_delay_surf = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc02/inputs/mat/win_delay_surf.mat'))['win_delay_surf'].transpose()
        x_vel_sat = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc02/inputs/mat/x_vel_sat.mat'))['x_vel_sat'].transpose()
        y_vel_sat = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc02/inputs/mat/y_vel_sat.mat'))['y_vel_sat'].transpose()
        z_vel_sat = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc02/inputs/mat/z_vel_sat.mat'))['z_vel_sat'].transpose()
        pitch_surf = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc02/inputs/mat/pitch_surf.mat'))['pitch_surf'].transpose()
        roll_surf = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc02/inputs/mat/roll_surf.mat'))['roll_surf'].transpose()
        look_ang_surf = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc02/inputs/mat/look_ang_surf.mat'))['look_ang_surf']
        wfm_scaling_factor_sar_ku = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc02/inputs/mat/wfm_scaling_factor_sar_ku.mat'))['wfm_scaling_factor_sar_ku'].transpose()
        alt_rate_sat = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc02/inputs/mat/alt_rate_sat.mat'))['alt_rate_sat'].transpose()

        # Expected output
        acdcLoaded = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc02/expected/ACDC02.mat'))['ACDC']
        acdcObject_expected = self.readACDCObject(acdcLoaded, acdc_data["i_surf"])

        # Code
        surface = SurfaceData(cst, chd, beams_masked = beams_masked[acdc_data["i_surf"],:,:], stack_mask = stack_mask[acdc_data["i_surf"],:,:],
                              stack_mask_vector =  stack_mask_vector[acdc_data["i_surf"]], waveform_multilooked = wfm_cor_i2q2_sar_ku[acdc_data["i_surf"]],
                              win_delay_surf = win_delay_surf[acdc_data["i_surf"]], time_surf = time_surf[acdc_data["i_surf"]],
                              lat_surf = lat_surf[acdc_data["i_surf"]], lon_surf = lon_surf[acdc_data["i_surf"]], alt_sat = alt_sat[acdc_data["i_surf"]],
                              x_vel_sat = x_vel_sat[acdc_data["i_surf"]], y_vel_sat = y_vel_sat[acdc_data["i_surf"]], z_vel_sat = z_vel_sat[acdc_data["i_surf"]],
                              pitch_sat = pitch_surf[acdc_data["i_surf"]], roll_sat = roll_surf[acdc_data["i_surf"]], look_angles_surf = look_ang_surf[acdc_data["i_surf"]],
                              t0_surf = acdc_data["t0_surf"], sigma0_scaling_factor = wfm_scaling_factor_sar_ku[acdc_data["i_surf"]],
                              alt_rate_sat = alt_rate_sat[acdc_data["i_surf"]])

        acdcObject, flag = ACDCalg(surface, np.double(acdc_data["lastSSH"]), np.double(acdc_data["lastHs"]))

        # Tests
        self.assertEqual(flag, 0)

        self.assertTrue(testHelper.assertTestArray1D(acdcObject.waveform, acdcObject_expected.waveform, acdc_data["errWave"]))
        self.assertTrue(testHelper.assertTestArray1D(acdcObject.ml_wav_fitted_ACDC, acdcObject_expected.ml_wav_fitted_ACDC, acdc_data["errFitted"]))
        self.assertTrue(testHelper.assertTestArray1D(acdcObject.range_index, acdcObject_expected.range_index, acdc_data["errWave"]))
        self.assertTrue(testHelper.assertTestDouble(acdcObject.Hs, acdcObject_expected.Hs, acdc_data["errParam"]))
        self.assertTrue(testHelper.assertTestDouble(acdcObject.epoch, acdcObject_expected.epoch, acdc_data["errParam"]))
        self.assertTrue(testHelper.assertTestDouble(acdcObject.SSH, acdcObject_expected.SSH, acdc_data["errParam"]))
        self.assertTrue(testHelper.assertTestDouble(acdcObject.retracking_cor, acdcObject_expected.retracking_cor, acdc_data["errParam"]))
        self.assertTrue(testHelper.assertTestDouble(acdcObject.tracker_range, acdcObject_expected.tracker_range, acdc_data["errParam"]))
        self.assertTrue(testHelper.assertTestDouble(acdcObject.corr_coeff, acdcObject_expected.corr_coeff, acdc_data["errParam"]))
        self.assertTrue(testHelper.assertTestDouble(acdcObject.Pu, acdcObject_expected.Pu, acdc_data["errParam"]))
        self.assertTrue(testHelper.assertTestDouble(acdcObject.amp_fit, acdcObject_expected.amp_fit, acdc_data["errParam"]))
        self.assertTrue(testHelper.assertTestDouble(acdcObject.sigma0, acdcObject_expected.sigma0, acdc_data["errParam"]))
        #self.assertTrue(testHelper.assertTestDouble(acdcObject.flag_fitting, acdcObject_expected.flag_fitting, acdc_data["errWave"])) #flag fitting
        self.assertEqual(acdcObject.lat_surf, acdcObject_expected.lat_surf)
        self.assertEqual(acdcObject.lon_surf, acdcObject_expected.lon_surf)
        self.assertEqual(acdcObject.time_sar_kue, acdcObject_expected.time_sar_kue)
        self.assertEqual(acdcObject.alt_rate_sat, acdcObject_expected.alt_rate_sat)

    def test_ACDC03(self):
        # Initialisation
        testHelper = UnitTestHelper()
        fileDir = os.path.dirname(os.path.realpath('__file__'))

        # Input file
        acdc_data = TestDataLoader(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc03/inputs/acdc_data03.txt'), delim=' ')
        rangeIndexMethod = RangeIndexMethod(acdc_data["range_index_method"])

        # Cnf, Chd, Cst files
        cst = ConstantsFile(semi_major_axis_cst = acdc_data["semi_major_axis_cst"],
                            semi_minor_axis_cst  = acdc_data["semi_minor_axis_cst"],
                            c_cst = acdc_data["c_cst"])
        chd = CharacterisationFile(cst, prf_sar_chd = acdc_data["prf_sar"],
                                    N_samples_sar_chd = acdc_data["N_samples_sar_chd"],
                                    uso_freq_nom_chd = acdc_data["uso_freq_nom_chd"],
                                    alt_freq_multiplier_chd = acdc_data["alt_freq_multiplier_chd"],
                                    bw_ku_chd = acdc_data["bw_ku_chd"],
                                    N_ku_pulses_burst_chd = acdc_data["N_ku_pulses_burst_chd"],
                                    freq_ku_chd = acdc_data["freq_ku_chd"])

        cnf = ConfigurationFile(zp_fact_range_cnf = acdc_data["zp_fact_range_cnf"])

        acdcConfig = ACDCConfiguration(range_index_method = rangeIndexMethod,
                                       initial_param_fit_feedback_flag = acdc_data["initial_param_fit_feedback_flag"],
                                       num_iterations = acdc_data["num_iterations"],
                                       mission = acdc_data["mission"],
                                       LUT_f0_path = os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc03/inputs/lut_binary.dat'),
                                       weighting_win_type = acdc_data["weighting_win_type"],
                                       weighting_win_width = acdc_data["weighting_win_width"],
                                       wvfm_discard_samples = acdc_data["wvfm_discard_samples"],
                                       wvfm_discard_samples_begin = acdc_data["wvfm_discard_samples_begin"],
                                       wvfm_discard_samples_end = acdc_data["wvfm_discard_samples_end"],
                                       Thn_flag = acdc_data["Thn_flag"],
                                       fit_noise = acdc_data["fit_noise"],
                                       Thn_w_first = acdc_data["Thn_w_first"],
                                       Thn_w_width = acdc_data["Thn_w_width"],
                                       percent_leading_edge = acdc_data["percent_leading_edge"],
                                       threshold_noise = acdc_data["threshold_noise"],
                                       max_iter_noise = acdc_data["max_iter_noise"],
                                       fitting_options_ACDC_lb = acdc_data["fitting_options_ACDC_lb"],
                                       fitting_options_ACDC_ub = acdc_data["fitting_options_ACDC_ub"],
                                       LUT_ximin = acdc_data["LUT_ximin"],
                                       LUT_ximax = acdc_data["LUT_ximax"],
                                       LUT_step = acdc_data["LUT_step"],
                                       ini_rou = acdc_data["rou"],
                                       rou = acdc_data["rou"],
                                       window_type_a = AzimuthWindowingMethod(acdc_data["window_type_a"]),
                                       window_a_fixed_value = acdc_data["window_a_fixed_value"],
                                       window_type_r = AzimuthWindowingMethod(acdc_data["window_type_r"]),
                                       window_r_fixed_value = acdc_data["window_r_fixed_value"],
                                       ini_Hs = acdc_data["ini_Hs"],
                                       ref_sample_wd = acdc_data["ref_sample_wd"])

        # Algorithm Initialisation
        ACDCalg = ACDCAlgorithm(chd,cst,cnf,acdcConfig)

        # Input arrays
        beams_masked = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc03/inputs/mat/beams_masked.mat'))['beams_masked']
        stack_mask = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc03/inputs/mat/stack_mask.mat'))['stack_mask']
        stack_mask_vector = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc03/inputs/mat/stack_mask_vector.mat'))['stack_mask_vector']
        lat_surf = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc03/inputs/mat/lat_surf.mat'))['lat_surf'].transpose()
        lon_surf = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc03/inputs/mat/lon_surf.mat'))['lon_surf'].transpose()
        alt_sat = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc03/inputs/mat/alt_sat.mat'))['alt_sat'].transpose()
        time_surf = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc03/inputs/mat/time_surf.mat'))['time_surf'].transpose()
        wfm_cor_i2q2_sar_ku = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc03/inputs/mat/wfm_cor_i2q2_sar_ku.mat'))['wfm_cor_i2q2_sar_ku']
        win_delay_surf = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc03/inputs/mat/win_delay_surf.mat'))['win_delay_surf'].transpose()
        x_vel_sat = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc03/inputs/mat/x_vel_sat.mat'))['x_vel_sat'].transpose()
        y_vel_sat = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc03/inputs/mat/y_vel_sat.mat'))['y_vel_sat'].transpose()
        z_vel_sat = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc03/inputs/mat/z_vel_sat.mat'))['z_vel_sat'].transpose()
        pitch_surf = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc03/inputs/mat/pitch_surf.mat'))['pitch_surf'].transpose()
        roll_surf = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc03/inputs/mat/roll_surf.mat'))['roll_surf'].transpose()
        look_ang_surf = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc03/inputs/mat/look_ang_surf.mat'))['look_ang_surf']
        wfm_scaling_factor_sar_ku = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc03/inputs/mat/wfm_scaling_factor_sar_ku.mat'))['wfm_scaling_factor_sar_ku'].transpose()
        alt_rate_sat = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc03/inputs/mat/alt_rate_sat.mat'))['alt_rate_sat'].transpose()

        # Expected output
        acdcLoaded = scpio.loadmat(os.path.join(fileDir, 'test_data/acdc/test_acdc/test_acdc03/expected/ACDC03.mat'))['ACDC']
        acdcObject_expected = self.readACDCObject(acdcLoaded, acdc_data["i_surf"])

        # Code
        surface = SurfaceData(cst, chd, beams_masked = beams_masked[acdc_data["i_surf"],:,:], stack_mask = stack_mask[acdc_data["i_surf"],:,:],
                              stack_mask_vector =  stack_mask_vector[acdc_data["i_surf"]], waveform_multilooked = wfm_cor_i2q2_sar_ku[acdc_data["i_surf"]],
                              win_delay_surf = win_delay_surf[acdc_data["i_surf"]], time_surf = time_surf[acdc_data["i_surf"]],
                              lat_surf = lat_surf[acdc_data["i_surf"]], lon_surf = lon_surf[acdc_data["i_surf"]], alt_sat = alt_sat[acdc_data["i_surf"]],
                              x_vel_sat = x_vel_sat[acdc_data["i_surf"]], y_vel_sat = y_vel_sat[acdc_data["i_surf"]], z_vel_sat = z_vel_sat[acdc_data["i_surf"]],
                              pitch_sat = pitch_surf[acdc_data["i_surf"]], roll_sat = roll_surf[acdc_data["i_surf"]], look_angles_surf = look_ang_surf[acdc_data["i_surf"]],
                              t0_surf = acdc_data["t0_surf"], sigma0_scaling_factor = wfm_scaling_factor_sar_ku[acdc_data["i_surf"]],
                              alt_rate_sat = alt_rate_sat[acdc_data["i_surf"]])

        acdcObject, flag = ACDCalg(surface, np.double(acdc_data["lastSSH"]), np.double(acdc_data["lastHs"]))

        # Tests
        self.assertEqual(flag, 0)

        self.assertTrue(testHelper.assertTestArray1D(acdcObject.waveform, acdcObject_expected.waveform, acdc_data["errWave"]))
        self.assertTrue(testHelper.assertTestArray1D(acdcObject.ml_wav_fitted_ACDC, acdcObject_expected.ml_wav_fitted_ACDC, acdc_data["errFitted"]))
        self.assertTrue(testHelper.assertTestArray1D(acdcObject.range_index, acdcObject_expected.range_index, acdc_data["errWave"]))
        self.assertTrue(testHelper.assertTestDouble(acdcObject.Hs, acdcObject_expected.Hs, acdc_data["errParam"]))
        self.assertTrue(testHelper.assertTestDouble(acdcObject.epoch, acdcObject_expected.epoch, acdc_data["errParam"]))
        self.assertTrue(testHelper.assertTestDouble(acdcObject.SSH, acdcObject_expected.SSH, acdc_data["errParam"]))
        self.assertTrue(testHelper.assertTestDouble(acdcObject.retracking_cor, acdcObject_expected.retracking_cor, acdc_data["errParam"]))
        self.assertTrue(testHelper.assertTestDouble(acdcObject.tracker_range, acdcObject_expected.tracker_range, acdc_data["errParam"]))
        self.assertTrue(testHelper.assertTestDouble(acdcObject.corr_coeff, acdcObject_expected.corr_coeff, acdc_data["errParam"]))
        self.assertTrue(testHelper.assertTestDouble(acdcObject.Pu, acdcObject_expected.Pu, acdc_data["errParam"]))
        self.assertTrue(testHelper.assertTestDouble(acdcObject.amp_fit, acdcObject_expected.amp_fit, acdc_data["errParam"]))
        self.assertTrue(testHelper.assertTestDouble(acdcObject.sigma0, acdcObject_expected.sigma0, acdc_data["errParam"]))
        #self.assertTrue(testHelper.assertTestDouble(acdcObject.flag_fitting, acdcObject_expected.flag_fitting, acdc_data["errWave"])) #flag fitting
        self.assertEqual(acdcObject.lat_surf, acdcObject_expected.lat_surf)
        self.assertEqual(acdcObject.lon_surf, acdcObject_expected.lon_surf)
        self.assertEqual(acdcObject.time_sar_kue, acdcObject_expected.time_sar_kue)
        self.assertEqual(acdcObject.alt_rate_sat, acdcObject_expected.alt_rate_sat)


    def readACDCObject(self, acdcLoaded, i) -> ACDCData:

        return ACDCData(waveform = acdcLoaded[i][0][0][0],
                ml_wav_fitted_ACDC = acdcLoaded[i][0][1][0],
                range_index = acdcLoaded[i][0][2][0],
                Hs = acdcLoaded[i][0][3][0][0],
                epoch = acdcLoaded[i][0][4][0][0],
                SSH = acdcLoaded[i][0][5][0][0],
                retracking_cor = acdcLoaded[i][0][6][0][0],
                tracker_range = acdcLoaded[i][0][7][0][0],
                corr_coeff = acdcLoaded[i][0][8][0][0],
                Pu = acdcLoaded[i][0][9][0][0],
                amp_fit = acdcLoaded[i][0][10][0][0],
                sigma0 = acdcLoaded[i][0][11][0][0],
                flag_fitting = acdcLoaded[i][0][12][0][0],
                lat_surf = acdcLoaded[i][0][13][0][0],
                lon_surf = acdcLoaded[i][0][14][0][0],
                time_sar_kue = acdcLoaded[i][0][15][0][0],
                alt_rate_sat = acdcLoaded[i][0][16][0][0])

if __name__ == "__main__":
    unittest.main()