#!/usr/bin/env python
# coding: utf-8

def dyn_corr(hs, ts, es):
    import numpy as np
    # inputs arguments: heights, times, and elevaton angles from user specified data collection period
    # (unevenly sampled and not always same length)

    # we're going to not use the first and last data points

    length = len(ts) - 2
    # initialize size of A matrix
    A = np.empty([length,2]) # default type float64
    # initialize
    e_dots = []
    # go through all data points
    for n in range(length):
        point = n + 1
        dt = ts[point+1] - ts[point] # dt is the sampling frequency
        e_dots.append((es[point+1]-es[point-1])/(2*dt)) # numerical differentiation to get time rate of change of e
        A[n][0] = 1
        A[n][1] = (np.tan(es[point]))/np.degrees(e_dots[n]) # ASSUMING THAT E_DOT IS IN RADS/TIME, this turns it into degrees
    hs = hs[1:len(hs)-1]
    H_array, residuals, rank, singular_values = np.linalg.lstsq(A, hs, rcond=None)
    return H_array


def reflector_height(filename, az1, az2, elev1, elev2):
    # Determine reflector height code
    # Author: Max Feinland
    # Date created: 11/15/23
    # Last modified: 2/19/2024
    # Purpose: to adapt Kristine Larson's code and use a GNSS receiver to
    # determine water level heights.
    
    # Importin' the stuff
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.optimize import curve_fit
    import pandas as pd
    import time

    # Function definitions
    def peak2noise(f, p, frange):
        frange_indices = np.where((f >= frange[0]) & (f <= frange[1]))
        peak_indices = np.argmax(p[frange_indices])
        peak_freq = f[frange_indices][peak_indices]
        max_amp = p[frange_indices][peak_indices]

        # Estimate peak-to-noise ratio
        noise_indices = np.setdiff1d(np.arange(len(frange_indices)), peak_indices)
        noise_std = np.std(p[frange_indices][noise_indices])
        pknoise = max_amp / noise_std
        return peak_freq, max_amp, pknoise

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

    def single_arc_analysis(t, elev, az, snr, hifielev, indices):
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

                cf = 0.1902936 / 2
                sorted_indices = np.argsort(sine)
                sortedX = sine[sorted_indices]
                sortedY = linearsnr[sorted_indices]

                ofac, hifac = get_ofac_hifac(hifielev, cf, 15, 0.005)
                f, p2 = lomb(sortedX / cf, sortedY, ofac, hifac)
                lambda_val = 3e8 / 1575.42e6

                # Uncomment if you want to see the periodogram
#                 dispname = f"PRN-{myprn}, arc {k}"
#                 plt.plot(f, p2, linewidth=2, label=dispname)
#                 plt.xlim([0, 15])
#                 plt.xlabel('Reflector Height (m)')
#                 plt.ylabel('Amplitude')
#                 plt.legend()
#                 plt.grid(True)
#                 plt.title('Lomb-Scargle Periodogram')

                frange = [0, 15]
                maxRH, maxRHAmp, pknoise = peak2noise(f, p2, frange)
                assigned_t = t[len(t)//2] ### at this point we assign a t using its midpoint
                assigned_elev = elev[len(elev)//2]
                return maxRH, assigned_t, assigned_elev

    dino = pd.read_csv(filename) # This can be changed if we're not reading/writing .csv, but rather DataFrame

    # Extract data from dino file
    t = np.array(dino.t)
    prn = np.array(dino.prn)
    elev = np.array(dino.elev)
    az = np.array(dino.az)
    snr = np.array(dino.snr)
    corr_times = []
    corr_elevs = []

    # housekeeping/quality control
    ediff_threshold = 5

    total_prns = np.unique(prn)
    reflH = []

    for idx in total_prns:
        indices_ofcurrentprn = np.where(prn == idx)
        myprn = idx

        current_t = t[indices_ofcurrentprn]
        current_elev = elev[indices_ofcurrentprn]
        current_snr = snr[indices_ofcurrentprn]
        current_az = az[indices_ofcurrentprn]

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
                    hght_rising, use_t_corr1, use_elev_corr1 = single_arc_analysis(current_arc_t, current_arc_elev, current_arc_az,
                                      current_arc_snr, hifielev, ok_indices_rising)
                    if hght_rising is not None:
                        reflH.append(hght_rising)
                        corr_times.append(use_t_corr1)
                        corr_elevs.append(use_elev_corr1)
                        
                    hght_falling, use_t_corr2, use_elev_corr2 = single_arc_analysis(current_arc_t, current_arc_elev, current_arc_az,
                                      current_arc_snr, hifielev, ok_indices_falling)
                    if hght_falling is not None:
                        reflH.append(hght_falling)
                        corr_times.append(use_t_corr2)
                        corr_elevs.append(use_elev_corr2)
                        
                elif len(ok_indices) > 0:
                    hght, use_t_corr3, use_elev_corr3  = single_arc_analysis(current_arc_t, current_arc_elev, current_arc_az,
                                      current_arc_snr, hifielev, ok_indices)
                    if hght is not None:
                        reflH.append(hght)
                        corr_times.append(use_t_corr3)
                        corr_elevs.append(use_elev_corr3)

    #Apply dynamic height
    # print("length of times: ")
    # print(np.shape(corr_times))
    # print("\nlength of elevs: ")
    # print(np.shape(corr_elevs))
    reflH_corrected = dyn_corr(reflH, corr_times, corr_elevs)

    return reflH_corrected

# Uncomment if you wanna run it
reflH_outfput = reflector_height("wesl_dino.csv",265, 330, 5, 20)
