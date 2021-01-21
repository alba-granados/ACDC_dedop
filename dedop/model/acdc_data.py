from collections import OrderedDict
from typing import Any

class ACDCData():
    """
    Class for storing ACDC data.
    """
    @property
    def waveform(self):
        return self["waveform"]

    @waveform.setter
    def waveform(self, value):
        self["waveform"] = value

    @property
    def ml_wav_fitted_ACDC(self):
        return self["ml_wav_fitted_ACDC"]

    @ml_wav_fitted_ACDC.setter
    def ml_wav_fitted_ACDC(self, value):
        self["ml_wav_fitted_ACDC"] = value

    @property
    def range_index(self):
        return self["range_index"]

    @range_index.setter
    def range_index(self, value):
        self["range_index"] = value

    @property
    def Hs(self):
        return self["Hs"]

    @Hs.setter
    def Hs(self, value):
        self["Hs"] = value

    @property
    def epoch(self):
        return self["epoch"]

    @epoch.setter
    def epoch(self, value):
        self["epoch"] = value

    @property
    def SSH(self):
        return self["SSH"]

    @SSH.setter
    def SSH(self, value):
        self["SSH"] = value

    @property
    def retracking_cor(self):
        return self["retracking_cor"]

    @retracking_cor.setter
    def retracking_cor(self, value):
        self["retracking_cor"] = value

    @property
    def tracker_range(self):
        return self["tracker_range"]

    @tracker_range.setter
    def tracker_range(self, value):
        self["tracker_range"] = value

    @property
    def corr_coeff(self):
        return self["corr_coeff"]

    @corr_coeff.setter
    def corr_coeff(self, value):
        self["corr_coeff"] = value

    @property
    def Pu(self):
        return self["Pu"]

    @Pu.setter
    def Pu(self, value):
        self["Pu"] = value

    @property
    def amp_fit(self):
        return self["amp_fit"]

    @amp_fit.setter
    def amp_fit(self, value):
        self["amp_fit"] = value

    @property
    def sigma0(self):
        return self["sigma0"]

    @sigma0.setter
    def sigma0(self, value):
        self["sigma0"] = value

    @property
    def flag_fitting(self):
        return self["flag_fitting"]

    @flag_fitting.setter
    def flag_fitting(self, value):
        self["flag_fitting"] = value

    @property
    def lat_surf(self):
        return self["lat_surf"]

    @lat_surf.setter
    def lat_surf(self, value):
        self["lat_surf"] = value

    @property
    def lon_surf(self):
        return self["lon_surf"]

    @lon_surf.setter
    def lon_surf(self, value):
        self["lon_surf"] = value

    @property
    def time_sar_kue(self):
        return self["time_sar_kue"]

    @time_sar_kue.setter
    def time_sar_kue(self, value):
        self["time_sar_kue"] = value

    @property
    def alt_rate_sat(self):
        return self["alt_rate_sat"]

    @alt_rate_sat.setter
    def alt_rate_sat(self, value):
        self["alt_rate_sat"] = value


    def __init__(self, *dicts: dict, **values: Any):
        # create empty data container
        self._data = OrderedDict()

         # get values from dictionaries
        for values_group in dicts:
            self._data.update(values_group)
        # get values from keyword arguments
        self._data.update(values)

    def __setitem__(self, key: str, value: Any) -> None:
        if not hasattr(self.__class__, key):
            raise KeyError("{} has no attribute '{}'".format(self, key))
        self._data[key] = value

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

