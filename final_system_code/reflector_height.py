# ~ def reflector_height(filename, az1, az2, elev1, elev2, temporal_res):
    # ~ # Determine reflector height code
    # ~ # Author: Max Feinland, Sasha Gladkova, Claire Wadman et al. (who else?)
    # ~ # Date created: 11/15/23
    # ~ # Last modified: 4/9/2024
    # ~ # Purpose: to adapt Kristine Larson's code and use a GNSS receiver to
    # ~ # determine water level heights.
    
    # ~ # Importin' the stuff
    # ~ import numpy as np
    # ~ # import matplotlib.pyplot as plt
    # ~ from scipy.optimize import curve_fit
    # ~ from scipy.signal import find_peaks, peak_widths
    # ~ import pandas as pd
    # ~ import time
    # ~ import warnings
    # ~ warnings.simplefilter('ignore', np.RankWarning)
    
    # ~ def dyn_corr(hs, ts, es):
        # ~ # inputs arguments: heights, times, and elevaton angles from user specified data collection period
        # ~ # (unevenly sampled and not always same length)

        # ~ # we're going to not use the first and last data points
        # ~ length = len(ts) - 2 # this yields a problem if there are <= 2 points
        # ~ # initialize size of A matrix
        # ~ A = np.empty([length,2]) # default type float64
        # ~ print("A = ", A)
        # ~ # initialize
        # ~ e_dots = []
        # ~ # change from degrees to radians
        # ~ for e in es:
            # ~ e = e*(np.pi/180)
        # ~ # go through all data points
        # ~ for n in range(length):
            # ~ point = n + 1
            # ~ dt = np.absolute(ts[point+1] - ts[point]) # dt is the sampling frequency
            # ~ e_dots.append((es[point+1]-es[point-1])/(2*dt)) # numerical differentiation to get time rate of change of e
            # ~ A[n][0] = 1
            # ~ A[n][1] = (np.tan(es[point]))/(e_dots[n]) # E_DOT IS IN RAD/SEC
        # ~ hs = hs[1:len(hs)-1]
        # ~ inf_indices = np.where(np.isinf(A).any(axis=1))[0]

        # ~ A = A[~np.isinf(A).any(axis=1)]
        # ~ hs = [hs[i] for i in range(len(hs)) if i not in inf_indices]
        # ~ try:
            # ~ H_array, residuals, rank, singular_values  = np.linalg.lstsq(A, hs, rcond=None)
        # ~ except:
            # ~ H_array = None
        # ~ return H_array[0] # second value is rate of change of H, which we don't care about

    # ~ # Function definitions
    # ~ def peak2noise(f, p, frange):
        # ~ frange_indices = np.where((f >= frange[0]) & (f <= frange[1]))[0]
        # ~ peak_indices = np.argmax(p[frange_indices])
        # ~ peak_indices = [int(peak_indices)]
        # ~ peak_freq = f[frange_indices][peak_indices]
        # ~ max_amp = p[frange_indices][peak_indices]
        # ~ w = peak_widths(p, peak_indices)
        # ~ w = w[0][0]

        # ~ prange = np.ptp(p)
        # ~ significant_pks, _ = find_peaks(p, prominence=prange*0.5)
        # ~ other_pks, _ = find_peaks(p)
        # ~ num_significant_pks = len(significant_pks)
        # ~ other_pks_hght = p[other_pks]
        # ~ noise = np.nanmean(other_pks_hght)
        # ~ pknoise = max_amp / noise
        # ~ return peak_freq, max_amp, pknoise, num_significant_pks, w

    # ~ def get_ofac_hifac(elev_angles, cf, max_h, desired_precision):
        # ~ X = np.sin(np.radians(elev_angles)) / cf
        # ~ N = len(X)
        # ~ W = np.max(X) - np.min(X)
        # ~ characteristic_peak_width = 1 / W
        # ~ ofac = characteristic_peak_width / desired_precision
        # ~ fc = N / (2 * W)
        # ~ hifac = max_h / fc
        # ~ return ofac, hifac

    # ~ def lomb(t, h, ofac, hifac): # lomb-scargle periodogram
        # ~ N = len(h) # number of samples
        # ~ T = np.max(t) - np.min(t) # time span
        # ~ mu = np.mean(h) # mean
        # ~ s2 = np.var(h) # variance

        # ~ f = np.arange(1/(T*ofac), hifac*N/(2*T), 1/(T*ofac)) # sampling frequencies
        # ~ # Calculate angular frequencies for each time point
        # ~ w = 2*np.pi*f

        # ~ t_reshaped = t.reshape(-1, 1)
        # ~ # Calculate constant offsets
        # ~ tau = np.arctan2(np.sum(np.sin(2*w*t_reshaped), axis=0),
                         # ~ np.sum(np.cos(2*w*t_reshaped), axis=0)) / (2*w)

        # ~ # Spectral power
        # ~ cterm = np.cos(w.reshape(-1, 1) * t - w.reshape(-1, 1) * tau.reshape(-1, 1))
        # ~ sterm = np.sin(w.reshape(-1, 1) * t - w.reshape(-1, 1) * tau.reshape(-1, 1))
        # ~ P = (np.sum(cterm*(h - mu), axis=1)**2 / np.sum(cterm**2, axis=1) +
             # ~ np.sum(sterm*(h - mu), axis=1)**2 / np.sum(sterm**2, axis=1)) / (2*s2)
        # ~ P = 2 * np.sqrt(s2 * P / N)  # amplitude

        # ~ return f, P

    # ~ def single_arc_analysis(t, elev, az, snr, hifielev, indices):
        # ~ # Inputs: all are self-explanatory except hifielev (should be polynomial fit elevation)
        # ~ # and indices is either ok_indices, ok_indices_rising, or ok_indices_falling
        # ~ # Once you have zoomed in on a single arc, you can run analysis on it 
        # ~ # to determine reflector height.
        # ~ ediff_r = np.ptp(elev[indices]) # range of elevation angles
        # ~ conditions = [ediff_r > ediff_threshold,
            # ~ len(np.unique(elev[indices])) > 5,
            # ~ len(np.unique(snr[indices])) > 5,
            # ~ len(t[indices]) > 100]
        # ~ # conditions: length of vector t is long enough, and there are enough unique values 
        # ~ # in elevation & snr
        # ~ if all(conditions):
            # ~ t = t[indices]
            # ~ elev = elev[indices]
            # ~ az = az[indices]
            # ~ snr = snr[indices]
            # ~ hifielev = hifielev[indices]

            # ~ sine = np.sin(np.radians(hifielev))

            # ~ linearsnr = 10**(snr/20)
            # ~ idx = np.isfinite(sine) & np.isfinite(linearsnr)
            # ~ if len(sine[idx]) > 0:
                # ~ p1 = np.polyfit(sine[idx], linearsnr[idx], 6)
                # ~ linearsnr = linearsnr - sine**6 * p1[0] - sine**5 * p1[1] - sine**4 * p1[2] \
                    # ~ - sine**3 * p1[3] - sine**2 * p1[4] - sine * p1[5] - p1[6]
                # ~ sine = sine[idx]
                # ~ linearsnr = linearsnr[idx]

                # ~ cf = 0.1902936 / 2
                # ~ sorted_indices = np.argsort(sine)
                # ~ sortedX = sine[sorted_indices]
                # ~ sortedY = linearsnr[sorted_indices]

                # ~ ofac, hifac = get_ofac_hifac(hifielev, cf, 5, 0.005)
                # ~ f, p2 = lomb(sortedX / cf, sortedY, ofac, hifac)
                # ~ lambda_val = 3e8 / 1575.42e6

