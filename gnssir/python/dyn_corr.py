# dynamic height correction
import numpy as np

def dyn_corr(hs, ts, es):
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
        dt = ts[point+1] - ts[point] # dt is the user specified temporal resolution, or time between antenna height calculations
        e_dots.append((es[point+1]-es[point-1])/(2*dt)) # numerical differentiation to get time rate of change of e
        # e_dots.append(1) # numerical differentiation to get time rate of change of e
        A[n][0] = 1
        A[n][1] = (np.tan(es[point]))/e_dots[n] # ASSUMING THAT E_DOT IS IN RADS/TIME
    print('A = \n', A)
    print('hs = \n', hs[1:len(hs)-1])
    # linalg.solve is the function of NumPy to solve a system of linear scalar equations 
    H_array = np.linalg.solve(A, hs) # this will give us [H, H_dot] and what we need is H
    return H_array
        
ts = [0.0, 500.0, 1000.0, 1500.0, 2000.0, 2500.0, 3000.0, 3500.0] # times of data points [s]
hs = [12.00, 12.01, 12.02, 12.03, 12.01, 12.02, 12.01] # antenna heights [m]
es = [0.52, 0.78, 1.04, 1.57, 2.09, 2.35, 2.61, 3.0] # elevation angles [rad]

H = dyn_corr(hs, ts, es)
