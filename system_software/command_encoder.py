# command_encoder.py
# Date: 1/2/24
# Author: Rebecca Blum
# 
# Revisions:
#   [name]     [date]     [notes]
#   R. Blum    1/11/24    initial script creation 
#
# Summary:
#   This script translates input "human readable" commands into binary. It then
#   sends off the binary sequences to the onsite system via Iridium. 
#
# Inputs:
#   [command type]
#   [command argument 1] - optional
#   [command argument 2] - optional
#
# Outputs:
#   None/message sent to Iridium
#
#------------------------------------------------------------------------------
# import packages and library 
import os
import sys
import argparse
import numpy
#import matplotlib.pyplot as plt

#def parse_args():

#    try:
#        print("Hello")
#    except:
#        print("Something went wrong")
#    else:
#        print("Nothing went wrong")

def dec2bin(value, length):
    long_binary = ['0']*length
    binary = [*str(bin(int(value)))]
    long_binary[2+length-len(binary):length] = binary[2:len(binary)]
    bin_string = "".join(long_binary)

    return bin_string

def func(id,value):

    if id.lower() == 'sf':
        # set sampling frequency of GNSS reciever
        if len(value) > 1:
            print("Error: too many input values for the sampling frequency")
            return
        cmd = 'sf='+value[0]
        cmds.append(cmd + ';')

    elif id.lower() == 'el':
        # set elevation angle range
        if len(value) > 2:
            print("Error: too many input values for the elevation angle range")
            return
        cmd = 'el='+value[0]+','+value[1]
        cmds.append(cmd + ';')

    elif id.lower() == 'az':
        # set azimuth angle range
        if len(value) > 2:
            print("Error: too many input values for the azimuth angle range")
            return
        cmd = 'az='+value[0]+','+value[1]
        cmds.append(cmd + ';')

    elif id.lower() == 'mode':
        # set system to calibration or normal mode
        if len(value) > 1:
            print("Error: too many input values for the mode")
            return
        cmd = 'mode='+value[0]
        cmds.append(cmd + ';')
        # set variables/settings/flags such that:
        # - system checks inbox every 5(?) minutes
        # - send back azmuth range once set?

    elif id.lower() == 'tres':
        # set time resolution of water level measurements
        if len(value) > 1:
            print("Error: too many input values for the time resolution")
            return
        cmd = 'tres='+value[0]
        cmds.append(cmd + ';')

    else: 
        print('Error: command not defined in database')

    # list to string

    return bin_cmd

def main():
    input = sys.argv

    cmd = input[1:len(input)] # the zeroeth entry is not useful here 

    print('\n')
 
    #os.system("python command_interpreter.py " + cmd)  
    
    print("done")
    
    return 

if __name__ == "__main__":
    main()
    
#input = '0b' + '0101' + '001100' + '110000'
#input = '0b' + '0100' + '00111' + '11111'
#input = '0b' + '0001' + '0011'
#output = ["freq", "max_el", "min_el", "max_az", "min_az","calibration","time_res"]    
