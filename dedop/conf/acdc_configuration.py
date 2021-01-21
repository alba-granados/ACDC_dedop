import numpy as np

from .auxiliary_file_reader import *
from .enums import AzimuthWindowingMethod, RangeIndexMethod


class ACDCConfiguration(AuxiliaryFileReader):
    """
    class for loading the ACDC Configuration.
    """
    _id = "ACDCCNF"
    _fileversion = 0

    def __init__(self, filename: str=None, **kwargs: Any):
        super().__init__(filename, **kwargs)

    # iterations of ACDC processing over the same surface
    num_iterations = AuxiliaryParameter("num_iterations", param_type=int)

    # iterations tracks over all the surfaces
    n_iterations_track = AuxiliaryParameter("n_iterations_track",
                                            param_type=int,
                                            default_value=1)

    # discarding samples
    wvfm_discard_samples = \
        AuxiliaryParameter("wvfm_discard_samples", param_type=bool)
    wvfm_discard_samples_begin = \
        AuxiliaryParameter("wvfm_discard_samples_begin", param_type=int)
    wvfm_discard_samples_end = \
        AuxiliaryParameter("wvfm_discard_samples_end", param_type=int)

    # retracking multilooking acdc
    weighting_win_type = \
        AuxiliaryParameter("weighting_win_type", param_type=str, default_value="gaussian") # TODO: Default?
    weighting_win_width = \
        AuxiliaryParameter("weighting_win_width", param_type=float)

    # noise estimation
    Thn_flag = AuxiliaryParameter("Thn_flag", param_type=bool)
    fit_noise = AuxiliaryParameter("fit_noise", param_type=bool)
    Thn_w_first = AuxiliaryParameter("Thn_w_first", param_type=int)
    Thn_w_width = AuxiliaryParameter("Thn_w_width", param_type=int)
    threshold_noise = AuxiliaryParameter("threshold_noise", param_type=float)
    max_iter_noise = AuxiliaryParameter("max_iter_noise", param_type=int)

    # surface parameter
    rou_flag = AuxiliaryParameter("rou_flag", param_type=bool)
    rou = AuxiliaryParameter("rou", param_type=float)
    Hs = AuxiliaryParameter("Hs", param_type=float)

    # PTR definition
    window_type_a = \
        AuxiliaryParameter("window_type_a", param_type=AzimuthWindowingMethod)
    window_a_fixed_value = \
        AuxiliaryParameter("window_a_fixed_value", param_type=float)
    window_type_r = \
        AuxiliaryParameter("window_type_r", param_type=AzimuthWindowingMethod)
    window_r_fixed_value = \
        AuxiliaryParameter("window_r_fixed_value", param_type=float)

    # look up tables configuration
    LUT_ximax = AuxiliaryParameter("LUT_ximax", param_type=float)
    LUT_ximin = AuxiliaryParameter("LUT_ximin", param_type=float)
    LUT_step = AuxiliaryParameter("LUT_step", param_type=float)

    # pre-processing stage
    percent_leading_edge = \
        AuxiliaryParameter("percent_leading_edge", param_type=float)

    # fitting configuration
    # initial values
    ini_Epoch = AuxiliaryParameter("ini_Epoch", param_type=float)
    ini_Hs = AuxiliaryParameter("ini_Hs", param_type=float)
    ini_Pu = AuxiliaryParameter("ini_Pu", param_type=float)
    ini_rou = AuxiliaryParameter("ini_rou", param_type=float)
    ini_error_epoch = AuxiliaryParameter("ini_error_epoch", param_type=float)
    initial_param_fit_feedback_flag = \
        AuxiliaryParameter("initial_param_fit_feedback_flag", param_type=bool)
    win_smooth = AuxiliaryParameter("win_smooth", param_type=int)

    # range indexation
    range_index_method = \
        AuxiliaryParameter("range_index_method", param_type=RangeIndexMethod)

    # reference bin window delay
    ref_sample_wd = AuxiliaryParameter("ref_sample_wd", param_type=float)

    # fitting routine specifications
    fitting_options_ACDC_lb = \
        AuxiliaryParameter("fitting_options_ACDC_lb", param_type=list, default_value = [])
    fitting_options_ACDC_ub = \
        AuxiliaryParameter("fitting_options_ACDC_ub", param_type=list, default_value = [])

    # acdc algorithm inputs
    LUT_f0_path = AuxiliaryParameter("LUT_f0_path", param_type=str)
    mission = AuxiliaryParameter("mission", param_type=str)

    # antenna
    @property
    def antenna_beamwidth_along_track_ku(self):
        return 1.35*np.pi/180

    @property
    def antenna_beamwidth_across_track_ku(self):
        return 1.35*np.pi/180