class NonFitParams():
    @property
    def Neff(self):
        return self["Neff"]

    @Neff.setter
    def Neff(self, value):
        self["Neff"] = value

    @property
    def alphag_a(self):
        return self["alphag_a"]

    @alphag_a.setter
    def alphag_a(self, value):
        self["alphag_a"] = value

    @property
    def alphag_r(self):
        return self["alphag_r"]

    @alphag_r.setter
    def alphag_r(self, value):
        self["alphag_r"] = value

    @property
    def alphax(self):
        return self["alphax"]

    @alphax.setter
    def alphax(self, value):
        self["alphax"] = value

    @property
    def alphay(self):
        return self["alphay"]

    @alphay.setter
    def alphay(self, value):
        self["alphay"] = value

    @property
    def Lx(self):
        return self["Lx"]

    @Lx.setter
    def Lx(self, value):
        self["Lx"] = value

    @property
    def Ly(self):
        return self["Ly"]

    @Ly.setter
    def Ly(self, value):
        self["Ly"] = value

    @property
    def Lz(self):
        return self["Lz"]

    @Lz.setter
    def Lz(self, value):
        self["Lz"] = value

    @property
    def h(self):
        return self["h"]

    @h.setter
    def h(self, value):
        self["h"] = value

    @property
    def xp(self):
        return self["xp"]

    @xp.setter
    def xp(self, value):
        self["xp"] = value

    @property
    def yp(self):
        return self["yp"]

    @yp.setter
    def yp(self, value):
        self["yp"] = value

    @property
    def pri_surf(self):
        return self["pri_surf"]

    @pri_surf.setter
    def pri_surf(self, value):
        self["pri_surf"] = value

    @property
    def waveskew(self):
        return self["waveskew"]

    @waveskew.setter
    def waveskew(self, value):
        self["waveskew"] = value

    @property
    def EMbias(self):
        return self["EMbias"]

    @EMbias.setter
    def EMbias(self, value):
        self["EMbias"] = value

    @property
    def rou(self):
        return self["rou"]

    @rou.setter
    def rou(self, value):
        self["rou"] = value

    @property
    def v_sat(self):
        return self["v_sat"]

    @v_sat.setter
    def v_sat(self, value):
        self["v_sat"] = value

    @property
    def Npulses(self):
        return self["Npulses"]

    @Npulses.setter
    def Npulses(self, value):
        self["Npulses"] = value

    @property
    def A_s2Ga(self):
        return self["A_s2Ga"]

    @A_s2Ga.setter
    def A_s2Ga(self, value):
        self["A_s2Ga"] = value

    @property
    def A_s2Gr(self):
        return self["A_s2Gr"]

    @A_s2Gr.setter
    def A_s2Gr(self, value):
        self["A_s2Gr"] = value

    @property
    def bw_Rx(self):
        return self["bw_Rx"]

    @bw_Rx.setter
    def bw_Rx(self, value):
        self["bw_Rx"] = value


    def __init__(self, *dicts: dict, **values: Any):
        # create empty data container
        self._data = OrderedDict()

         # get values from dictionaries
        for values_group in dicts:
            self._data.update(values_group)
        # get values from keyword arguments
        self._data.update(values)

    def __setitem__(self, key: str, value: Any) -> None:
        if not hasattr(self.__class__, key):
            raise KeyError("{} has no attribute '{}'".format(self, key))
        self._data[key] = value

    def __getitem__(self, key: str) -> Any:
        return self._data[key]


class L1BSACDC():
    @property
    def pri_sar_sat_beam(self):
        return self["pri_sar_sat_beam"]

    @pri_sar_sat_beam.setter
    def pri_sar_sat_beam(self, value):
        self["pri_sar_sat_beam"] = value

    @property
    def alt_sat(self):
        return self["alt_sat"]

    @alt_sat.setter
    def alt_sat(self, value):
        self["alt_sat"] = value

    @property
    def x_vel_sat(self):
        return self["x_vel_sat"]

    @x_vel_sat.setter
    def x_vel_sat(self, value):
        self["x_vel_sat"] = value

    @property
    def y_vel_sat(self):
        return self["y_vel_sat"]

    @y_vel_sat.setter
    def y_vel_sat(self, value):
        self["y_vel_sat"] = value

    @property
    def z_vel_sat(self):
        return self["z_vel_sat"]

    @z_vel_sat.setter
    def z_vel_sat(self, value):
        self["z_vel_sat"] = value

    @property
    def lat_sat(self):
        return self["lat_sat"]

    @lat_sat.setter
    def lat_sat(self, value):
        self["lat_sat"] = value

    @property
    def pitch_surf(self):
        return self["pitch_surf"]

    @pitch_surf.setter
    def pitch_surf(self, value):
        self["pitch_surf"] = value

    @property
    def roll_surf(self):
        return self["roll_surf"]

    @roll_surf.setter
    def roll_surf(self, value):
        self["roll_surf"] = value

    @property
    def fs_clock_ku_surf(self):
        return self["fs_clock_ku_surf"]

    @fs_clock_ku_surf.setter
    def fs_clock_ku_surf(self, value):
        self["fs_clock_ku_surf"] = value

    @property
    def start_beam(self):
        return self["start_beam"]

    @start_beam.setter
    def start_beam(self, value):
        self["start_beam"] = value

    @property
    def stop_beam(self):
        return self["stop_beam"]

    @stop_beam.setter
    def stop_beam(self, value):
        self["stop_beam"] = value

    @property
    def N_beams_start_stop(self):
        return self["N_beams_start_stop"]

    @N_beams_start_stop.setter
    def N_beams_start_stop(self, value):
        self["N_beams_start_stop"] = value

    @property
    def delta_range(self):
        return self["delta_range"]

    @delta_range.setter
    def delta_range(self, value):
        self["delta_range"] = value


    def __init__(self, *dicts: dict, **values: Any):
        # create empty data container
        self._data = OrderedDict()

         # get values from dictionaries
        for values_group in dicts:
            self._data.update(values_group)
        # get values from keyword arguments
        self._data.update(values)

    def __setitem__(self, key: str, value: Any) -> None:
        if not hasattr(self.__class__, key):
            raise KeyError("{} has no attribute '{}'".format(self, key))
        self._data[key] = value

    def __getitem__(self, key: str) -> Any:
        return self._data[key]


