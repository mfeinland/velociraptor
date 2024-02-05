#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd
import time

# import warnings
# warnings.simplefilter('ignore', np.RankWarning)

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

def lomb(t, h, ofac, hifac):

    # Sample length and time span
    N = len(h)
    T = np.max(t) - np.min(t)

    # Mean and variance
    mu = np.mean(h)
    s2 = np.var(h)

    # Calculate sampling frequencies
    f = np.arange(1 / (T * ofac), hifac * N / (2 * T), 1 / (T * ofac))

#     print(len(f))
    # Calculate angular frequencies for each time point
    w = 2 * np.pi * f

    t_reshaped = t.reshape(-1, 1)

    # Calculate constant offsets
    tau = np.arctan2(np.sum(np.sin(2 * w * t_reshaped), axis=0),
                     np.sum(np.cos(2 * w * t_reshaped), axis=0)) / (2 * w)

    # Spectral power
    cterm = np.cos(w.reshape(-1, 1) * t - w.reshape(-1, 1) * tau.reshape(-1, 1))
    sterm = np.sin(w.reshape(-1, 1) * t - w.reshape(-1, 1) * tau.reshape(-1, 1))
    P = (np.sum(cterm * (h - mu), axis=1)**2 / np.sum(cterm**2, axis=1) +
         np.sum(sterm * (h - mu), axis=1)**2 / np.sum(sterm**2, axis=1)) / (2 * s2)


    # Estimate of the number of independent frequencies
    M = 2 * len(f) / ofac

    # Statistical significance of power, alarm probability rather confident
    prob = M * np.exp(-P)
    inds = prob > 0.01
    prob[inds] = 1 - (1 - np.exp(-P[inds]))**M

    # Amplitude
    P = 2 * np.sqrt(s2 * P / N)  # Amplitude

    # 95% confident level amplitude
    cf = 0.95
    cf = 1 - cf
    conf95 = -np.log(1 - (1 - cf)**(1 / M))  # Power
    conf95 = 2 * np.sqrt(s2 * conf95 / N)  # Amplitude

    return f, P


# Determine reflector height code
# Author: Max Feinland
# Date created: 11/15/23
# Last modified: 2/2/2024 by sasha
# Purpose: to adapt Kristine Larson's code and use a GNSS receiver to
# determine water level heights.
t1 = time.time()
snrFile = pd.read_csv("dino.csv")

# Find the index of the next day
# nextDay_idx = np.where(snrFile[:, 0] == 0)[0][0]

# Extract data based on the next day index
t = snrFile.t
prn = snrFile.prn
elevf = snrFile.elev
azf = snrFile.az
sNR = snrFile.snr

# housekeeping/quality control
az1, az2 = 250, 330
elev1, elev2 = 9, 20
ediff_threshold = 5

total_prns = np.unique(prn)
maxrhmax = []

for idx in total_prns:
    indices_ofcurrentprn = np.where(prn == idx)
    myprn = idx

    current_t = [t[x] for x in indices_ofcurrentprn]
    current_elev = [elevf[x] for x in indices_ofcurrentprn]
    current_snr = [sNR[x] for x in indices_ofcurrentprn]
    current_az = [azf[x] for x in indices_ofcurrentprn]