# ~ #                 # Uncomment if you want to see the periodogram
                # ~ frange = [0, 5]
                # ~ maxRH, maxRHAmp, pknoise, num_s_pks, w = peak2noise(f, p2, frange)

                # ~ assigned_t = t[len(t)//2] ### at this point we assign a t using its midpoint
                # ~ assigned_elev = elev[len(elev)//2]
                # ~ if (pknoise > 2.5) & (num_s_pks < 2) & (w < 120):
                    # ~ pass
                # ~ else:
                    # ~ maxRH = assigned_t = assigned_elev = None
            # ~ else:
                # ~ maxRH = assigned_t = assigned_elev = None
        # ~ else:
            # ~ maxRH = assigned_t = assigned_elev = None
        # ~ return maxRH, assigned_t, assigned_elev

            
    # ~ ## BEGIN MAIN SCRIPT
    # ~ dino = pd.read_csv(filename) # This can be changed if we're not reading/writing .csv, but rather DataFrame

    # ~ # Extract data from dino file
    # ~ t = np.array(dino.t)
    
    # ~ # in case you end up passing a UTC day
    # ~ overflow_index = np.where(np.diff(t) < 0)[0]
    # ~ # Add 86400 to all elements from the overflow index onward
    # ~ if len(overflow_index) > 0:
        # ~ overflow_index = overflow_index[0]  # Take the first overflow index
        # ~ t[overflow_index + 1:] += 86400

    # ~ prn = np.array(dino.prn)
    # ~ elev = np.array(dino.elev)
    # ~ az = np.array(dino.az)
    # ~ snr = np.array(dino.snr)
    # ~ const = np.array(dino.const)
    
    # ~ corr_times = []
    # ~ corr_elevs = []
    # ~ reflH_from_each_arc = []

    # ~ # housekeeping/quality control
    # ~ ediff_threshold = 2

    # ~ total_prns = np.unique(prn)
    # ~ reflH = []

    # ~ list_of_constellations = np.unique(dino.const)
    
    # ~ split_idx = [0]
    
    # ~ # splitting up into multiple segments based on temporal resolution
    # ~ seconds_in_one_segment = 60.*90./temporal_res
    # ~ # print(seconds_in_one_segment)

    # ~ try:
        # ~ number_of_intervals = int(np.ceil(float(np.ptp(t))/seconds_in_one_segment))
        # ~ time_diff = np.diff(t) # calculate the time differences between consecutive elements
        # ~ cumulative_time_diff = np.cumsum(time_diff)
        # ~ for i in range(number_of_intervals-1):
            # ~ indices_that_are_after_the_split = np.where(cumulative_time_diff >= seconds_in_one_segment*(i+1))[0][0]
            # ~ if 'indices_that_are_after_the_split' in locals():
                # ~ split_idx.append(indices_that_are_after_the_split)
        # ~ # If the last segment is shorter than 1080 seconds, add the last index
        # ~ if cumulative_time_diff[-1] % seconds_in_one_segment != 0:
            # ~ split_idx = np.append(split_idx, len(t) - 1)
    # ~ except ValueError:
        # ~ split_idx = []

    # ~ for j in range(len(split_idx)-1):
        # ~ reflH_for_subdivision = []
        # ~ t2 = t[split_idx[j]:split_idx[j+1]]
        # ~ prn_n = prn[split_idx[j]:split_idx[j+1]]
        # ~ elev_n = elev[split_idx[j]:split_idx[j+1]]
        # ~ az_n = az[split_idx[j]:split_idx[j+1]]
        # ~ snr_n = snr[split_idx[j]:split_idx[j+1]]
        # ~ const_n = const[split_idx[j]:split_idx[j+1]]
        # ~ for current_constellation in list_of_constellations:
            # ~ for idx in total_prns:
                # ~ indices_ofcurrentprn = np.where((prn_n == idx) & (const_n == current_constellation))
                # ~ myprn = idx

                # ~ current_t = t2[indices_ofcurrentprn]
                # ~ current_elev = elev_n[indices_ofcurrentprn]
                # ~ current_snr = snr_n[indices_ofcurrentprn]
                # ~ current_az = az_n[indices_ofcurrentprn]

                # ~ tdiff = np.diff(current_t)
                # ~ separate_arcs = np.concatenate(([0], np.where(tdiff > 20)[0], [len(current_t)]))
                # ~ arcs = []

                # ~ for k in range(len(separate_arcs) - 1):
                    # ~ arcs.append(np.arange(separate_arcs[k], separate_arcs[k + 1]))

                    # ~ current_arc_t = current_t[arcs[k]]
                    # ~ current_arc_elev = current_elev[arcs[k]]
                    # ~ current_arc_snr = current_snr[arcs[k]]
                    # ~ current_arc_az = current_az[arcs[k]]

                    # ~ if len(current_arc_t) > 0:
                        # ~ p = np.polyfit(current_arc_t, current_arc_elev, 6) # improved polyfit to 6th order (thanks sasha)
                        # ~ hifielev = current_arc_t**6*p[0]  +  current_arc_t**5*p[1]  + \
                        # ~ current_arc_t**4*p[2]  +  current_arc_t**3*p[3]  +  current_arc_t**2*p[4]  + \
                        # ~ current_arc_t*p[5]  +  p[6]

                        # ~ current_arc_az = np.array(current_arc_az)

                        # ~ ok_indices = np.where(
                            # ~ (current_arc_elev >= elev1) & (current_arc_elev <= elev2) &
                            # ~ (current_arc_az >= az1) & (current_arc_az <= az2))[0]

                        # ~ # Split up ok_indices into rising and falling arcs, if applicable.
                        # ~ rising_arc = np.where(np.diff(ok_indices) > 5)
                        # ~ if (rising_arc[0]).size > 0:
                            # ~ ok_indices_rising = ok_indices[0:rising_arc[0][0]]
                            # ~ ok_indices_falling = ok_indices[rising_arc[0][0]+1:]
                            # ~ if len(ok_indices_rising) > 0:
                                # ~ hght_rising, use_t_corr1, use_elev_corr1 = single_arc_analysis(current_arc_t, current_arc_elev, current_arc_az,
                                              # ~ current_arc_snr, hifielev, ok_indices_rising)

                                # ~ if hght_rising is not None:
                                    # ~ # print("myprn = ", myprn, "hght_rising = ", hght_rising)
                                    # ~ reflH_for_subdivision.append(hght_rising)
                                    # ~ reflH_from_each_arc.append(hght_rising)
                                    # ~ corr_times.append(use_t_corr1)
                                    # ~ corr_elevs.append(use_elev_corr1)

                            # ~ if len(ok_indices_falling) > 0:
                                # ~ hght_falling, use_t_corr2, use_elev_corr2 = single_arc_analysis(current_arc_t, current_arc_elev, current_arc_az,
                                              # ~ current_arc_snr, hifielev, ok_indices_falling)
                                # ~ if hght_falling is not None:
                                    # ~ # print("myprn = ", myprn, "hght_falling = ", hght_falling)
                                    # ~ reflH_for_subdivision.append(hght_falling)
                                    # ~ reflH_from_each_arc.append(hght_falling)
                                    # ~ corr_times.append(use_t_corr2)
                                    # ~ corr_elevs.append(use_elev_corr2)

                        # ~ elif len(ok_indices) > 0:
                            # ~ hght, use_t_corr3, use_elev_corr3  = single_arc_analysis(current_arc_t, current_arc_elev, current_arc_az,
                                          # ~ current_arc_snr, hifielev, ok_indices)
                            # ~ if hght is not None:
                                # ~ # print("myprn = ", myprn, "hght = ", hght)
                                # ~ reflH_for_subdivision.append(hght)
                                # ~ reflH_from_each_arc.append(hght)
                                # ~ corr_times.append(use_t_corr3)
                                # ~ corr_elevs.append(use_elev_corr3)
        # ~ if len(reflH_for_subdivision) > 0:
             # ~ # reflH_dyncorr = dyn_corr(reflH_from_each_arc, corr_times, corr_elevs)
             # ~ reflH.append(np.nanmean(reflH_for_subdivision)) # average reflector height for given subdivision
        # ~ else:
             # ~ reflH_dyncorr = None
             # ~ reflH.append(None)
    # ~ # print("reflH_from_each_arc = ", reflH_from_each_arc)  
    # ~ return reflH
    # ~ # not doing dyn corr for now
    # ~ #return reflH, reflH_dyncorr
