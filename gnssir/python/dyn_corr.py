# dynamic height correction
import numpy as np

def dyn_corr(hs, ts, es):
    # inputs arguments: heights, times, and elevaton angles from user specified data collection period
    # (unevenly sampled and not always same length)

    # initialize size of A matrix
    A = np.empty([len(ts),2]) # default type float64
    e_dots = np.empty(len(ts)) # need to calculate numerical derivative of e wrt t
    # go through all data points
    for n in range(len(ts)):
        print(n)
        A[n][0] = 1
        A[n][1] = (np.tan(es[n]))/e_dots[n] # QUESTION: should tan be in deg or rad (and what is the default in python)
    print(A)
    return A
        
ts = [5, 4, 3, 2, 1, 9, 8, 7]
hs = [1, 1, 1, 1, 1, 8, 8, 8]
es = [1, 1, 1, 1, 1, 7, 7, 7]

dyn_corr(hs, ts, es)