#     nanTs = np.isnan(current_t)
#     current_t = np.array(current_t)[~nanTs]
#     current_elev = np.array(current_elev)[~nanTs]
#     current_snr = np.array(current_snr)[~nanTs]
#     current_az = np.array(current_az)[~nanTs]
    
    tdiff = np.diff(current_t)
    first_tdiff_val = tdiff[np.where(tdiff > 20)]
    
    separate_arcs = np.concatenate(([0], np.where(tdiff > 20)[1], [len(current_t)]))
    # separate_arcs = np.concatenate(1, np.where(tdiff > 20), len(current_t)) # maybe add 1?
    #separate_arcs = separate_arcs-1
    arcs = []

    for k in range(len(separate_arcs) - 1):
        arcs.append(np.arange(separate_arcs[k], separate_arcs[k + 1]))

        current_t = np.array(current_t)[0]
        current_elev = np.array(current_elev)[0]
        current_snr = np.array(current_snr)[0]
        current_az = np.array(current_az)[0]
        try:
            current_arc_t = [current_t[y] for y in arcs[k]]
            current_arc_elev = [current_elev[y] for y in arcs[k]]
            current_arc_snr = [current_snr[y] for y in arcs[k]]
            current_arc_az = [current_az[y] for y in arcs[k]]
        except:
            break
        
        sampleevery5seconds = np.arange(0, len(current_arc_t), 10)
        current_arc_t = np.array([current_arc_t[x] for x in sampleevery5seconds])
        current_arc_elev = np.array([current_arc_elev[x] for x in sampleevery5seconds])
        current_arc_snr = np.array([current_arc_snr[x] for x in sampleevery5seconds])
        current_arc_az = np.array([current_arc_az[x] for x in sampleevery5seconds])
        

        if len(current_arc_t) > 0:
            p = np.polyfit(current_arc_t, current_arc_elev, 2)
    #         print(current_arc_t)
            hifielev = [x**2 * p[0] + x * p[1] + p[2] for x in current_arc_t]

            ok_indices = np.where(
                (current_arc_elev >= elev1) & (current_arc_elev <= elev2) &
                (current_arc_az >= az1) & (current_arc_az <= az2)
            )[0]
            try:
                ediff = np.ptp(current_arc_elev[ok_indices])
                conditions = [ 
                    ediff > ediff_threshold,
                    len(np.unique(current_arc_elev)) > 5,
                    len(np.unique(current_snr)) > 5,
                    len(current_arc_t) > 100
                ]

            except:
                ediff = None
                conditions = [False, True]
    #         print(ok_indices)

            if all(conditions):
                # print("all conditions check")
                # p = np.polyfit(current_arc_t, current_arc_elev, 2)
                # hifielev = current_arc_t**2 * p[0] + current_arc_t * p[1] + p[2]

                current_arc_t = current_arc_t[ok_indices]
                current_arc_elev = current_arc_elev[ok_indices]
                current_arc_az = current_arc_az[ok_indices]
                current_arc_snr = current_arc_snr[ok_indices]

                p = np.polyfit(current_arc_t, current_arc_elev, 2)
                hifielev = current_arc_t**2 * p[0] + current_arc_t * p[1] + p[2]
#                 plt.figure()
#                 plt.plot(current_arc_t, hifielev, label='adj')
#                 plt.plot(current_arc_t, current_arc_elev, label = 'raw')

                # p = np.polyfit(current_arc_t, current_arc_elev, 6) # improved polyfit to 6th order
                # hifielev = current_arc_t**6*p[0]  +  current_arc_t**5*p[1]  +  current_arc_t**4*p[2]  +  current_arc_t**3*p[3]  +  current_arc_t**2*p[4]  +  current_arc_t*p[5]  +  p[6]

                hits5 = np.where(hifielev >= 5)[0]
                threshold_index = np.where(hifielev >= 25)[0]
                ni, mi = np.max(hifielev), np.argmax(hifielev)
                index = mi if not threshold_index or mi < threshold_index[0] else threshold_index[0]

                firstarc = np.arange(hits5[0], index)
                sine = np.sin(np.radians(hifielev[firstarc]))
                linearsnr = 10**(current_arc_snr[firstarc] / 20)
                p1 = np.polyfit(sine, linearsnr, 2)
                linearsnr = linearsnr - sine**2 * p1[0] - sine * p1[1] - p1[2]
#                 plt.figure()
#                 plt.plot(sine, linearsnr)

    #             negsnr = np.where(linearsnr < -200)[0]
    #             sine = np.delete(sine, negsnr)
    #             linearsnr = np.delete(linearsnr, negsnr)

                cf = 0.1902936 / 2
                sorted_indices = np.argsort(sine)
                sortedX = sine[sorted_indices]
                sortedY = linearsnr[sorted_indices]

                t2 = time.time()
                print('Time elapsed: ', t2 - t1)
                ofac, hifac = get_ofac_hifac(hifielev[firstarc], cf, 15, 0.005)
                f, p2 = lomb(sortedX / cf, sortedY, ofac, hifac)
                lambda_val = 3e8 / 1575.42e6

#                 plt.figure()
                dispname = f"PRN-{myprn}, arc {k}"
                plt.plot(f, p2, linewidth=2, label=dispname)
                plt.xlim([0, 15])
                plt.xlabel('Reflector Height (m)')
                plt.ylabel('Amplitude')
                plt.legend()
                plt.grid(True)
                plt.title('Lomb-Scargle Periodogram')

                frange = [0, 5]
                maxRH, maxRHAmp, pknoise = peak2noise(f, p2, frange)
                print(f"Peak frequency for PRN-{myprn}, arc {k}: {maxRH} Hz")

plt.show()

# plt.savefig('plot1.png')