def reflector_height(filename, az1, az2, elev1, elev2, temporal_res):
    # Determine reflector height code
    # Author: Max Feinland, Sasha Gladkova, Claire Wadman et al. (who else?)
    # Date created: 11/15/23
    # Last modified: 4/16/2024
    # Purpose: to adapt Kristine Larson's code and use a GNSS receiver to
    # determine water level heights.
    
    # Importin' the stuff
    import numpy as np
    # import matplotlib.pyplot as plt
    from scipy.optimize import curve_fit
    from scipy.signal import find_peaks, peak_widths
    import pandas as pd
    import time
    import warnings
    warnings.simplefilter('ignore', np.RankWarning)
    
    def dyn_corr(hs, ts, es):
        # inputs arguments: heights, times, and elevaton angles from user specified data collection period
        # (unevenly sampled and not always same length)

        # we're going to not use the first and last data points
        length = len(ts) - 2 # this yields a problem if there are <= 2 points
        # initialize size of A matrix
        A = np.empty([length,2]) # default type float64
        print("A = ", A)
        # initialize
        e_dots = []
        # change from degrees to radians
        for e in es:
            e = e*(np.pi/180)
        # go through all data points
        for n in range(length):
            point = n + 1
            dt = np.absolute(ts[point+1] - ts[point]) # dt is the sampling frequency
            e_dots.append((es[point+1]-es[point-1])/(2*dt)) # numerical differentiation to get time rate of change of e
            A[n][0] = 1
            A[n][1] = (np.tan(es[point]))/(e_dots[n]) # E_DOT IS IN RAD/SEC
        hs = hs[1:len(hs)-1]
        inf_indices = np.where(np.isinf(A).any(axis=1))[0]

        A = A[~np.isinf(A).any(axis=1)]
        hs = [hs[i] for i in range(len(hs)) if i not in inf_indices]
        try:
            H_array, residuals, rank, singular_values  = np.linalg.lstsq(A, hs, rcond=None)
        except:
            H_array = None
        return H_array[0] # second value is rate of change of H, which we don't care about

    # Function definitions
    def get_cf(const):
        beidou = 1575.42E6 # this one could also be on L5... but less likely
        glonass = 1575.42E6
        galileo = 1176.45E6 # this one could also be on L1 (~equally likely)
        gps = 1575.42E6  # this one could also be on L5... but less likely
        switcher = {
            "GB": beidou,
            "GA": galileo,
            "GP": gps,
            "GL": glonass,
        }
        return switcher.get(const, gps)
        
    def peak2noise(f, p, frange):
        frange_indices = np.where((f >= frange[0]) & (f <= frange[1]))[0]
        peak_indices = np.argmax(p[frange_indices])
        peak_indices = [int(peak_indices)]
        peak_freq = f[frange_indices][peak_indices]
        max_amp = p[frange_indices][peak_indices]
        w = peak_widths(p, peak_indices)
        w = w[0][0]

        prange = np.ptp(p)
        significant_pks, _ = find_peaks(p, prominence=prange*0.5)
        other_pks, _ = find_peaks(p)
        num_significant_pks = len(significant_pks)
        other_pks_hght = p[other_pks]
        noise = np.nanmean(other_pks_hght)
        pknoise = max_amp / noise
        return peak_freq, max_amp, pknoise, num_significant_pks, w

    def get_ofac_hifac(elev_angles, cf, max_h, desired_precision):
        X = np.sin(np.radians(elev_angles)) / cf
        N = len(X)
        W = np.max(X) - np.min(X)
        characteristic_peak_width = 1 / W
        ofac = characteristic_peak_width / desired_precision
        fc = N / (2 * W)
        hifac = max_h / fc
        return ofac, hifac

    def lomb(t, h, ofac, hifac): # lomb-scargle periodogram
        N = len(h) # number of samples
        T = np.max(t) - np.min(t) # time span
        mu = np.mean(h) # mean
        s2 = np.var(h) # variance

        f = np.arange(1/(T*ofac), hifac*N/(2*T), 1/(T*ofac)) # sampling frequencies
        # Calculate angular frequencies for each time point
        w = 2*np.pi*f

        t_reshaped = t.reshape(-1, 1)
        # Calculate constant offsets
        tau = np.arctan2(np.sum(np.sin(2*w*t_reshaped), axis=0),
                         np.sum(np.cos(2*w*t_reshaped), axis=0)) / (2*w)

        # Spectral power
        cterm = np.cos(w.reshape(-1, 1) * t - w.reshape(-1, 1) * tau.reshape(-1, 1))
        sterm = np.sin(w.reshape(-1, 1) * t - w.reshape(-1, 1) * tau.reshape(-1, 1))
        P = (np.sum(cterm*(h - mu), axis=1)**2 / np.sum(cterm**2, axis=1) +
             np.sum(sterm*(h - mu), axis=1)**2 / np.sum(sterm**2, axis=1)) / (2*s2)
        P = 2 * np.sqrt(s2 * P / N)  # amplitude

        return f, P

    def single_arc_analysis(t, elev, az, snr, hifielev, indices, const):
        # Inputs: all are self-explanatory except hifielev (should be polynomial fit elevation)
        # and indices is either ok_indices, ok_indices_rising, or ok_indices_falling
        # Once you have zoomed in on a single arc, you can run analysis on it 
        # to determine reflector height.
        ediff_r = np.ptp(elev[indices]) # range of elevation angles
        conditions = [ediff_r > ediff_threshold,
            len(np.unique(elev[indices])) > 5,
            len(np.unique(snr[indices])) > 5,
            len(t[indices]) > 100]
        # conditions: length of vector t is long enough, and there are enough unique values 
        # in elevation & snr
        if all(conditions):
            t = t[indices]
            elev = elev[indices]
            az = az[indices]
            snr = snr[indices]
            hifielev = hifielev[indices]

            sine = np.sin(np.radians(hifielev))

            linearsnr = 10**(snr/20)
            idx = np.isfinite(sine) & np.isfinite(linearsnr)
            if len(sine[idx]) > 0:
                p1 = np.polyfit(sine[idx], linearsnr[idx], 6)
                linearsnr = linearsnr - sine**6 * p1[0] - sine**5 * p1[1] - sine**4 * p1[2] \
                    - sine**3 * p1[3] - sine**2 * p1[4] - sine * p1[5] - p1[6]
                sine = sine[idx]
                linearsnr = linearsnr[idx]

                # cf = 0.1902936 / 2
                cf = get_cf(const)
                c_f_wl = 3e8/(2*cf)
                sorted_indices = np.argsort(sine)
                sortedX = sine[sorted_indices]
                sortedY = linearsnr[sorted_indices]

                ofac, hifac = get_ofac_hifac(hifielev, c_f_wl, 5, 0.005)
                f, p2 = lomb(sortedX / c_f_wl, sortedY, ofac, hifac)
                lambda_val = 3e8 / c_f_wl

