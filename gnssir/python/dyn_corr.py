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
        dt = ts[point+1] - ts[point] # dt is the sampling frequency
        e_dots.append((es[point+1]-es[point-1])/(2*dt)) # numerical differentiation to get time rate of change of e
        A[n][0] = 1
        A[n][1] = (np.tan(es[point]))/e_dots[n] # ASSUMING THAT E_DOT IS IN RADS/TIME
    print('size of A:', A.shape)
    print('e_dots = \n', e_dots)
    hs = hs[1:len(hs)-1]
    print('size of hs: ', hs.shape)
    print('hs = \n', hs)
    H_array, residuals, rank, singular_values = np.linalg.lstsq(A, hs, rcond=None)
    return H_array
        
ts = [0.0, 500.0, 1000.0, 1500.0, 2000.0, 2500.0, 3000.0, 3500.0] # times of data points [s]
hs = np.array([12, 14, 16, 25, 22, 19, 14, 10]) # antenna heights [m]
hs = hs.reshape(8,1)
es = [0.52, 0.78, 1.04, 1.57, 2.09, 2.35, 2.61, 2.70, 3.0] # elevation angles [rad]

H = dyn_corr(hs, ts, es)
print('H = ', H)
