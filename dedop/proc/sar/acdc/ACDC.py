import numpy as np
import math as m

from dedop.conf import CharacterisationFile, ConstantsFile, ConfigurationFile, ACDCConfiguration
from dedop.conf.enums import RangeIndexMethod, AzimuthWindowingMethod
from dedop.model.acdc_data import ACDCData, NonFitParams, L1BSACDC
from dedop.model.surface_data import SurfaceData

from ..base_algorithm import BaseAlgorithm
from .amplitude_compensation import AmplitudeCompensationAlgorithm
from .dilation_compensation import DilationCompensationAlgorithm
from .retracking import RetrackingAlgorithm


class ACDCAlgorithm(BaseAlgorithm):

    def __init__(self, chd: CharacterisationFile, cst: ConstantsFile,
                 cnf: ConfigurationFile, acdcCnf: ACDCConfiguration):
        super().__init__(chd, cst, cnf)

        self.acdcConfig = acdcCnf

        self.amplitude_compensation_algorithm = AmplitudeCompensationAlgorithm(chd, cst, cnf, acdcCnf)
        self.dilation_compensation_algorithm = DilationCompensationAlgorithm(chd, cst, cnf, acdcCnf)
        self.retracking_algorithm = RetrackingAlgorithm(chd, cst, cnf, acdcCnf)

    def __call__(self, surfaceData: SurfaceData,
                 # feedback variables
                 lastSSH = np.nan, lastHs = np.nan,
                 i_track_iter: int = 0):

        # ------------- VARIABLES INITIALIZATION - ---------------------------

        # load the func_f0 values for ACDC in case LUT is used
        LUT_file = open(self.acdcConfig.LUT_f0_path, 'rb')
        func_f0 = np.fromfile(LUT_file, np.double)
        LUT_file.close()


        start_beam = np.where(surfaceData.stack_mask_vector > 1)
        start_beam = (start_beam[0])[0]
        stop_beam = np.where(surfaceData.stack_mask_vector > 1)
        stop_beam = (stop_beam[-1])[-1]
        N_beams_start_stop = stop_beam-start_beam+1
        stop_beam += 1 # Add 1 more to get N_beams_start_stop elements


        if not np.any(surfaceData.waveform_multilooked is not np.nan):
            flag_exit = -1

            acdcObject = ACDCData(waveform=[np.nan] * (self.chd.n_samples_sar*self.cnf.zp_fact_range),
                                ml_wav_fitted_ACDC=[np.nan] * (self.chd.n_samples_sar*self.cnf.zp_fact_range),
                                range_index=[np.nan] * (self.chd.n_samples_sar*self.cnf.zp_fact_range),
                                Hs=np.nan,
                                epoch=np.nan,
                                SSH=np.nan,
                                retracking_cor=np.nan,
                                tracker_range=np.nan,
                                corr_coeff=np.nan,
                                Pu=np.nan,
                                amp_fit=np.nan,
                                sigma0=np.nan,
                                flag_fitting=np.nan,
                                lat_surf=np.nan,
                                lon_surf=np.nan,
                                time_sar_kue=np.nan,
                                alt_rate_sat=np.nan)

            return acdcObject, flag_exit
        else:
            flag_exit = 0

        L1BS = L1BSACDC(
            pri_sar_sat_beam = self.chd.pri_sar,
            alt_sat = surfaceData.alt_sat,
            x_vel_sat = surfaceData.x_vel_sat,
            y_vel_sat = surfaceData.y_vel_sat,
            z_vel_sat = surfaceData.z_vel_sat,
            lat_sat = surfaceData.lat_surf,
            pitch_surf = surfaceData.pitch_sat,
            roll_surf =  surfaceData.roll_sat,
            fs_clock_ku_surf = 1.0/surfaceData.t0_surf,
            start_beam = start_beam,
            stop_beam = stop_beam,
            N_beams_start_stop = N_beams_start_stop)

        # range indexation
        # N_samples_sar corresponds to non-zero padded ones
        if self.acdcConfig.range_index_method == RangeIndexMethod.conventional:
            range_index = np.arange((self.chd.n_samples_sar*self.cnf.zp_fact_range))
            L1BS.delta_range=self.cst.c/(2.0*L1BS.fs_clock_ku_surf*self.cnf.zp_fact_range)
        elif self.acdcConfig.range_index_method == RangeIndexMethod.resampling:
            range_index = np.arange(0.0, (self.chd.n_samples_sar), 1/self.cnf.zp_fact_range)
            L1BS.delta_range=self.cst.c/(2.0*L1BS.fs_clock_ku_surf)

        # --------- Initialization of the non-fitting variables -----------
        nf_p = self.gen_nonfit_params_ACDC(L1BS)

        # ---------------- Stack + mask -------------------------------------------
        # take only those ones within the start and stop
        mask = np.squeeze(surfaceData.stack_mask[L1BS.start_beam:L1BS.stop_beam,:])
        stack = np.squeeze(surfaceData.beams_masked[L1BS.start_beam:L1BS.stop_beam,:])
        #stack = np.matmul(stack,mask)
        stack = stack*mask

        #------------------------- Look indexation --------------------------------
        delta_look_angle=m.asin(self.chd.wv_length_ku/(nf_p.pri_surf*2.0*self.chd.n_ku_pulses_burst*nf_p.v_sat))
        looks = surfaceData.look_angles_surf[L1BS.start_beam:L1BS.stop_beam]
        looks=np.transpose([x / delta_look_angle for x in looks]) #looks indexes

        ## ---------------- Initial Hs & Koff(epoch) -------------------------
        #---------------------------------------------------------------------
        if self.acdcConfig.initial_param_fit_feedback_flag and not np.isnan(lastSSH) and not np.isnan(lastHs):
            # use feedback from "previous"
            retracker_corr=(L1BS.alt_sat-lastSSH-surfaceData.win_delay_surf*self.cst.c/2)
            epoch  =   1.0*retracker_corr/L1BS.delta_range+self.acdcConfig.ref_sample_wd+1
            Hs = lastHs

        else:
            # Use a simple retracker from ML waveforms: peak detector
            fit_data = surfaceData.waveform_multilooked
            fit_data = fit_data / np.max(fit_data)
            peak_pow = np.max(fit_data)
            idx_max_peak = np.argmax(fit_data)
            idx_leading_edge = (np.where(np.where(fit_data <= self.acdcConfig.percent_leading_edge / 100.0 * peak_pow) < idx_max_peak)[-1])[-1]

            if (idx_leading_edge == 0): #isEmpty?
                #if there is no leading edge or the waveform has displaced that
                #much from the window to the left select the peak as leading
                #edge
                idx_leading_edge = idx_max_peak
            epoch = range_index[idx_leading_edge]

            # Use the initial SWH defined in the configuation
            Hs = self.acdcConfig.ini_Hs


        # Amplitude
        A = 1.0;

        ## ------------- ALGORITHMS -----------------------------------------------
        if i_track_iter == 0:
            Num_iterations_over_surface = self.acdcConfig.num_iterations
        else:
            Num_iterations_over_surface = 1

        for i in range(Num_iterations_over_surface):
            ## --------------- Amplitude Compensation ---------------------------------
            #--------------------------------------------------------------------------
            stack_ac, k, l, g = self.amplitude_compensation_algorithm(stack, looks, range_index, nf_p, Hs, epoch)

            ## ---------------- Dilation Compensation ---------------------------------
            #--------------------------------------------------------------------------
            look_indexation_ref=0 #min(looks);
            k_scaled = self.dilation_compensation_algorithm(k, g, nf_p, Hs, look_indexation_ref)

            ## --------------- Retracking ACDC waveform -------------------------------
            #--------------------------------------------------------------------------
            waveform,k_ml_ACDC,estimates,flag,ml_wav_fitted_ACDC,start_sample_fit,stop_sample_fit = self.retracking_algorithm(stack_ac,k_scaled,nf_p,[epoch,Hs,A,0.0],look_indexation_ref,func_f0, mask)

            ## ------------- COMPLETE ACDC OBJECT -------------------------------------
            if flag == -1:
                acdcObject = ACDCData(waveform=[np.nan] * (self.chd.n_samples_sar*self.cnf.zp_fact_range),
                                ml_wav_fitted_ACDC=[np.nan] * (self.chd.n_samples_sar*self.cnf.zp_fact_range),
                                range_index=[np.nan] * (self.chd.n_samples_sar*self.cnf.zp_fact_range),
                                Hs=np.nan,
                                epoch=np.nan,
                                SSH=np.nan,
                                retracking_cor=np.nan,
                                tracker_range=np.nan,
                                corr_coeff=np.nan,
                                Pu=np.nan,
                                amp_fit=np.nan,
                                sigma0=np.nan,
                                flag_fitting=np.nan,
                                lat_surf=np.nan,
                                lon_surf=np.nan,
                                time_sar_kue=np.nan,
                                alt_rate_sat=np.nan)

                flag_exit = -1
                break

            else:
                acdcEpoch = estimates[0]-1
                acdcRetrackingCor = -(self.acdcConfig.ref_sample_wd - acdcEpoch)*L1BS.delta_range
                acdcTrackerRange = surfaceData.win_delay_surf*self.cst.c/2+acdcRetrackingCor

                acdcObject = ACDCData(waveform=waveform[start_sample_fit:stop_sample_fit],
                                ml_wav_fitted_ACDC=ml_wav_fitted_ACDC,
                                range_index=k_ml_ACDC[start_sample_fit:stop_sample_fit],
                                epoch=acdcEpoch,
                                Hs=estimates[1],
                                Pu=estimates[2],
                                amp_fit=10**((estimates[2])/10)/max(waveform),
                                sigma0=estimates[2]+surfaceData.sigma0_scaling_factor,
                                corr_coeff=estimates[3],
                                flag_fitting=estimates[4],
                                lat_surf=surfaceData.lat_surf,
                                lon_surf=surfaceData.lon_surf,
                                time_sar_kue=surfaceData.time_surf,
                                alt_rate_sat=surfaceData.alt_rate_sat,
                                retracking_cor=acdcRetrackingCor,
                                tracker_range=acdcTrackerRange,
                                SSH=surfaceData.alt_sat-acdcTrackerRange)

            epoch = acdcObject.epoch;
            Hs = acdcObject.Hs;

        return acdcObject, flag_exit


    def gen_nonfit_params_ACDC(self, L1BS: L1BSACDC) -> NonFitParams:
        params = {}

        params["pri_surf"] = L1BS.pri_sar_sat_beam
        params["waveskew"] = 0
        params["EMbias"] = 0
        params["rou"] = self.acdcConfig.rou
        params["h"] = L1BS.alt_sat
        params["v_sat"] = np.linalg.norm([L1BS.x_vel_sat,L1BS.y_vel_sat,L1BS.z_vel_sat])

        R_Earth = np.sqrt((self.cst.semi_major_axis**4*m.cos(L1BS.lat_sat*m.pi/180)**2+self.cst.semi_minor_axis**4*m.sin(L1BS.lat_sat*m.pi/180)**2)/((self.cst.semi_major_axis*m.cos(L1BS.lat_sat*m.pi/180))**2+(self.cst.semi_minor_axis*m.sin(L1BS.lat_sat*m.pi/180))**2))
        alpha = 1 + (params["h"])/(R_Earth)

        if self.acdcConfig.mission in ("CS2","CR2"):
             params["xp"] = L1BS.alt_sat*(-1.0*L1BS.pitch_surf)
             params["yp"] = L1BS.alt_sat*(1.0*L1BS.roll_surf)
        elif self.acdcConfig.mission in ("S3","S3_"):
            params["xp"] = L1BS.alt_sat*(1.0*L1BS.pitch_surf)
            params["yp"] = L1BS.alt_sat*(L1BS.roll_surf)
        elif self.acdcConfig. mission in ("S6","S6_"):
            params["xp"] = L1BS.alt_sat*(1.0*L1BS.pitch_surf)
            params["yp"] = L1BS.alt_sat*(L1BS.roll_surf)
        else:
            print("invalid mission code ", self.acdcConfig.mission)

        params["alphax"] = (8*m.log(2))/(L1BS.alt_sat*self.acdcConfig.antenna_beamwidth_along_track_ku)**2
        params["alphay"] = (8*m.log(2))/(L1BS.alt_sat*self.acdcConfig.antenna_beamwidth_across_track_ku)**2

        params["Lx"] = self.cst.c*L1BS.alt_sat/(2*params["v_sat"]*self.chd.freq_ku*self.chd.n_ku_pulses_burst*params["pri_surf"])
        if self.acdcConfig.range_index_method == RangeIndexMethod.conventional:
            params["Ly"] = np.sqrt(self.cst.c*L1BS.alt_sat/(alpha*L1BS.fs_clock_ku_surf*self.cnf.zp_fact_range))
            params["Lz"] = 0.5*self.cst.c/(L1BS.fs_clock_ku_surf*self.cnf.zp_fact_range)
        elif self.acdcConfig.range_index_method == RangeIndexMethod.resampling:
            params["Ly"] = np.sqrt(self.cst.c*L1BS.alt_sat/(alpha*L1BS.fs_clock_ku_surf))
            params["Lz"] = 0.5*self.cst.c/(L1BS.fs_clock_ku_surf)

        params["Neff"]=L1BS.N_beams_start_stop

        if self.acdcConfig.window_type_a == AzimuthWindowingMethod.boxcar:
            A_s2Ga_chd = 1.0196
            alpha_ga_chd = 1.0/(2*(0.36012)**2)
        elif self.acdcConfig.window_type_a == AzimuthWindowingMethod.hanning:
            A_s2Ga_chd = 1.0101
            alpha_ga_chd = 1.0/(2*(0.59824)**2)
        elif self.acdcConfig.window_type_a == AzimuthWindowingMethod.hamming:
            A_s2Ga_chd = 1.0081
            alpha_ga_chd = 1.0/(2.0*(0.54351)**2)
        elif self.acdcConfig.window_type_a == AzimuthWindowingMethod.disabled:
            A_s2Ga_chd = 1.0
            alpha_ga_chd = 1.0/(2.0*(self.acdcConfig.window_a_fixed_value)**2)
        else:
            print("invalid window type a. Chose hamming, hanning, boxcar or none")


        if self.acdcConfig.window_type_r == AzimuthWindowingMethod.boxcar:
            A_s2Gr_chd = 1.0196
            alpha_gr_chd = 1.0/(2*(0.36012)**2)
        elif self.acdcConfig.window_type_r == AzimuthWindowingMethod.hanning:
            A_s2Gr_chd = 1.0101
            alpha_gr_chd = 1.0/(2*(0.59824)**2)
        elif self.acdcConfig.window_type_r == AzimuthWindowingMethod.hamming:
            A_s2Gr_chd = 1.0081
            alpha_gr_chd = 1.0/(2.0*(0.54351)**2)
        elif self.acdcConfig.window_type_r == AzimuthWindowingMethod.disabled:
            A_s2Gr_chd = 1.0
            alpha_gr_chd = 1.0/(2.0*(self.acdcConfig.window_r_fixed_value)**2)
        else:
            print("invalid window type r. Chose hamming, hanning, boxcar or none")

        params["Npulses"] = self.chd.n_ku_pulses_burst
        params["alphag_a"] = alpha_ga_chd
        params["alphag_r"] = alpha_gr_chd
        params["A_s2Ga"] = A_s2Ga_chd
        params["A_s2Gr"] = A_s2Gr_chd
        params["bw_Rx"] = self.chd.bw_ku

        return NonFitParams(params)