#                 # Uncomment if you want to see the periodogram
                frange = [0, 5]
                maxRH, maxRHAmp, pknoise, num_s_pks, w = peak2noise(f, p2, frange)

                assigned_t = t[len(t)//2] ### at this point we assign a t using its midpoint
                assigned_elev = elev[len(elev)//2]
                if (pknoise > 2.5) & (num_s_pks < 2) & (w < 120):
                    pass
                else:
                    maxRH = assigned_t = assigned_elev = None
            else:
                maxRH = assigned_t = assigned_elev = None
        else:
            maxRH = assigned_t = assigned_elev = None
        return maxRH, assigned_t, assigned_elev

            
    ## BEGIN MAIN SCRIPT
    dino = pd.read_csv(filename) # This can be changed if we're not reading/writing .csv, but rather DataFrame

    # Extract data from dino file
    t = np.array(dino.t)
    
    # in case you end up passing a UTC day
    overflow_index = np.where(np.diff(t) < 0)[0]
    # Add 86400 to all elements from the overflow index onward
    if len(overflow_index) > 0:
        overflow_index = overflow_index[0]  # Take the first overflow index
        t[overflow_index + 1:] += 86400

    prn = np.array(dino.prn)
    elev = np.array(dino.elev)
    az = np.array(dino.az)
    snr = np.array(dino.snr)
    const = np.array(dino.const)
    
    corr_times = []
    corr_elevs = []
    reflH_from_each_arc = []

    # housekeeping/quality control
    ediff_threshold = 2

    total_prns = np.unique(prn)
    reflH = []

    list_of_constellations = np.unique(dino.const)
    
    split_idx = [0]
    
    # splitting up into multiple segments based on temporal resolution
    seconds_in_one_segment = 60.*90./temporal_res
    # print(seconds_in_one_segment)

    try:
        number_of_intervals = int(np.ceil(float(np.ptp(t))/seconds_in_one_segment))
        time_diff = np.diff(t) # calculate the time differences between consecutive elements
        cumulative_time_diff = np.cumsum(time_diff)
        for i in range(number_of_intervals-1):
            indices_that_are_after_the_split = np.where(cumulative_time_diff >= seconds_in_one_segment*(i+1))[0][0]
            if 'indices_that_are_after_the_split' in locals():
                split_idx.append(indices_that_are_after_the_split)
        # If the last segment is shorter than 1080 seconds, add the last index
        if cumulative_time_diff[-1] % seconds_in_one_segment != 0:
            split_idx = np.append(split_idx, len(t) - 1)
    except ValueError:
        split_idx = []

    for j in range(len(split_idx)-1):
        reflH_for_subdivision = []
        t2 = t[split_idx[j]:split_idx[j+1]]
        prn_n = prn[split_idx[j]:split_idx[j+1]]
        elev_n = elev[split_idx[j]:split_idx[j+1]]
        az_n = az[split_idx[j]:split_idx[j+1]]
        snr_n = snr[split_idx[j]:split_idx[j+1]]
        const_n = const[split_idx[j]:split_idx[j+1]]
        for current_constellation in list_of_constellations:
            for idx in total_prns:
                indices_ofcurrentprn = np.where((prn_n == idx) & (const_n == current_constellation))
                myprn = idx

                current_t = t2[indices_ofcurrentprn]
                current_elev = elev_n[indices_ofcurrentprn]
                current_snr = snr_n[indices_ofcurrentprn]
                current_az = az_n[indices_ofcurrentprn]

                tdiff = np.diff(current_t)
                separate_arcs = np.concatenate(([0], np.where(tdiff > 20)[0], [len(current_t)]))
                arcs = []

                for k in range(len(separate_arcs) - 1):
                    arcs.append(np.arange(separate_arcs[k], separate_arcs[k + 1]))

                    current_arc_t = current_t[arcs[k]]
                    current_arc_elev = current_elev[arcs[k]]
                    current_arc_snr = current_snr[arcs[k]]
                    current_arc_az = current_az[arcs[k]]

                    if len(current_arc_t) > 0:
                        p = np.polyfit(current_arc_t, current_arc_elev, 6) # improved polyfit to 6th order (thanks sasha)
                        hifielev = current_arc_t**6*p[0]  +  current_arc_t**5*p[1]  + \
                        current_arc_t**4*p[2]  +  current_arc_t**3*p[3]  +  current_arc_t**2*p[4]  + \
                        current_arc_t*p[5]  +  p[6]

                        current_arc_az = np.array(current_arc_az)

                        ok_indices = np.where(
                            (current_arc_elev >= elev1) & (current_arc_elev <= elev2) &
                            (current_arc_az >= az1) & (current_arc_az <= az2))[0]

                        # Split up ok_indices into rising and falling arcs, if applicable.
                        rising_arc = np.where(np.diff(ok_indices) > 5)
                        if (rising_arc[0]).size > 0:
                            ok_indices_rising = ok_indices[0:rising_arc[0][0]]
                            ok_indices_falling = ok_indices[rising_arc[0][0]+1:]
                            if len(ok_indices_rising) > 0:
                                hght_rising, use_t_corr1, use_elev_corr1 = single_arc_analysis(current_arc_t, current_arc_elev, current_arc_az,
                                              current_arc_snr, hifielev, ok_indices_rising, current_constellation)

                                if hght_rising is not None:
                                    # print("myprn = ", myprn, "hght_rising = ", hght_rising)
                                    reflH_for_subdivision.append(hght_rising)
                                    reflH_from_each_arc.append(hght_rising)
                                    corr_times.append(use_t_corr1)
                                    corr_elevs.append(use_elev_corr1)

                            if len(ok_indices_falling) > 0:
                                hght_falling, use_t_corr2, use_elev_corr2 = single_arc_analysis(current_arc_t, current_arc_elev, current_arc_az,
                                              current_arc_snr, hifielev, ok_indices_falling, current_constellation)
                                if hght_falling is not None:
                                    # print("myprn = ", myprn, "hght_falling = ", hght_falling)
                                    reflH_for_subdivision.append(hght_falling)
                                    reflH_from_each_arc.append(hght_falling)
                                    corr_times.append(use_t_corr2)
                                    corr_elevs.append(use_elev_corr2)

                        elif len(ok_indices) > 0:
                            hght, use_t_corr3, use_elev_corr3  = single_arc_analysis(current_arc_t, current_arc_elev, current_arc_az,
                                          current_arc_snr, hifielev, ok_indices, current_constellation)
                            if hght is not None:
                                # print("myprn = ", myprn, "hght = ", hght)
                                reflH_for_subdivision.append(hght)
                                reflH_from_each_arc.append(hght)
                                corr_times.append(use_t_corr3)
                                corr_elevs.append(use_elev_corr3)
        if len(reflH_for_subdivision) > 0:
             # reflH_dyncorr = dyn_corr(reflH_from_each_arc, corr_times, corr_elevs)
            cur_reflH = np.round(np.nanmean(reflH_for_subdivision), 2)
            reflH.append(cur_reflH) # average reflector height for given subdivision
        else:
            reflH_dyncorr = None
            reflH.append(None)
    # print("reflH_from_each_arc = ", reflH_from_each_arc)  
    return reflH
    # not doing dyn corr for now
    #return reflH, reflH_dyncorr
