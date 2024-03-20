# reflection_footprint.py
# Date: 
# Author: Rebecca Blum
# 
# Revisions: 
#   [name]     [date]     [notes]
#   R. Blum       initial script creation 
#
# Summary:
#     
#
# Inputs:
#   [antenna height]
#   [longitude]
#   [latitude]
#   [elevation angles]
#
# Outputs:
#
#------------------------------------------------------------------------------
# import packages and library 
import argparse
import sys
import matplotlib.pyplot as plt
import numpy as np

def footprint(n, lamb, e, h):
    d = n*lamb/2
    #R = h/tan(e) + (d/sin(e))/tan(e)
    #R = 90
    b = np.sqrt(2*d*h/np.sin(e) + (d/np.sin(e))**2)
    a = b/np.sin(e)
   
    theta = np.linspace(0,2*np.pi,100)
   
    for i in range(99):
        x = []
        y = []
   
        dx = a*np.cos(theta[i]) #+ R;
        dy = b*np.sin(theta[i])
   
        x.append(np.sin(a)*dx - np.cos(a)*dy)
        y.append(np.sin(a)*dy + np.cos(a)*dx)
   
    x = b*np.cos(theta)
    y = a*np.sin(theta)
    return x,y

def rotate(x,y,theta):
    x2 = []
    y2 = []
    R = np.array([[np.cos(theta), -np.sin(theta)],[np.sin(theta),  np.cos(theta)]])
    for i in range(99):
        xy = np.matmul(R,np.array([x[i],y[i]]))
        x2.append(xy[0])
        y2.append(xy[1])

    return x2, y2

def main():
    n = 1
    lamb = 19.05/100 # cm -> m
    e = 20*np.pi/180; # rad
    h = 2 # meters

    [x,y] = footprint(n, lamb, e, h)
    plt.plot(x,y)
    plt.show()

    theta = 60*np.pi/180
    [x2,y2] = rotate(x,y,theta)

    plt.plot(x2,y2)
    plt.show()
if __name__ == "__main__":
    main()
