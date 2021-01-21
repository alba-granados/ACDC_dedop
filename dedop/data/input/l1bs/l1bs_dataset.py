from typing import Dict, Any
import numpy as np

from dedop.conf import ConfigurationFile, CharacterisationFile, ConstantsFile
from ...output.l1bs_writer import L1BSVariables, L1BSDimensions

from ..netcdf_reader_l1bs import NetCDFReaderL1BS

class L1BSDataset():

    def __init__(self, filename: str, cnf: ConfigurationFile, cst: ConstantsFile, chd: CharacterisationFile):
        self.cnf = cnf
        self.cst = cst
        self.chd = chd

        self.dataSet = NetCDFReaderL1BS(filename)

    def readL1BS(self, index: int) -> Dict[str, Any]:
        iq_scale_value = self.dataSet.get_value(L1BSVariables.iq_scale_factor_l1bs_echo_sar_ku, index)
        i_echoes = self.dataSet.get_value(L1BSVariables.i_echoes_ku_l1bs_echo_sar_ku, index) * iq_scale_value
        q_echoes = self.dataSet.get_value(L1BSVariables.q_echoes_ku_l1bs_echo_sar_ku, index) * iq_scale_value

        beams_iq = np.sqrt(i_echoes * i_echoes + q_echoes * q_echoes)
        beams_masked = beams_iq * self.dataSet.get_value(L1BSVariables.stack_mask_l1bs_echo_sar_ku, index)

        waveform_scale = pow(10, -self.dataSet.get_value(L1BSVariables.agc_ku_l1bs_echo_sar_ku, index) / 10)
        waveform =  self.dataSet.get_value(L1BSVariables.i2q2_meas_ku_l1bs_echo_sar_ku, index) / waveform_scale

        data = {"beams_masked" : beams_masked,
                "stack_mask" : self.dataSet.get_value(L1BSVariables.stack_mask_l1bs_echo_sar_ku, index),
                "stack_mask_vector" : self.dataSet.get_value(L1BSVariables.stack_mask_vector_l1bs_echo_sar_ku, index),
                "waveform_multilooked" : waveform,
                "win_delay_surf" : self.dataSet.get_value(L1BSVariables.range_ku_l1bs_echo_sar_ku, index) * 2 / self.cst.c,
                "time_surf" : self.dataSet.get_value(L1BSVariables.time_l1bs_echo_sar_ku, index),
                "lat_surf" : np.radians(self.dataSet.get_value(L1BSVariables.lat_l1bs_echo_sar_ku, index)),
                "lon_surf" : np.radians(self.dataSet.get_value(L1BSVariables.lon_l1bs_echo_sar_ku, index)),
                "alt_sat" : self.dataSet.get_value(L1BSVariables.alt_l1bs_echo_sar_ku, index),
                "alt_rate_sat" : self.dataSet.get_value(L1BSVariables.orb_alt_rate_l1bs_echo_sar_ku, index),
                "x_vel_sat" : self.dataSet.get_value(L1BSVariables.x_vel_l1bs_echo_sar_ku, index),
                "y_vel_sat" : self.dataSet.get_value(L1BSVariables.y_vel_l1bs_echo_sar_ku, index),
                "z_vel_sat" : self.dataSet.get_value(L1BSVariables.z_vel_l1bs_echo_sar_ku, index),
                "pitch_sat" : self.dataSet.get_value(L1BSVariables.pitch_sat_pointing_l1bs_echo_sar_ku, index),
                "roll_sat" : self.dataSet.get_value(L1BSVariables.roll_sat_pointing_l1bs_echo_sar_ku, index),
                "look_angles_surf" : self.dataSet.get_value(L1BSVariables.look_ang_l1bs_echo_sar_ku, index),
                "t0_surf" : self.dataSet.get_value(L1BSVariables.t0_surf_l1bs_echo_sar_ku, index),
                "sigma0_scaling_factor" : self.dataSet.get_value(L1BSVariables.scale_factor_ku_l1bs_echo_sar_ku, index)
                }

        return data

    def getDimension(self, dimName: L1BSDimensions = L1BSDimensions.time_l1bs_echo_sar_ku):
        """
        return the dimension by parameter dimName, by default return time_l1bs_echo_sar_ku dimension
        """
        return self.dataSet.dimensions[dimName.value]

    def close(self) -> None:
        self.dataSet.close()